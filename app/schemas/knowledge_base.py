from typing import Any, Self

from pydantic import BaseModel, Field, ConfigDict


class CreateKBRequest(BaseModel):
    """
    创建知识库接口请求模型
    """
    model_config = ConfigDict(extra="forbid")
    name: str = Field(..., min_length=1, max_length=64, description="知识库名称")
