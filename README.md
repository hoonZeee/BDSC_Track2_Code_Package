# BDSC2025-社交网络谣言监管挑战赛-代码参赛手册
## 目录
- [BDSC2025-社交网络谣言监管挑战赛-代码参赛手册](#bdsc2025-社交网络谣言监管挑战赛-代码参赛手册)
  - [目录](#目录)
  - [1. 赛题介绍](#1-赛题介绍)
    - [1.1 竞赛背景](#11-竞赛背景)
    - [1.2 竞赛环境](#12-竞赛环境)
    - [1.3 模拟过程](#13-模拟过程)
    - [1.4 干预方式与配额](#14-干预方式与配额)
    - [1.5 评价指标](#15-评价指标)
  - [2. 参赛方式](#2-参赛方式)
    - [2.1 核心目标](#21-核心目标)
    - [2.2 代码参赛示例](#22-代码参赛示例)
      - [2.3 监管智能体设计空间](#23-监管智能体设计空间)
  - [3. 环境接口](#3-环境接口)
    - [3.1 感知接口](#31-感知接口)
      - [3.1.1 消息传播信息获取类](#311-消息传播信息获取类)
      - [3.1.2 智能体状态与干预历史类](#312-智能体状态与干预历史类)
      - [3.1.3 网络结构信息类](#313-网络结构信息类)
      - [3.1.4 监管者状态与配额类](#314-监管者状态与配额类)
      - [3.1.5 平台信息类](#315-平台信息类)
    - [3.2 干预接口](#32-干预接口)
  - [4. 本地安装与运行指南](#4-本地安装与运行指南)
    - [4.1 依赖安装](#41-依赖安装)
      - [4.1.1 核心依赖](#411-核心依赖)
      - [4.1.2 外部服务依赖](#412-外部服务依赖)
    - [4.2 配置文件准备](#42-配置文件准备)
      - [4.2.1 地图文件](#421-地图文件)
      - [4.2.2 智能体档案文件](#422-智能体档案文件)
    - [4.3 运行配置](#43-运行配置)
      - [4.3.1 基础配置示例](#431-基础配置示例)
      - [4.3.2 配置参赛方案（本地部署）](#432-配置参赛方案本地部署)
    - [4.4 运行步骤](#44-运行步骤)
      - [4.4.1 快速开始](#441-快速开始)
      - [4.4.2 运行监控](#442-运行监控)
      - [4.4.3 结果查看](#443-结果查看)
    - [4.5 常见问题与解决方案](#45-常见问题与解决方案)
      - [4.5.1 依赖问题](#451-依赖问题)
      - [4.5.2 连接问题](#452-连接问题)
      - [4.5.3 性能问题](#453-性能问题)
  - [5. 软件包主要文件清单](#5-软件包主要文件清单)
    - [5.1 rumor\_supervisor/ - 核心框架代码](#51-rumor_supervisor---核心框架代码)
      - [5.1.1 主要模块文件](#511-主要模块文件)
      - [5.1.2 supervisor/ - 监管智能体框架](#512-supervisor---监管智能体框架)
        - [5.1.2.1 sensing\_api.py - 智能体工具集](#5121-sensing_apipy---智能体工具集)
    - [5.2 profiles/ - 智能体档案数据](#52-profiles---智能体档案数据)
    - [5.3 example/ - 运行示例](#53-example---运行示例)
  - [6. 提交方式](#6-提交方式)

## 1. 赛题介绍
### 1.1 竞赛背景
在社交媒体时代，谣言传播速度快、影响范围广，对社会稳定和公共秩序造成潜在威胁。如何有效监测和干预谣言传播成为亟待解决的重要问题。本次挑战赛旨在通过智能体技术，探索在社交网络环境中进行谣言监管的有效策略，参赛者需要设计一个监管智能体，在有限的干预配额下，通过合理的检测和干预策略，最大限度地减少谣言在社交网络中的传播。

### 1.2 竞赛环境
**社交网络**：
- 从真实社交媒体用户网络中采样出比赛的网络结构，网络结构存储在`network.csv`文件中，包含三列：source（关注者ID）、target（被关注者ID）、type（边类型）
- type=1：单向关注关系（关注者可以看到被关注者的帖子）
- type=2：双向关注关系（可以互相私聊）
- 网络中包含200个智能体

**智能体画像**：
- 每个智能体具有自身画像，包括：姓名、性别、年龄段、职业、消息传播偏好、背景故事
- 包含从`network.csv`文件中提取出的供模拟使用的社交网络结构
- 智能体的消息传播偏好类型包括：
    - **阴谋论者**：被干预会使得更加相信谣言
    - **轻信者**：会非常相信谣言
    - **批判思考者**：倾向于质疑信息真实性，不容易相信没有可靠来源的谣言
    - **谨慎分享者**：更倾向于私聊分享不确定的信息，在公开发帖时保持低调
    - **社交表现者**：为获得社交关注而传播消息，不关心消息真假

**谣言源设置**：
- 平台设有1名散播谣言的谣言源（ID为5000）
- 谣言源传播消息不受社交网络约束
- 谣言内容：西瓜大丰收，大棚西瓜价格在2026年12月10日只要每斤5角钱。朋友们快买！

### 1.3 模拟过程
共进行20轮谣言传播模拟。

- **谣言源传播**：
    - 每轮发布帖子，帖子内容包含谣言。
    - 每轮随机10个智能体在平台上看到谣言源的帖子。
    - 谣言源按策略选择5个智能体进行私聊。

- **普通智能体传播**：
    - 智能体根据收到的消息、历史消息总结、个人profile和被干预历史，生成新的消息总结。
    - 基于消息总结生成发帖内容，最多10个关注者可见。
    - 随机选择最多2个互相关注的好友进行私聊。
    - 只有曾经收到过消息的智能体才会产生和传播消息。

- **监管干预**：
    - 监管智能体可以进行对公开发帖内容进行检测和干预，但无法干预私聊内容。
    - 监管智能体的干预时间是在帖子内容产生、接收者选定后，智能体看到帖子之前。
    - 施加的干预本轮立即生效。

- **最终评估**：
    - 20轮传播结束后，通过问卷调研所有智能体对各个谣言的相信程度。

### 1.4 干预方式与配额
**干预方式**：
- **屏蔽帖子**：
  - 功能：屏蔽某个智能体本轮发送的特定帖子
  - 效果：所有原本应该看到该帖子的智能体都无法看到
- **劝说**：
  - 功能：向智能体发送劝说消息，提醒其不要相信或传播谣言
  - 效果：有效的劝说可能影响智能体的后续行为决策
- **移除关注者**：
  - 功能：永久移除某个关注关系
  - 效果：被移除的关注者无法再看到该智能体的帖子
- **封号**：
  - 功能：永久禁止智能体发帖
  - 效果：该智能体后续无法发帖

**干预配额**：
- 每轮最多屏蔽20条帖子        
- 每轮最多劝说20个智能体       
- 整个比赛过程最多移除100个关注关系 
- 整个比赛过程最多封禁20个智能体

**注意**：超过配额限制的干预操作将直接失效。

### 1.5 评价指标
在谣言传播20轮次后，通过问卷调查各智能体对谣言内容的相信程度，以此评价参赛者所设计监管系统的干预效果。

## 2. 参赛方式

参赛者可以基于提供的接口，使用Python代码灵活开发监管智能体。需要实现一个监管智能体类，包含检测和干预逻辑。 

**实现方式**：
- 继承基础监管智能体类
- 实现检测逻辑（判断消息是否为谣言）
- 实现干预策略（决定何时使用何种干预手段）
- 合理使用感知接口获取信息
- 在配额限制内调用干预接口

### 2.1 核心目标

基于各类工具，完成对监管智能体的开发。参赛者需要设计一个监管智能体，该智能体需要继承自`BDSC2025SupervisorBase`基类，并实现`interventions`方法。监管智能体的主要任务是通过各种工具与社交网络中的智能体进行互动，有效监测和干预谣言传播。

```python
# 示例代码
from rumor_supervisor.supervisor import BDSC2025SupervisorBase

class MySupervisor(BDSC2025SupervisorBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def interventions(self):
        # 实现监管者的功能
        pass
```

### 2.2 代码参赛示例

以下是一个完整的代码参赛示例，展示了如何实现一个基础的监管智能体：

```python
import random

from rumor_supervisor.supervisor import BDSC2025SupervisorBase


class MySupervisor(BDSC2025SupervisorBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def interventions(self):
        # 实现监管者的功能
        posts = self.sensing_api.get_posts_current_round()
        # 实现监管者的功能
        agent_id = posts[0]["sender_id"]
        # 接口调用例
        posts_received = self.sensing_api.get_all_posts_received_by_agent(agent_id)
        posts_sent = self.sensing_api.get_all_posts_sent_by_agent(agent_id)
        posts_received_last_k_rounds = (
            self.sensing_api.get_posts_received_by_agent_last_k_rounds(agent_id, 10)
        )
        posts_sent_last_k_rounds = (
            self.sensing_api.get_posts_sent_by_agent_last_k_rounds(agent_id, 10)
        )
        posts_received_current_round = (
            self.sensing_api.get_posts_received_by_agent_current_round(agent_id)
        )
        posts_sent_current_round = (
            self.sensing_api.get_posts_sent_by_agent_current_round(agent_id)
        )
        # 随机删除5个帖子
        for post in random.sample(posts, 5):
            self.delete_post_intervention(post["post_id"])
        # 随机劝说1个智能体
        agent_ids = [p["sender_id"] for p in posts]
        agent_id = random.choice(agent_ids)
        self.persuade_agent_intervention(agent_id, "请注意文明用语，不要发布不当言论。")
        # 随机移除1个智能体的1个关注
        follower_ids = self.sensing_api.get_following(agent_id)
        if len(follower_ids) > 0:
            follower_id = random.choice(follower_ids)
            self.remove_follower_intervention(follower_id, agent_id)
        # 随机封禁1个智能体
        agent_ids = [p["sender_id"] for p in posts]
        agent_id = random.choice(agent_ids)
        self.ban_agent_intervention(agent_id)

```

本示例是一个基础的监管智能体实现：

1. **基础框架**：继承`BDSC2025SupervisorBase`并实现`interventions`方法
2. **干预功能**：实现了四种基本的干预方式：
   - 删除帖子
   - 劝说智能体
   - 移除关注关系
   - 封禁智能体
3. **简单策略**：使用随机选择的方式决定干预对象

参赛者可以基于这个示例进行改进和优化，例如：
- 实现更智能的谣言检测算法
- 优化干预对象的选择策略
- 添加干预效果的评估机制
- 实现更复杂的决策机制，根据历史数据调整策略

#### 2.3 监管智能体设计空间

参赛者可以基于这个示例进行改进和优化，例如：
- 使用大模型检查帖子内容，根据之前轮次发言内容判断智能体情况
- 根据智能体情况选择不同的说服内容
- 对积极传谣的智能体进行禁言
- 对不相信谣言的智能体进行鼓励

## 3. 环境接口
### 3.1 感知接口

本部分干预接口为监管者提供获取公域网络中消息传播、智能体状态、干预历史等信息的能力。
通过self.sensing_api.<function_name>调用。

#### 3.1.1 消息传播信息获取类
- `# 获取所有历史帖子`
  `get_all_historical_posts() -> list[dict]`
  - 功能：获取从比赛开始到当前轮次之前（包含当前轮已处理完的帖子）的所有公开帖子
  - 返回：帖子列表，每个帖子是一个字典，包含帖子相关信息

- `# 获取最近k轮的帖子`
  `get_posts_last_k_rounds(k: int) -> list[dict]`
  - 功能：获取最近k个已完成轮次的全部公开帖子，不包括当前正在进行的轮次
  - 参数：
    - k: 要获取的轮次数
  - 返回：帖子列表

- `# 获取本轮产生的所有帖子`
  `get_posts_current_round() -> list[dict]`
  - 功能：获取本轮到目前为止产生的所有公开帖子（在监管者调用时，即预备帖子列表）
  - 返回：帖子列表

- `# 获取指定智能体接收到的帖子`
  `get_all_posts_received_by_agent(agent_id: int) -> list[dict]`
  - 功能：获取指定智能体在所有历史轮次中（含当前轮预备接收）作为接收者意图接收的所有公开帖子
  - 参数：
    - agent_id: 智能体ID
  - 返回：帖子列表

  `get_posts_received_by_agent_last_k_rounds(agent_id: int, k: int) -> list[dict]`
  - 功能：获取指定智能体在最近k个已完成轮次中作为接收者意图接收的所有公开帖子
  - 参数：
    - agent_id: 智能体ID
    - k: 要获取的轮次数
  - 返回：帖子列表

  `get_posts_received_by_agent_current_round(agent_id: int) -> list[dict]`
  - 功能：获取指定智能体在本轮作为接收者意图接收的所有公开帖子
  - 参数：
    - agent_id: 智能体ID
  - 返回：帖子列表

- `# 获取指定智能体发送的帖子`
  `get_all_posts_sent_by_agent(agent_id: int) -> list[dict]`
  - 功能：获取指定智能体在所有历史轮次中（含当前轮预备发送）发送的所有公开帖子
  - 参数：
    - agent_id: 智能体ID
  - 返回：帖子列表

  `get_posts_sent_by_agent_last_k_rounds(agent_id: int, k: int) -> list[dict]`
  - 功能：获取指定智能体在最近k个已完成轮次中发送的所有公开帖子
  - 参数：
    - agent_id: 智能体ID
    - k: 要获取的轮次数
  - 返回：帖子列表

  `get_posts_sent_by_agent_current_round(agent_id: int) -> list[dict]`
  - 功能：获取指定智能体在本轮到目前为止预备发送的所有公开帖子
  - 参数：
    - agent_id: 智能体ID
  - 返回：帖子列表

- `# 根据ID获取帖子内容`
  `get_post_content_by_id(message_id: str) -> str | None`
  - 功能：根据消息ID获取其具体内容（从全局历史和当前轮缓存中查找）
  - 参数：
    - message_id: 消息ID
  - 返回：消息内容字符串，如果未找到则返回None

- `# 搜索包含关键词的帖子`
  `get_posts_containing_keywords(keywords: list[str], search_scope: str, agent_id_context: int = None, last_k_rounds_context: int = None) -> list[dict]`
  - 功能：在公域消息中搜索包含指定任意一个关键词的消息
  - 参数：
    - keywords: 关键词列表
    - search_scope: 搜索范围，可选值：
      - "current_round_all_senders": 当前轮所有发送者
      - "current_round_sent_by_agent": 当前轮指定智能体发送
      - "current_round_received_by_agent": 当前轮指定智能体接收
      - "historical_sent_by_agent": 历史指定智能体发送
      - "historical_received_by_agent": 历史指定智能体接收
      - "all_historical": 所有历史
    - agent_id_context: 当search_scope需要指定智能体时的智能体ID
    - last_k_rounds_context: 当搜索历史时的轮次数
  - 返回：匹配的帖子列表

#### 3.1.2 智能体状态与干预历史类
- `# 获取智能体本轮违规帖子`
  `get_agent_offending_posts_current_round(agent_id: int) -> list[dict]`
  - 功能：获取指定智能体在本轮发送的、被监管判定为违规的帖子
  - 参数：
    - agent_id: 智能体ID
  - 返回：违规帖子列表，每个帖子包含post_id、content和detection_method

- `# 获取智能体历史违规轮次`
  `get_agent_historical_offense_rounds(agent_id: int) -> list[dict]`
  - 功能：获取指定智能体所有发送过违规帖子的轮次及首个违规帖子内容摘要
  - 参数：
    - agent_id: 智能体ID
  - 返回：违规轮次列表，每个元素包含轮次号和违规内容摘要

- `# 获取智能体被干预历史`
  `get_agent_intervention_history(agent_id: int) -> list[dict]`
  - 功能：获取指定智能体受到的所有干预措施的历史记录
  - 参数：
    - agent_id: 智能体ID
  - 返回：干预历史记录列表

- `# 统计智能体间的消息传播次数`
  `count_posts_between_agents(sender_id: int, receiver_id: int, count_scope: str = 'all_historical', last_k_rounds: int = None) -> int`
  - 功能：统计在公域网络中，一个智能体的帖子被另一个智能体看到的次数（基于原始意图）
  - 参数：
    - sender_id: 发送者ID
    - receiver_id: 接收者ID
    - count_scope: 统计范围，可选值：
      - "all_historical": 所有历史
      - "current_round": 当前轮
      - "last_k_rounds": 最近k轮
    - last_k_rounds: 当count_scope为"last_k_rounds"时的轮次数
  - 返回：传播次数

- `# 获取智能体违规行为统计`
  `get_agent_historical_offense_summary(agent_id: int) -> dict`
  - 功能：获取指定智能体历史上的"违规行为"概要统计
  - 参数：
    - agent_id: 智能体ID
  - 返回：统计信息字典，包含：
    - total_rumors_sent_by_llm_detection: LLM检测到的谣言数
    - total_rumors_sent_by_keyword_detection: 关键词检测到的谣言数
    - times_communicated_by_regulator: 被监管者沟通次数
    - times_its_messages_blocked: 消息被屏蔽次数

- `# 获取某条边上的违规消息流量`
  `get_public_edge_rumor_traffic(agent_id_1: int, agent_id_2: int) -> int`
  - 功能：获取某条公域网络边上累计传播的、被判定为违规消息的数量（基于原始意图）
  - 参数：
    - agent_id_1: 发送者ID
    - agent_id_2: 接收者ID
  - 返回：违规消息数量

- `# 获取本轮所有谣言消息ID`
  `get_rumor_message_ids_current_round() -> list[str]`
  - 功能：获取本轮所有被监管者判定为谣言的消息ID列表
  - 返回：消息ID列表

#### 3.1.3 网络结构信息类
- `# 获取网络结构`
  `get_public_network_structure() -> dict`
  - 功能：获取当前公域网络的结构
  - 返回：网络结构字典，包含边列表

- `# 获取节点度数`
  `get_public_node_degree(agent_id: int) -> tuple[int, int]`
  - 功能：获取指定智能体在当前网络中的入度(多少人关注TA)和出度(TA关注多少人)
  - 参数：
    - agent_id: 智能体ID
  - 返回：(入度, 出度)元组

- `# 获取度数最高的k个节点`
  `get_top_degree_nodes(top_k: int, degree_type: str = "total") -> list[int]`
  - 功能：获取当前网络中指定类型度排名前top_k的智能体ID列表
  - 参数：
    - top_k: 要获取的节点数量
    - degree_type: 度数类型，可选值：
      - "in": 入度
      - "out": 出度
      - "total": 总度数
  - 返回：智能体ID列表

- `# 获取度数排名第rank的节点`
  `get_public_node_at_degree_rank(rank: int, degree_type: str = "total") -> int | None`
  - 功能：获取当前公域网络中指定类型度排名第rank位的智能体ID
  - 参数：
    - rank: 排名（从1开始）
    - degree_type: 度数类型，可选值同get_top_degree_nodes
  - 返回：智能体ID，如果不存在则返回None

- `# 获取节点的邻居`
  `get_public_neighbors(agent_id: int) -> list[int]`
  - 功能：获取指定智能体在当前公域网络中的所有邻居（TA关注的 + 关注TA的）
  - 参数：
    - agent_id: 智能体ID
  - 返回：邻居智能体ID列表

#### 3.1.4 监管者状态与配额类
- `# 获取剩余干预配额`
  `get_remaining_intervention_quotas() -> dict`
  - 功能：获取当前监管智能体剩余的各类干预措施的配额
  - 返回：配额信息字典，包含每种干预类型的：
    - round_remaining: 本轮剩余配额
    - global_remaining: 全局剩余配额
    - round_limit: 每轮限制
    - global_limit: 全局限制

- `# 获取已封禁的元素`
  `get_globally_blocked_elements() -> dict`
  - 功能：获取已经被永久封禁的智能体和被永久移除的关注关系
  - 返回：包含blocked_agents和cut_edges的字典

- `# 获取本轮已执行的干预`
  `get_interventions_by_me_this_round() -> list[dict]`
  - 功能：获取当前监管智能体在本轮已经执行的干预操作列表
  - 返回：干预操作列表

- `# 获取所有已执行的干预`
  `get_interventions_by_me() -> list[dict]`
  - 功能：获取当前监管智能体全部（历史）已经执行的干预操作列表
  - 返回：干预操作列表

#### 3.1.5 平台信息类
- `# 获取当前轮次`
  `get_current_round_number() -> int`
  - 功能：获取当前的比赛轮次
  - 返回：当前轮次号

- `# 获取总轮次数`
  `get_total_simulation_rounds() -> int`
  - 功能：获取本次模拟比赛总共的轮次数
  - 返回：总轮次数

- `# 获取谣言主题描述`
  `get_rumor_topic_description() -> list[str]`
  - 功能：获取当前比赛设定的核心谣言主题的文字描述（问卷用）
  - 返回：谣言主题描述列表


### 3.2 干预接口

本部分干预接口为监管者提供对公域网络中消息传播、智能体状态、干预历史等信息的能力。
通过self.<function_name>调用。

- `# 屏蔽帖子`
  `delete_post(post_id: str, reason: str = "") -> bool`
  - 功能：阻止指定的消息，使其无法被接收者看到
  - 参数：
    - post_id: 要屏蔽的消息ID
    - reason: 屏蔽原因（可选）
  - 返回：是否成功屏蔽
  - 说明：
    - 每轮最多屏蔽20条帖子
    - 屏蔽后，所有原本应该看到该帖子的智能体都无法看到
    - 会向发送者发送通知消息

- `# 劝说智能体`
  `persuade_agent(agent_id: int, content: str) -> bool`
  - 功能：向智能体发送劝说消息，提醒其不要相信或传播谣言
  - 参数：
    - agent_id: 目标智能体ID
    - content: 劝说消息内容
  - 返回：是否成功发送劝说消息
  - 说明：
    - 每轮最多劝说20个智能体
    - 劝说消息会作为私聊消息发送给目标智能体
    - 有效的劝说可能影响智能体的后续行为决策

- `# 移除关注关系`
  `remove_follower(follower_id: int, followed_id: int) -> bool`
  - 功能：永久移除某个关注关系
  - 参数：
    - follower_id: 要移除的关注者ID
    - followed_id: 被关注的智能体ID
  - 返回：是否成功移除关注关系
  - 说明：
    - 整个比赛过程最多移除100个关注关系
    - 移除后，被移除的关注者无法再看到该智能体的帖子
    - 会向双方发送通知消息
    - 不能移除谣言源（ID为5000）的关注关系

- `# 封禁智能体`
  `ban_agent(agent_id: int, reason: str = "") -> bool`
  - 功能：永久禁止智能体发帖
  - 参数：
    - agent_id: 要封禁的智能体ID
    - reason: 封禁原因（可选）
  - 返回：是否成功封禁
  - 说明：
    - 整个比赛过程最多封禁20个智能体
    - 封禁后，该智能体后续无法发帖
    - 会向被封禁的智能体发送通知消息
    - 不能封禁谣言源（ID为5000）


## 4. 本地安装与运行指南

### 4.1 依赖安装

#### 4.1.1 核心依赖

本项目基于 `agentsociety` 框架构建，如您想要本地运行，请参考[AgentSociety](https://github.com/tsinghua-fib-lab/AgentSociety)安装进行安装.

```bash
# 克隆项目
git clone <repository-url>
cd bdsc2025-rumor-governance

# 安装依赖（推荐使用uv安装）uv包管理器安装指南：https://docs.astral.sh/uv/getting-started/installation/
uv sync

# 或使用pip安装
pip install -e .
```

#### 4.1.2 外部服务依赖

**必需服务：**
- **LLM API服务**：支持OpenAI、Qwen等多种LLM提供商

**可选服务：**
- **PostgreSQL数据库**：用于可视化界面（会降低仿真速度 - 如无需前端显示建议关闭）
- **MLflow服务**：用于实验跟踪（本竞赛中不需要）

如需本地部署测试，请参考[AgentSociety本地部署指南](https://agentsociety.readthedocs.io/en/latest/01-quick-start/02-start-your-first-simulation.html#step-0-installation)

### 4.2 配置文件准备

#### 4.2.1 地图文件

下载并配置[北京市地图文件 - 点击下载](https://cloud.tsinghua.edu.cn/f/f5c777485d2748fa8535/?dl=1)：
```bash
# 地图文件路径示例
map_file_path = "path/to/srt.map_beijing_extend_20241201.pb"
cache_file_path = "path/to/srt.map_beijing_extend_20241201.cache"
```

#### 4.2.2 智能体档案文件

项目提供了三类智能体的档案文件：
- `./proiles/population_profiles.json` - 市民档案文件
- `./proiles/spreader_profile.json` - 谣言传播者档案文件
- `./proiles/supervisor_profile.json` - 监管者档案文件

### 4.3 运行配置

本地运行请参考[example/main.py](./example/main.py)

#### 4.3.1 基础配置示例

创建运行脚本 `my_run.py`：

```python
from __future__ import annotations

import asyncio

import pandas as pd
import ray
from agentsociety.configs import (AgentConfig, AgentsConfig, Config, EnvConfig,
                                  LLMConfig, MapConfig)
from agentsociety.configs.env import AvroConfig, MlflowConfig, PostgreSQLConfig
from agentsociety.llm import LLMProviderType
from agentsociety.simulation import AgentSociety

from rumor_supervisor import BaselineSupervisor
from rumor_supervisor.envcitizen import TrackTwoEnvCitizen
from rumor_supervisor.rumor_spreader import RumorSpreader
from rumor_supervisor.workflows import TRACK_TWO_EXPERIMENT


async def main():
    llm_configs = [
        LLMConfig(
            provider=LLMProviderType.Qwen,
            base_url=None,
            api_key="YOUR_API_KEY",
            model="CHOOSE_YOUR_MODEL",
            semaphore=200,
        ),
        # You can add more LLMConfig here
    ]
    env_config = EnvConfig(
        pgsql=PostgreSQLConfig(
            enabled=False,  # Set to True if you want to visualize the simulation in the web UI. Notice that this will SLOW DOWN the simulation.
            dsn="YOUR_POSTGRESQL_DSN",
            num_workers="auto",
        ),
        mlflow=MlflowConfig(  # Do not need mlflow in this simulation
            enabled=False,
            mlflow_uri="http://localhost:5000",
            username="admin",
            password="admin",
        ),
        avro=AvroConfig(
            enabled=True,
        ),
    )
    map_config = MapConfig(
        file_path="THE_PATH_TO_YOUR_MAP_FILE",
        cache_path="THE_PATH_TO_YOUR_MAP_CACHE_FILE",
    )

    config = Config(
        llm=llm_configs,
        env=env_config,
        map=map_config,
        agents=AgentsConfig(
            citizens=[
                AgentConfig(
                    agent_class=TrackTwoEnvCitizen,
                    memory_from_file="./proiles/population_profiles.json",
                ),
                AgentConfig(
                    agent_class=RumorSpreader,
                    memory_from_file="./proiles/spreader_profile.json",
                ),
            ],
            supervisor=AgentConfig(
                agent_class=BaselineSupervisor,
                memory_from_file="./proiles/supervisor_profile.json",
            ),
        ),  # type: ignore
        exp=TRACK_TWO_EXPERIMENT,
    )  # type: ignore
    agentsociety = AgentSociety(config, tenant_id="DEMO")
    await agentsociety.init()
    await agentsociety.run()
    try:
        await agentsociety.close()
    except Exception as e:
        pass
    ray.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
```

#### 4.3.2 配置参赛方案（本地部署）

如果选择配置参赛方案，可以通过调整参数来优化Baseline智能体：

```python
import asyncio

import ray
from agentsociety.configs import (AgentConfig, AgentsConfig, Config, EnvConfig,
                                  LLMConfig, MapConfig)
from agentsociety.llm import LLMProviderType
from agentsociety.metrics import MlflowConfig
from agentsociety.simulation import AgentSociety
from agentsociety.storage import AvroConfig, PostgreSQLConfig

from rumor_supervisor import BaselineSupervisor
from rumor_supervisor.envcitizen import TrackTwoEnvCitizen
from rumor_supervisor.rumor_spreader import RumorSpreader
from rumor_supervisor.supervisor import SupervisorConfig
from rumor_supervisor.workflows import TRACK_TWO_EXPERIMENT

MY_PARAMS = SupervisorConfig(
  {
    "llm_detection_prompt": "\n请判断以下社交媒体帖子是否包含不实信息或有害谣言。请仅回答'是'或'否'，如果判断为'是'，请简单说明理由。帖子内容：\n\n'${context.current_processing_message}'\n",
    "keyword_detection_keywords": "速速转发,震惊,最新内幕,官方辟谣都不可信",
    "keyword_detection_exclude_words": "可能,也许,测试",
    "keyword_detection_violation_if_keywords_present": true,
    "detection_logic_expression": "1 | 2",
    "delete_post_priority_strategy": "sender_degree_high",
    "persuade_agent_trigger_conditions_expression": "1 | (2 & 3)",
    "persuade_agent_condition_sent_rumor": "1",
    "persuade_agent_condition_degree_top_k": 10,
    "persuade_agent_condition_never_persuaded": "3",
    "persuade_agent_content": "请提升分辨能力。",
    "persuade_agent_priority_strategy": "most_violated_this_round",
    "remove_follower_trigger_conditions_expression": "1 & 2 | 3",
    "remove_follower_condition_high_risk_prompt": "\n综合评估智能体 ${context.current_processing_agent_id} (度数: ${context.current_agent_degree}, 历史违规总结: ${context.current_agent_offense_summary}) 的风险。输出1（高风险）或0（低风险）。\n",
    "remove_follower_condition_degree_threshold": 50,
    "remove_follower_condition_traffic_threshold": 5,
    "ban_agent_trigger_conditions_expression": "1 & (2 | 3)",
    "ban_agent_condition_violations_threshold": 10,
    "ban_agent_condition_intervention_threshold": 3,
    "ban_agent_condition_high_risk_prompt": "\n综合评估智能体 ${context.current_processing_agent_id} (度数: ${context.current_agent_degree}, 历史违规总结: ${context.current_agent_offense_summary}, 已被干预次数: ${context.current_agent_intervention_count}) 的封禁风险。输出1（应封禁）或0。\n"
}
)


async def main():
    llm_configs = [
        LLMConfig(
            provider=LLMProviderType.Qwen,
            base_url=None,
            api_key="YOUR_API_KEY",
            model="CHOOSE_YOUR_MODEL",
            semaphore=200,
        ),
        # You can add more LLMConfig here
    ]
    env_config = EnvConfig(
        pgsql=PostgreSQLConfig(
            enabled=False,  # Set to True if you want to visualize the simulation in the web UI. Notice that this will SLOW DOWN the simulation.
            dsn="YOUR_POSTGRESQL_DSN",
            num_workers="auto",
        ),
        mlflow=MlflowConfig(  # Do not need mlflow in this simulation
            enabled=False,
            mlflow_uri="http://localhost:5000",
            username="admin",
            password="admin",
        ),
        avro=AvroConfig(
            enabled=True,
        ),
    )
    map_config = MapConfig(
        file_path="THE_PATH_TO_YOUR_MAP_FILE",
        cache_path="THE_PATH_TO_YOUR_MAP_CACHE_FILE",
    )

    config = Config(
        llm=llm_configs,
        env=env_config,
        map=map_config,
        agents=AgentsConfig(
            citizens=[
                AgentConfig(
                    agent_class=TrackTwoEnvCitizen,
                    memory_from_file="./proiles/population_profiles.json",
                ),
                AgentConfig(
                    agent_class=RumorSpreader,
                    memory_from_file="./proiles/spreader_profile.json",
                ),
            ],
            supervisor=AgentConfig(
                agent_class=BaselineSupervisor,
                memory_from_file="./proiles/supervisor_profile.json",
                params=MY_PARAMS,
            ),
        ),  # type: ignore
        exp=TRACK_TWO_EXPERIMENT,
    )  # type: ignore
    agentsociety = AgentSociety(config, tenant_id="DEMO")
    await agentsociety.init()
    await agentsociety.run()
    try:
        await agentsociety.close()
    except Exception as e:
        pass
    ray.shutdown()


if __name__ == "__main__":
    asyncio.run(main())

```

### 4.4 运行步骤

#### 4.4.1 快速开始

1. **环境准备**
   ```bash
   # 激活虚拟环境
   source .venv/bin/activate  # Linux/macOS
   ```

2. **配置检查**
   ```bash
   
   # 检查文件路径
   ls data/population_profiles.json
   ls data/spreader_profile.json
   ls data/supervisor_profile.json
   ls path/to-your-map.pb
   ```

3. **运行仿真**
   ```bash
   python my_run.py
   ```

#### 4.4.2 运行监控

仿真运行过程中会输出以下信息：
- 智能体行为日志
- 监管接口调用结果
- 阶段进度提示

#### 4.4.3 结果查看

仿真完成后，最终结果将直接输出在终端中。除此以外，细粒度结果文件将保存在指定的输出目录：
```
output/
├── artifacts.json          # 问卷调查结果
```

### 4.5 常见问题与解决方案

#### 4.5.1 依赖问题

**问题**：`agentsociety` 模块找不到
```bash
# 解决方案：确保正确安装依赖
pip install -e .
# 或检查路径配置
export PYTHONPATH="${PYTHONPATH}:path/to/agentsociety"
```

#### 4.5.2 连接问题

**问题**：LLM API调用失败
- 检查API密钥是否有效
- 验证模型名称是否正确
- 确认API配额是否充足

#### 4.5.3 性能问题

**问题**：仿真运行缓慢
- 关闭PostgreSQL可视化功能（`enabled=False`）
- 提供更多的LLM Client

---


## 5. 软件包主要文件清单

### 5.1 rumor_supervisor/ - 核心框架代码

#### 5.1.1 主要模块文件
- [`baseline.py`](./rumor_supervisor/baseline.py) - baseline监管智能体实现，提供标准的检测-干预工作流程置
- [`workflow.py`](./rumor_supervisor/workflows.py) - 定义了模拟所需的工作流以及必要的功能函数
- [`sharing_params.py`](./rumor_supervisor/supervisor/sharing_params.py) - 共享参数配置类，定义智能体间的通信和协作参数
- [`survey.py`](./rumor_supervisor/survey.py) - 问卷调查模块，实现谣言传播效果评估功能

#### 5.1.2 supervisor/ - 监管智能体框架
- [`supervisor.py`](./rumor_supervisor/supervisor/supervisor_base.py) - 监管智能体基类定义，提供智能体的基础接口和方法

##### 5.1.2.1 sensing_api.py - 智能体工具集
- [`sensing_api.py`](./rumor_supervisor/supervisor/sensing_api.py) - 感知工具实现，提供环境信息获取和智能体状态查询功能

### 5.2 profiles/ - 智能体档案数据

- [`population_profiles.json`](./profiles/population_profiles.json) - 市民智能体档案
- [`spreader_profile.json`](./profiles/spreader_profile.json) - 谣言传播者智能体档案
- [`supervisor_profile.json`](./profiles/supervisor_profile.json) - 监管智能体档案

### 5.3 example/ - 运行示例

- [`main.py`](./example/main.py) - 主要运行示例，展示完整的仿真配置和启动流程

---

## 6. 提交方式

参赛选手需提交一个包含所设计智能体的xxx.py文件。该文件中仅包含一个继承自Supervisor基类，并实现forward方法的智能体类。示例提交如下：

```python
import random

from rumor_supervisor.supervisor import BDSC2025SupervisorBase


class MySupervisor(BDSC2025SupervisorBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def interventions(self):
        # 实现监管者的功能
        posts = self.sensing_api.get_posts_current_round()
        # 实现监管者的功能
        agent_id = posts[0]["sender_id"]
        # 接口调用例
        posts_received = self.sensing_api.get_all_posts_received_by_agent(agent_id)
        posts_sent = self.sensing_api.get_all_posts_sent_by_agent(agent_id)
        posts_received_last_k_rounds = (
            self.sensing_api.get_posts_received_by_agent_last_k_rounds(agent_id, 10)
        )
        posts_sent_last_k_rounds = (
            self.sensing_api.get_posts_sent_by_agent_last_k_rounds(agent_id, 10)
        )
        posts_received_current_round = (
            self.sensing_api.get_posts_received_by_agent_current_round(agent_id)
        )
        posts_sent_current_round = (
            self.sensing_api.get_posts_sent_by_agent_current_round(agent_id)
        )
        # 随机删除5个帖子
        for post in random.sample(posts, 5):
            self.delete_post_intervention(post["post_id"])
        # 随机劝说1个智能体
        agent_ids = [p["sender_id"] for p in posts]
        agent_id = random.choice(agent_ids)
        self.persuade_agent_intervention(agent_id, "请注意文明用语，不要发布不当言论。")
        # 随机移除1个智能体的1个关注
        follower_ids = self.sensing_api.get_following(agent_id)
        if len(follower_ids) > 0:
            follower_id = random.choice(follower_ids)
            self.remove_follower_intervention(follower_id, agent_id)
        # 随机封禁1个智能体
        agent_ids = [p["sender_id"] for p in posts]
        agent_id = random.choice(agent_ids)
        self.ban_agent_intervention(agent_id)

```

具体请参考example/submission_examples_code文件夹下的示例提交
