from sqlalchemy import String, BIGINT, SMALLINT, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.core.enums import DocumentType
from app.models.base import Base


class Document(Base):
    """


    """

    __tablename__ = 'documents'

    __table_args__ = (
        UniqueConstraint('knowledge_base_id', 'sha256', name='uq_kb_sha256'),
    )

    # 文档标题
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True, comment="文档标题")
    # 文档类型：1-txt 2-markdown 3-word 4-pdf 5-excel 6-ppt 7-image 8-other
    type: Mapped[int] = mapped_column(SMALLINT, nullable=False, index=True, comment="文档类型")
    # 对象存储键（Object Key）
    storage_key: Mapped[str] = mapped_column(String(255), nullable=False, comment="对象存储键（Object Key）")
    # 文档所属用户ID（外键）
    user_id: Mapped[str] = mapped_column(String(32), nullable=False, index=True, comment="文档所属用户ID")
    # 文档大小,单位为字节（byte,B）
    size: Mapped[int] = mapped_column(BIGINT, nullable=False, comment="文档大小,单位为字节（byte,B）")
    # 文档状态
    status: Mapped[int] = mapped_column(SMALLINT, nullable=False, index=True, comment="文档状态")
    # 文档所属知识库ID（外键）
    knowledge_base_id: Mapped[str] = mapped_column(String(32), nullable=False, index=True, comment="文档所属知识库ID")
    # 文档SHA256值
    sha256: Mapped[str] = mapped_column(String(64), nullable=False, index=True, comment="文档SHA256值")
