from pathlib import Path

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.infra.storage.oss_client import upload_file_to_aliyun_oss
from app.repositories.document_repo import DocumentRepo
from app.utils.hash import calculate_uploadfile_sha256


class DocumentService:
    """

    """

    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = DocumentRepo(db=db)

    async def upload_docs_batch(self, user_id: str, kb_id: str, docs: list[UploadFile]):
        # 计算每个前端发过来的文档的sha256值
        for doc in docs:
            sha256 = await calculate_uploadfile_sha256(doc)
            existed = await self.repo.get_by_kb_id_and_sha256(kb_id, sha256)
            if existed:
                # 同一个知识库里面用户重复上传了文档
                continue
            # 首次上传该文件，此时需要调用封装好的oss上传方法，将文件上传到阿里云oss
            await doc.seek(0)
            doc_name = doc.filename
            doc_ext = Path(doc_name).suffix.lower()
            upload_file_to_aliyun_oss(doc.file, f"{kb_id}/{sha256}{doc_ext}")
