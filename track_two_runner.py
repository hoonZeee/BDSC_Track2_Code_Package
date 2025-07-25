import argparse
import asyncio
import importlib.util
import json
import os
from typing import Optional

import ray
import yaml
from agentsociety.configs import (AgentConfig, AgentsConfig, Config, EnvConfig,
                                  LLMConfig, MapConfig)
from agentsociety.simulation import AgentSociety
from agentsociety.storage import DatabaseConfig

from rumor_supervisor import (TRACK_TWO_EXPERIMENT, BaselineSupervisor,
                              RumorSpreader, TrackTwoEnvCitizen)


def load_agent_from_file(file_path: str) -> type:
    # 获取文件名（不含扩展名）作为模块名
    module_name = os.path.splitext(os.path.basename(file_path))[0]

    # 动态加载模块
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)  # type: ignore
    spec.loader.exec_module(module)  # type: ignore

    # 查找并返回自定义监管智能体
    for item_name in dir(module):
        item = getattr(module, item_name)
        if isinstance(item, type) and "BDSC2025SupervisorBase" in str(item.__bases__):
            return item
    raise ValueError(f"在文件 {file_path} 中未找到 BDSC2025SupervisorBase 子类")


def load_params_from_file(file_path: str) -> type:
    with open(file_path, "r", encoding="utf-8") as file:
        params = json.load(file)
    return params


def load_config_from_yaml(config_path: str):
    """
    Loads configuration from YAML file and returns llm_configs, env_config, and map_config.
    - **Description**:
        - Reads YAML configuration file and creates the required configuration objects.

    - **Args**:
        - `config_path` (str): The path to the YAML configuration file.

    - **Returns**:
        - `tuple`: A tuple containing (llm_configs, env_config, map_config).
    """
    with open(config_path, "r", encoding="utf-8") as file:
        config_data = yaml.safe_load(file)

    # Create LLM configurations
    llm_configs = []
    for llm_data in config_data.get("llm_configs", []):
        llm_config = LLMConfig(**llm_data)
        llm_configs.append(llm_config)

    # Create environment configuration
    env_data = config_data.get("env_config", {})
    env_config = EnvConfig(
        db=DatabaseConfig(
            enabled=True,
            db_type="sqlite",
            pg_dsn=None,
        ),
    )

    # Create map configuration
    map_data = config_data.get("map_config", {})
    map_config = MapConfig(**map_data)

    return llm_configs, env_config, map_config


async def process_agent(
    supervisor_class: type,
    llm_configs: list[LLMConfig],
    env_config: EnvConfig,
    map_config: MapConfig,
    citizen_profile_path: str,
    rumor_spreader_profile_path: str,
    supervisor_profile_path: str,
):
    config = Config(
        llm=llm_configs,
        env=env_config,
        map=map_config,
        agents=AgentsConfig(
            citizens=[
                AgentConfig(
                    agent_class=TrackTwoEnvCitizen,
                    memory_from_file=citizen_profile_path,  # change this to the path to the profile file
                ),
                AgentConfig(
                    agent_class=RumorSpreader,  # change this to the class of your design, FOR CODE DESIGNERS
                    memory_from_file=rumor_spreader_profile_path,
                ),
            ],
            supervisor=AgentConfig(
                agent_class=supervisor_class,
                memory_from_file=supervisor_profile_path,
            ),
        ),  # type: ignore
        exp=TRACK_TWO_EXPERIMENT,
    )
    agentsociety = AgentSociety(config, tenant_id="TRACK_TWO")
    await agentsociety.init()
    try:
        await agentsociety.run()
    except Exception as e:
        print(f"Error: {e}")
        return

    # ================================
    # Results
    # ================================
    survey_score = agentsociety.context["final_score"]["average"]
    # TODO: Kafka
    try:
        await agentsociety.close()
    except Exception as e:
        pass
    ray.shutdown()


async def process_params(
    params: dict,
    llm_configs: list[LLMConfig],
    env_config: EnvConfig,
    map_config: MapConfig,
    citizen_profile_path: str,
    rumor_spreader_profile_path: str,
    supervisor_profile_path: str,
):
    config = Config(
        llm=llm_configs,
        env=env_config,
        map=map_config,
        agents=AgentsConfig(
            citizens=[
                AgentConfig(
                    agent_class=TrackTwoEnvCitizen,
                    memory_from_file=citizen_profile_path,  # change this to the path to the profile file
                ),
                AgentConfig(
                    agent_class=RumorSpreader,  # change this to the class of your design, FOR CODE DESIGNERS
                    memory_from_file=rumor_spreader_profile_path,
                ),
            ],
            supervisor=AgentConfig(
                agent_class=BaselineSupervisor,
                memory_from_file=supervisor_profile_path,
                agent_params=params,
            ),
        ),  # type: ignore
        exp=TRACK_TWO_EXPERIMENT,
    )
    agentsociety = AgentSociety(config, tenant_id="TRACK_TWO")
    await agentsociety.init()
    try:
        await agentsociety.run()
    except Exception as e:
        print(f"Error: {e}")
        return

    # ================================
    # Results
    # ================================
    survey_score = agentsociety.context["final_score"]["average"]
    print(f"Survey score: {survey_score}")
    # TODO: Kafka
    try:
        await agentsociety.close()
    except Exception as e:
        pass
    ray.shutdown()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run agent simulation with a specific Python file"
    )

    # Create mutually exclusive group
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-f",
        "--file",
        type=str,
        help="Path to the Python file containing the supervisor class",
    )
    group.add_argument(
        "-p",
        "--param",
        type=str,
        help="Path to the parameter file containing the supervisor parameters",
    )

    # Add optional config argument
    parser.add_argument(
        "--citizens_profile",
        required=True,
        type=str,
        help="Path to the citizens profile file",
    )
    parser.add_argument(
        "--rumor_spreader_profile",
        required=True,
        type=str,
        help="Path to the rumor spreader profile file",
    )
    parser.add_argument(
        "--supervisor_profile",
        required=True,
        type=str,
        help="Path to the supervisor profile file",
    )
    parser.add_argument(
        "--config",
        required=True,
        type=str,
        help="Path to the YAML configuration file for environment settings",
    )

    args = parser.parse_args()

    # Load configurations from YAML file if provided
    llm_configs, env_config, map_config = None, None, None
    if args.config:
        if not os.path.exists(args.config):
            raise FileNotFoundError(f"配置文件未找到: {args.config}")

        if not args.config.endswith((".yaml", ".yml")):
            raise ValueError(f"配置文件必须是 YAML 文件 (.yaml 或 .yml): {args.config}")

        llm_configs, env_config, map_config = load_config_from_yaml(args.config)

    # Process based on main argument
    if args.file:
        if not os.path.exists(args.file):
            raise FileNotFoundError(f"文件未找到: {args.file}")

        if not args.file.endswith(".py"):
            raise ValueError(f"文件必须是 Python 文件 (.py): {args.file}")

        # Process the single file with configs (default or from --config)
        supervisor_class = load_agent_from_file(args.file)
        asyncio.run(
            process_agent(
                supervisor_class=supervisor_class,
                llm_configs=llm_configs,  # type: ignore
                env_config=env_config,  # type: ignore
                map_config=map_config,  # type: ignore
                citizen_profile_path=args.citizens_profile,
                rumor_spreader_profile_path=args.rumor_spreader_profile,
                supervisor_profile_path=args.supervisor_profile,
            )
        )
    elif args.param:
        if not os.path.exists(args.param):
            raise FileNotFoundError(f"参数文件未找到: {args.param}")

        if not args.param.endswith(".json"):
            raise ValueError(f"参数文件必须是 JSON 文件 (.json): {args.param}")

        params = load_params_from_file(args.param)
        asyncio.run(
            process_params(
                params,  # type: ignore
                llm_configs,  # type: ignore
                env_config,  # type: ignore
                map_config,  # type: ignore
                args.citizens_profile,
                args.rumor_spreader_profile,
                args.supervisor_profile,
            )
        )
