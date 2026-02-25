from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db


# 定义异步数据库会话依赖项
DBSessionDep = Annotated[AsyncSession, Depends(get_db)]