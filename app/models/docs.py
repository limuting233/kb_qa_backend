from sqlalchemy import String, BIGINT
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Document(Base):
    __tablename__ = 'documents'

    # 文档标题
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True, comment="文档标题")
    # 文档类型：1-txt 2-markdown 3-word 4-pdf 5-excel 6-ppt 7-image 8-other
    type: Mapped[int] = mapped_column(BIGINT, nullable=False, index=True, comment="文档类型")
    # 文档URL
    url: Mapped[str] = mapped_column(String(255), nullable=False, comment="文档URL")
    # 文档所属用户ID（外键）
    user_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True, comment="文档所属用户ID")
    # 文档大小,单位为字节（byte,B）
    size: Mapped[int] = mapped_column(BIGINT, nullable=False, comment="文档大小,单位为字节（byte,B）")
    # 文档状态：1-已上传 2-已解析 3-索引中 4-完成 5-失败
    status: Mapped[int] = mapped_column(BIGINT, nullable=False, index=True, comment="文档状态")
    # 文档所属知识库ID（外键）
    knowledge_base_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True, comment="文档所属知识库ID")
    # 文档SHA256值
    sha256: Mapped[str] = mapped_column(String(64), nullable=False, index=True, comment="文档SHA256值")
