from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.enums import KBStatus, KBAvailability
from app.core.exceptions import BizException, KBNotFoundException, KBEmptyException, KBUnavailableException, \
    KBBuildNotAllowedException
from app.models.knowledge_base import KnowledgeBase
from app.repositories.knowledge_base_repo import KnowledgeBaseRepo


class KnowledgeBaseService:

    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = KnowledgeBaseRepo(db=db)

    async def create_kb(self, kb_name: str, user_id: str):
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

    async def build_kb(self, kb_id: str, user_id: str):
        """
        构建知识库。
        :param kb_id: 知识库ID。
        :param user_id: 当前用户 ID。
        :return:
        """

        # 1. 判断该知识库是否存在
        existed = await self.repo.get_by_id_and_user_id(kb_id, user_id)
        if existed is None:
            raise KBNotFoundException(kb_id=kb_id)

        # 2. 判断该知识库是否存在文档
        if existed.doc_count == 0:
            raise KBEmptyException(kb_id=kb_id)

        # 3. 判断该知识库的availability是否为ENABLED
        if existed.availability != KBAvailability.ENABLED.value:
            raise KBUnavailableException(kb_id=kb_id)

        # 4. 判断该知识库的status是否为UNBUILT
        if existed.status != KBStatus.UNBUILT.value:
            raise KBBuildNotAllowedException(kb_id=kb_id)
            # raise BizException(http_status=status.HTTP_400_BAD_REQUEST, code=40003, message=f"知识库状态错误: {kb_id}")

        # 开始构建知识库，使用chroma向量数据库
