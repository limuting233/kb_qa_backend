from fastapi import APIRouter
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

router = APIRouter()


@router.post("")
async def chat():
    """
    聊天接口
    :return:流式响应
    """



