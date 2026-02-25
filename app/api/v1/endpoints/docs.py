from fastapi import APIRouter

from app.api.deps import DBSessionDep

router = APIRouter()


@router.post("/upload_batch")
async def upload_docs_batch(db: DBSessionDep):
    """
    上传批量文档接口
    :return:
    """
