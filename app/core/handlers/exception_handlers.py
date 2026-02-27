from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.exceptions import BusinessException
from loguru import logger


def register_exception_handlers(app: FastAPI):
    """
    注册异常处理器
    :param app:
    :return:
    """
    logger.info("正在注册异常处理器 ...")
    app.add_exception_handler(BusinessException, handle_business_exception)
    logger.info("异常处理器注册完成")


def handle_business_exception(request: Request, exception: BusinessException) -> JSONResponse:
    """
    处理业务异常
    :param request:
    :param exception:
    :return:
    """
    logger.error(
        f"[BusinessException处理器] http状态码:{exception.http_status}, 业务状态码:{exception.code}, 错误消息:{exception.message}")

    return JSONResponse(
        status_code=exception.http_status,
        content={
            "code": exception.code,
            "message": "fail",
            "error_message": exception.message,
            "data": exception.data,

        }
    )
