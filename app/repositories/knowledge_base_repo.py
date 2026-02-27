from sqlalchemy import select, update, func
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

    async def add(self, kb: KnowledgeBase):
        """
        新增一条kb记录
        :param kb: 要插入的记录
        :return: 新增后的记录
        """
        if not kb:
            return None
        self.db.add(kb)
        await self.db.flush()
        # await self.db.refresh(kb)
        # return kb

    async def get_by_id_and_user_id(self, kb_id: str, user_id: str) -> KnowledgeBase | None:
        stmt = (
            select(KnowledgeBase).where(
                KnowledgeBase.id == kb_id,
                KnowledgeBase.user_id == user_id,
                KnowledgeBase.deleted_at.is_(None),
            )
        )
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()

    async def update_doc_count(self, kb_id: str, delta: int) -> KnowledgeBase | None:
        """
        更新知识库文档计数（可增可减，最小为 0）
        :param kb_id: 知识库ID
        :param delta: 变化量，正数增加，负数减少
        :return:
        """
        stmt = (
            update(KnowledgeBase).where(
                KnowledgeBase.id == kb_id,
                KnowledgeBase.deleted_at.is_(None),
            )
            .values(
                doc_count=func.greatest(0, KnowledgeBase.doc_count + delta),
            )
            .returning(KnowledgeBase)
        )
        res = await self.db.execute(stmt)
        await self.db.flush()
        return res.scalar_one_or_none()
