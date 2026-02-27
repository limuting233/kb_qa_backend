from pathlib import Path

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.enums import DocumentStatus, DocumentType
from app.core.exceptions import StorageUploadException, BusinessException
from app.infra.storage.oss_client import upload_file_to_aliyun_oss
from app.models.document import Document
from app.repositories.document_repo import DocumentRepo
from app.repositories.knowledge_base_repo import KnowledgeBaseRepo
from app.utils.hash import calculate_uploadfile_sha256
from loguru import logger

_EXT_TO_DOC_TYPE = {
    ".txt": DocumentType.TXT.value,
    ".md": DocumentType.MARKDOWN.value,
    ".markdown": DocumentType.MARKDOWN.value,
    ".doc": DocumentType.WORD.value,
    ".docx": DocumentType.WORD.value,
    ".pdf": DocumentType.PDF.value,
    ".xls": DocumentType.EXCEL.value,
    ".xlsx": DocumentType.EXCEL.value,
    ".ppt": DocumentType.PPT.value,
    ".pptx": DocumentType.PPT.value,
    ".jpg": DocumentType.IMAGE.value,
    ".jpeg": DocumentType.IMAGE.value,
    ".png": DocumentType.IMAGE.value,
    ".gif": DocumentType.IMAGE.value,
    ".webp": DocumentType.IMAGE.value,
}


class DocumentService:
    """

    """

    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = DocumentRepo(db=db)
        self.kb_repo = KnowledgeBaseRepo(db=db)

    async def upload_docs_batch(self, user_id: str, kb_id: str, docs: list[UploadFile]):
        # 判断该kb_id是否存在,并且该kb是否属于这个用户
        kb_existed = await self.kb_repo.get_by_id_and_user_id(kb_id, user_id)
        if not kb_existed:
            logger.error("user_id和kb_id不匹配")
            return None

        uploadeds = []
        failed_uploadeds = []

        seen_sha256 = set()

        for doc in docs:
            # 计算每个前端发过来的文档的sha256值
            sha256 = await calculate_uploadfile_sha256(doc)  # 计算sha256值

            if sha256 in seen_sha256:
                logger.warning(f"批量上传文档接口中存在重复文档[{doc.filename}]")
                continue

            seen_sha256.add(sha256)
            existed = await self.repo.get_by_kb_id_and_sha256(kb_id, sha256)
            if existed:
                # 同一个知识库里面用户重复上传了文档
                logger.warning(f"重复上传文档[{doc.filename}]到知识库[{kb_id}]")
                continue
            # 首次上传该文件，此时需要调用封装好的oss上传方法，将文件上传到阿里云oss
            await doc.seek(0)

            doc_name = doc.filename
            doc_ext = Path(doc_name).suffix.lower()
            storage_key = f"{kb_id}/{sha256}{doc_ext}"

            try:
                upload_file_to_aliyun_oss(doc.file, storage_key)

                uploadeds.append(
                    Document(
                        title=doc_name,
                        type=_EXT_TO_DOC_TYPE.get(doc_ext, DocumentType.OTHER.value),
                        storage_key=storage_key,
                        user_id=user_id,
                        size=doc.size,
                        status=DocumentStatus.DB_CREATED.value,
                        knowledge_base_id=kb_id,
                        sha256=sha256
                    )
                )
            except StorageUploadException as e:
                logger.error(e)
                failed_uploadeds.append(
                    Document(
                        title=doc_name,
                        type=_EXT_TO_DOC_TYPE.get(doc_ext, DocumentType.OTHER.value),
                        storage_key=storage_key,
                        user_id=user_id,
                        size=doc.size,
                        status=DocumentStatus.FAILED.value,
                        knowledge_base_id=kb_id,
                        sha256=sha256
                    )
                )
            except Exception as e:
                logger.exception(f"aliyun oss出错，{str(e)}")

        # 所有文档全部上传好之后，将上传成功的文档入数据库
        await self.repo.add(uploadeds)

        # 更新kb表中doc_count
        updated_kb = await self.kb_repo.update_doc_count(kb_id, len(uploadeds))
        logger.info(f"updated_kb:{updated_kb}")

        await self.db.commit()

        res = {
            "success_cnt": len(uploadeds),
            "failed_cnt": len(failed_uploadeds),
            "repeat_cnt": len(docs) - len(uploadeds) - len(failed_uploadeds),
            "total": len(docs),
            "failed": [d.title for d in failed_uploadeds]
        }
        return res
