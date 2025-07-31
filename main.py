import asyncio

import ray
from agentsociety.configs import (AgentConfig, AgentsConfig, Config, EnvConfig,
                                  LLMConfig, MapConfig)
from agentsociety.llm import LLMProviderType
from agentsociety.simulation import AgentSociety
from agentsociety.storage import DatabaseConfig

from llm_supervisor import MySupervisor
# from rumor_supervisor import BaselineSupervisor
from rumor_supervisor.envcitizen import TrackTwoEnvCitizen
from rumor_supervisor.rumor_spreader import RumorSpreader
from rumor_supervisor.supervisor import SupervisorConfig
from rumor_supervisor.workflows import TRACK_TWO_EXPERIMENT

MY_PARAMS = SupervisorConfig(
    # change the parameters here, FOR FRONTEND DESIGNERS
)


async def main():
    llm_configs = [
        LLMConfig(
            provider=LLMProviderType.VLLM,
            base_url="api port", #local port
            api_key="1234",
            model="api model",
            concurrency=200,
            timeout=60,
        ),
        # You can add more LLMConfig here
    ]
    env_config = EnvConfig(
        db=DatabaseConfig(
            enabled=True,
            db_type="sqlite",
            pg_dsn=None,
        ),
    )
    map_config = MapConfig(
        file_path="./map.pb",
    )

    config = Config(
        llm=llm_configs,
        env=env_config,
        map=map_config,
        agents=AgentsConfig(
            citizens=[
                AgentConfig(
                    agent_class=TrackTwoEnvCitizen,
                    memory_from_file="./data/population_profiles.json",
                ),
                AgentConfig(
                    agent_class=RumorSpreader,
                    memory_from_file="./data/spreader_profile.json",
                ),
            ],
            supervisor=AgentConfig(
                agent_class=MySupervisor,
                #agent_class=BaselineSupervisor,
                memory_from_file="./data/supervisor_profile.json",
            ),
        ),  # type: ignore
        exp=TRACK_TWO_EXPERIMENT,
    )  # type: ignore
    agentsociety = AgentSociety(config, tenant_id="DEMO") # 경로 설정 test1으로 해서 데이터 수집
    await agentsociety.init()
    await agentsociety.run()
    try:
        await agentsociety.close()
    except Exception as e:
        pass
    ray.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
