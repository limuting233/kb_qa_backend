from typing import Any
from fastapi import status


class BizException(Exception):
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


class KBNotFoundException(BizException):
    """
    知识库不存在异常
    """
    def __init__(self, kb_id: str):
        super().__init__(http_status=status.HTTP_404_NOT_FOUND, code=40401, message=f"知识库不存在: {kb_id}")

class KBEmptyException(BizException):
    """
    知识库为空异常
    """
    def __init__(self, kb_id: str):
        super().__init__(http_status=status.HTTP_400_BAD_REQUEST, code=40001, message=f"知识库为空: {kb_id}")


class KBUnavailableException(BizException):
    """
    知识库不可用异常
    """
    def __init__(self, kb_id: str):
        super().__init__(http_status=status.HTTP_400_BAD_REQUEST, code=40002, message=f"知识库不可用: {kb_id}")

class KBBuildNotAllowedException(BizException):
    """
    知识库构建不允许异常
    """
    def __init__(self, kb_id: str):
        super().__init__(http_status=status.HTTP_400_BAD_REQUEST, code=40003, message=f"知识库构建不允许: {kb_id}")


class StorageUploadException(Exception):
    pass
