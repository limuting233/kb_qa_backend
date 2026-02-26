import uuid
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# _CN_TZ = ZoneInfo("Asia/Shanghai")


class Base(DeclarativeBase):
    """
    基础模型类，所有其他模型类都应继承自该类。
    """

    __abstract__ = True

    # 主键：UUID字符串
    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=lambda: uuid.uuid4().hex, comment="主键")

    # 创建时间：插入时由数据库自动写入
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False,
                                                 default=lambda: datetime.now(timezone.utc), comment="创建时间")

    # 更新时间：插入时写入，更新时自动刷新
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False,
                                                 default=lambda: datetime.now(timezone.utc),
                                                 onupdate=lambda: datetime.now(timezone.utc), comment="更新时间")

    # 软删除时间：未删除为 NULL，删除时写入时间
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, default=None,
                                                        index=True, comment="软删除时间")
