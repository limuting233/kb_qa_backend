from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db

# 定义异步数据库会话依赖项
DBSessionDep = Annotated[AsyncSession, Depends(get_db)]


async def get_current_user_id() -> str:
    return "945b719ce7cb4033a147317ec85bafd2"  # TODO: 后续改成从 cookie/redis/token 解析


UserIdDep = Annotated[str, Depends(get_current_user_id)]
