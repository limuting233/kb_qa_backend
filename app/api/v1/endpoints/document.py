from typing import List, Annotated

from fastapi import APIRouter, UploadFile, File, Form
# from fastapi.params import Form
from fastapi.responses import JSONResponse

from app.api.deps import DBSessionDep, UserIdDep
# from app.schemas.document import UploadDocsBatchRequest
from app.services.document_service import DocumentService

router = APIRouter()


# document_service = DocumentService()


@router.post("/upload_batch")
async def upload_docs_batch(kb_id: Annotated[str, Form(...)], docs: Annotated[List[UploadFile], File(...)],
                            user_id: UserIdDep,
                            db: DBSessionDep):
    """
    批量上传文档接口
    :param kb_id:
    :param docs:
    :param user_id:
    :param db:
    :return:
    """
    doc_service = DocumentService(db)

    await doc_service.upload_docs_batch(user_id, kb_id, docs)
