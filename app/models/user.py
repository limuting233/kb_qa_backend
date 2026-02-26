from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class User(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(20), index=True, unique=True, nullable=False, comment="用户名")
    password: Mapped[str] = mapped_column(String(255), nullable=False, comment="密码")
    phone: Mapped[str | None] = mapped_column(String(11), nullable=True, default=None, comment="手机号")
    email: Mapped[str | None] = mapped_column(String(255), nullable=True, default=None, comment="邮箱")
