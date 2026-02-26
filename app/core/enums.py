from enum import IntEnum


class DocumentStatus(IntEnum):
    """
    文档状态的枚举类
    """
    UPLOADED = 1  # 后端已接收文档
    STORING = 2  # 上传对象存储中
    STORED = 3  # 原始文档已入对象存储
    DB_CREATED = 4  # 数据库记录已创建
    PROCESSING = 5  # 解析/切片/向量化中
    READY = 6  # 可检索/可问答
    FAILED = 7  # 处理失败


# 文档类型：1-txt 2-markdown 3-word 4-pdf 5-excel 6-ppt 7-image 8-other
class DocumentType(IntEnum):
    """
    文档类型的枚举类
    """
    TXT = 1
    MARKDOWN = 2
    WORD = 3
    PDF = 4
    EXCEL = 5
    PPT = 6
    IMAGE = 7
    OTHER = 8


class KBStatus(IntEnum):
    """
    知识库状态的枚举类
    """

    ACTIVE = 1  # 可用
    BUILDING = 2  # 构建中
    FAILED = 3  # 失败
    DISABLED = 4  # 禁用


class KBVisibility(IntEnum):
    """
    知识库是否面向公众可见的枚举类
    """
    PRIVATE = 1
    SHARED = 2
