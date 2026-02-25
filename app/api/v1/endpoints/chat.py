from fastapi import APIRouter

router = APIRouter()

@router.post("")
async def chat():
    """
    聊天接口
    :return:流式响应
    """