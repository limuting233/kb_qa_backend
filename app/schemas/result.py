from typing import TypeVar, Generic, Literal

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")


class Result(BaseModel, Generic[T]):
    model_config = ConfigDict(extra="forbid")

    code: int
    message: Literal["success", "fail"]
    error_message: str | None = Field(default=None)
    data: T | None = Field(default=None)

    @classmethod
    def success(cls, data: T | None = None) -> "Result[T]":
        return cls(code=200, message="success", error_message=None, data=data, )

    @classmethod
    def fail(cls, code: int, error_message: str) -> "Result[T]":
        return cls(code=code, message="fail", error_message=error_message, data=None, )
