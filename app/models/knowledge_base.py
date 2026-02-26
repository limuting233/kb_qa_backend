from sys import prefix
from typing import Any

from sqlalchemy import String, BIGINT, SMALLINT
from sqlalchemy.orm import Mapped, mapped_column

from app.core.enums import KBStatus, KBVisibility
from app.models.base import Base


class KnowledgeBase(Base):
    """

    """

    __tablename__ = "knowledge_bases"

    #
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True, comment="知识库名称")

    user_id: Mapped[str] = mapped_column(String(32), nullable=False, index=True, comment="知识库所属用户的id")  # 外键

    description: Mapped[str | None] = mapped_column(String(1024), nullable=True, default=None, comment="知识库的描述")

    status: Mapped[int] = mapped_column(SMALLINT, nullable=False, index=True, default=KBStatus.ACTIVE.value,
                                        comment="知识库状态")

    visibility: Mapped[int] = mapped_column(SMALLINT, nullable=False, index=True, default=KBVisibility.PRIVATE.value,
                                            comment="知识库的可见性")
    doc_count: Mapped[int] = mapped_column(BIGINT, nullable=False, default=0, comment="文档数量冗余")
    chunk_count: Mapped[int] = mapped_column(BIGINT, nullable=False, default=0, comment="分块数量冗余")

    # embedding_model: Mapped[int] = mapped_column(BIGINT, nullable=False, comment="Embedding模型")

    def as_dict(self) -> dict[str, Any]:
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}
