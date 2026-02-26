import os
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


# print(_PROJECT_ROOT)


class Settings(BaseSettings):
    """
    应用配置类
    """

    # 应用配置
    APP_NAME: str
    APP_PORT: int

    PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent.parent  # 项目根目录

    # 目前运行环境
    ENV: str = os.getenv("ENV", "dev")

    # PostgreSQL数据库配置
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    ECHO_SQL: bool
    POOL_SIZE: int
    MAX_OVERFLOW: int
    POOL_TIMEOUT: int
    POOL_RECYCLE: int

    # aliyun oss相关配置
    REGION: str
    BUCKET: str
    OSS_ACCESS_KEY_ID: str
    OSS_ACCESS_KEY_SECRET: str

    model_config = SettingsConfigDict(

        env_file=os.path.join(PROJECT_ROOT, f".env.{ENV}"),  # 环境变量文件绝对路径
        env_file_encoding="utf-8",  # 环境变量文件编码
        env_ignore_empty=True,  # 忽略空值的环境变量
        case_sensitive=True,  # 环境变量名称是否区分大小写,为True时,ENV=dev和env=dev是不同的环境变量
    )

    # class Config:
    #     env = os.getenv("env", "dev")
    #     env_file = os.path.join(_PROJECT_ROOT, f".env.{env}")


settings = Settings()
