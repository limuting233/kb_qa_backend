from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.knowledge_base import KnowledgeBase


class KnowledgeBaseRepo:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_user_id_and_name(self, user_id: str, kb_name: str) -> KnowledgeBase | None:
        """
        根据用户id和知识库名称查询知识库信息
        :param user_id: 用户id
        :param kb_name: 知识库名称
        :return: KnowledgeBase | None
        """

        # 构建sqlalchemy查询语句
        stmt = (
            select(KnowledgeBase)
            .where(
                KnowledgeBase.user_id == user_id,
                KnowledgeBase.name == kb_name,
                KnowledgeBase.deleted_at.is_(None),
            )
            .limit(1)
        )
        # 执行查询
        res = await self.db.execute(stmt)
        # 返回结果
        return res.scalar_one_or_none()

    async def add(self, kb: KnowledgeBase) -> KnowledgeBase:
        """
        新增一条kb记录
        :param kb: 要插入的记录
        :return: 新增后的记录
        """
        self.db.add(kb)
        await self.db.flush()
        await self.db.refresh(kb)
        return kb
