from dotenv import load_dotenv
from fastapi import FastAPI

from app.api.v1 import router
from app.core.config import settings
from app.core.handlers.exception_handlers import register_exception_handlers
from app.core.logging import setup_logging
from app.infra.storage.oss_client import create_aliyun_oss_client
from loguru import logger


def create_app() -> FastAPI:
    """
    创建FastAPI应用实例
    :return: FastAPI应用实例
    """
    app = FastAPI(title=settings.APP_NAME)
    app.include_router(router.api_router, prefix="/api/v1")

    load_dotenv(dotenv_path=settings.PROJECT_ROOT / f".env.{settings.ENV}", override=True)

    setup_logging()
    register_exception_handlers(app)

    create_aliyun_oss_client()  # 创建oss客户端

    return app


app = create_app()
