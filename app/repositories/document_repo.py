from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.document import Document


class DocumentRepo:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_kb_id_and_sha256(self, kb_id: str, sha256: str) -> Document | None:
        """
        根据知识库id和sha256值查询文档信息
        :param kb_id:
        :param sha256:
        :return:
        """
        stmt = (
            select(Document)
            .where(
                Document.knowledge_base_id == kb_id,
                Document.sha256 == sha256
            )
        )

        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()
