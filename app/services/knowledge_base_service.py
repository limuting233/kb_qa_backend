from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from watchfiles import awatch

from app.models.knowledge_base import KnowledgeBase
from app.repositories.knowledge_base_repo import KnowledgeBaseRepo
from app.schemas.knowledge_base import CreateKBRequest


class KnowledgeBaseService:

    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = KnowledgeBaseRepo(db=db)

    async def create_kb(self, kb_name: str, user_id: str) :
        """
        创建知识库。

        处理逻辑：
        1. 按用户 + 知识库名称检查是否已存在（未软删除）。
        2. 不存在则创建新记录并提交事务。
        3. 捕获数据库完整性异常与通用 SQL 异常，统一回滚并抛出业务错误。

        :param kb_name: 知识库名称。
        :param user_id: 当前用户 ID。
        :return: 创建成功后的 KnowledgeBase ORM 对象。
        :raises HTTPException: 当名称重复或数据库操作失败时抛出。
        """
        # kb_name = kb_name.strip()
        # 判断该用户是否创建过同名知识库
        existed = await self.repo.get_by_user_id_and_name(user_id, kb_name)
        if existed is not None:
            raise HTTPException(status_code=400, detail="知识库名称不可重复")

        try:
            kb = KnowledgeBase(name=kb_name, user_id=user_id)
            await self.repo.add(kb)
            await self.db.commit()


        except IntegrityError:
            await self.db.rollback()
            raise HTTPException(status_code=409, detail="数据冲突")
        except SQLAlchemyError:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail="创建知识库失败")
