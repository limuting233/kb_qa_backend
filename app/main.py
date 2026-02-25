from fastapi import FastAPI

from app.api.v1 import router
from app.core.config import settings


# from app.core import config


def create_app() -> FastAPI:
    """
    创建FastAPI应用实例
    :return: FastAPI应用实例
    """
    app = FastAPI(title=settings.APP_NAME)
    app.include_router(router.api_router, prefix="/api/v1")

    return app


app = create_app()
