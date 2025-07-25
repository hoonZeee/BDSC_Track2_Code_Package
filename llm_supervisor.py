import re
import statistics
from collections import defaultdict
from rumor_supervisor.supervisor import BDSC2025SupervisorBase


class MySupervisor(BDSC2025SupervisorBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rumor_score_cache = {}            # agent_id → 루머 점수 캐시
        self.warning_count = defaultdict(int)  # agent_id → 누적 경고 횟수
        self.rumor_threshold = 5.0             # 루머 판단 기준
        self.retweet_threshold = 3             # 삭제 기준: 리트윗 수
        self.ban_warning_threshold = 3         # 밴 기준: 누적 경고 수

    async def interventions(self):
        posts = self.sensing_api.get_posts_current_round()
        if not posts:
            return

        spread_count = defaultdict(int)
        for post in posts:
            spread_count[post["sender_id"]] += 1

        candidate_scores = []
        for agent_id in spread_count:
            score = await self._get_rumor_score(agent_id)
            if score >= self.rumor_threshold:
                candidate_scores.append((agent_id, spread_count[agent_id], score))

        if not candidate_scores:
            return

        # 루머 점수 × 확산량 기준으로 타겟 선정
        target_id, _, score = max(candidate_scores, key=lambda x: x[1] * x[2])
        self.warning_count[target_id] += 1

        # 1. 게시글 삭제
        for post in self.sensing_api.get_posts_sent_by_agent_current_round(target_id):
            if await self._should_delete_post(post):
                self.delete_post_intervention(post["post_id"])

        # 2. 설득 메시지 전송
        self._send_persuasion_message(target_id, score)

        # 3. 위험 팔로워 제거
        self._remove_risky_follower(target_id)

        # 4. 계정 밴 조건 체크
        if (
            score >= 8.0 and
            self.warning_count[target_id] >= self.ban_warning_threshold and
            spread_count[target_id] > self.retweet_threshold
        ):
            self.ban_agent_intervention(target_id, "⚠️ Multiple warnings and high rumor activity.")

    async def _get_rumor_score(self, agent_id: int) -> float:
        if agent_id in self.rumor_score_cache:
            return self.rumor_score_cache[agent_id]

        posts = self.sensing_api.get_all_posts_sent_by_agent(agent_id)
        if not posts:
            self.rumor_score_cache[agent_id] = 2.0
            return 2.0

        recent_posts = posts[:5]
        scores = []

        for post in recent_posts:
            prompt = self._build_rumor_prompt(post["content"])
            try:
                response = await self.llm.atext_request([{"role": "user", "content": prompt}], port=16528)
                match = re.search(r"\d+(\.\d+)?", response)
                if match:
                    scores.append(float(match.group()))
            except Exception:
                continue

        if not scores:
            final_score = 2.0
        else:
            avg = sum(scores) / len(scores)
            stddev = statistics.stdev(scores) if len(scores) > 1 else 0
            final_score = max(avg + 0.5 * stddev, max(scores))

        self.rumor_score_cache[agent_id] = final_score
        return final_score

    def _build_rumor_prompt(self, content: str) -> str:
        return (
            "You are a reliable AI fact-checker.\n"
            "Evaluate the credibility of the following social media message and provide a rumor score from 0 to 10.\n\n"
            f"Message:\n{content}\n\n"
            "Evaluation Criteria:\n"
            "1. Is the message based on credible or official sources?\n"
            "2. Does it contain overly emotional or sensational language?\n"
            "3. Are there logical inconsistencies or unverifiable claims?\n"
            "4. Is there any indication of prior fact-checks or history of being flagged?\n"
            "5. Does the message follow patterns of previously known misinformation?\n\n"
            "Respond ONLY with a number from 0 to 10 (e.g., 7.0)."
        )

    async def _should_delete_post(self, post: dict) -> bool:
        score = await self._get_rumor_score(post["sender_id"])
        shares = len(post.get("receiver_ids", []))
        return score >= self.rumor_threshold and shares >= self.retweet_threshold

    def _remove_risky_follower(self, target_id: int):
        followers = self.sensing_api.get_following(target_id)
        if not followers:
            return

        def rumor_traffic(f_id: int) -> int:
            return self.sensing_api.get_public_edge_rumor_traffic(target_id, f_id)

        risky_follower = max(followers, key=rumor_traffic, default=None)
        if risky_follower:
            self.remove_follower_intervention(risky_follower, target_id)

    def _send_persuasion_message(self, agent_id: int, score: float):
        if score >= 8.0:
            message = (
                f"Your recent posts are highly suspected of spreading false information. Rumor Score: {score:.1f}\n\n"
                "Spreading unverified claims can lead to severe consequences, including account bans.\n"
                "Please only share information from verified government or media sources.\n"
                "Let’s work together to keep this space trustworthy."
            )
        elif score >= 5.0:
            message = (
                f"⚠️ Your posts may contain unverified or misleading information. Rumor Score: {score:.1f}\n\n"
                "To ensure accuracy, please cross-check your content using:\n"
                " - Government announcements\n"
                " - Trusted news outlets\n"
                " - Fact-checking platforms (e.g., Snopes, FactCheck.org)\n"
                "Avoid contributing to misinformation online."
            )
        else:
            message = (
                f"Please be mindful when posting sensitive information. Rumor Score: {score:.1f}\n\n"
                "Consider including credible sources and avoiding emotionally charged expressions."
            )

        self.persuade_agent_intervention(agent_id, message)
