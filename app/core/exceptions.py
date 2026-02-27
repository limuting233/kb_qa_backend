from typing import Any


class BusinessException(Exception):
    """
    基础业务异常类
    """

    def __init__(self, http_status: int, code: int, message: str, data: Any | None = None):
        self.http_status = http_status
        self.code = code
        self.message = message
        self.data = data
        # 让 Exception 自己也带 message，方便日志里看到
        super().__init__(message)


class StorageUploadException(Exception):
    pass