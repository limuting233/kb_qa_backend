from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.api.deps import DBSessionDep, UserIdDep
from app.models.knowledge_base import KnowledgeBase
from app.schemas.knowledge_base import CreateKBRequest
from app.schemas.result import Result
from app.services.knowledge_base_service import KnowledgeBaseService

router = APIRouter()


@router.post("")
async def create_kb(request: CreateKBRequest, user_id: UserIdDep, db: DBSessionDep):
    """
    创建知识库接口。

    接口流程：
    1. 接收并校验创建知识库请求参数（当前仅包含知识库名称）。
    2. 通过依赖注入获取当前用户 ID（后续可替换为 cookie/redis/token 解析逻辑）。
    3. 调用服务层创建知识库（包含同名校验、入库与事务提交）。
    4. 将 ORM 对象转换为字典并按统一返回结构输出。

    :param request: 创建知识库请求体，类型为 CreateKBRequest，包含知识库基础信息（如 name）。
    :param user_id: 当前登录用户 ID，由 UserIdDep 依赖注入提供。
    :param db: 异步数据库会话，由 DBSessionDep 依赖注入提供。
    :return: 统一响应结构 Result[dict]，data 为新建知识库信息。
    """
    # user_id = "945b719ce7cb4033a147317ec85bafd2"

    # 初始化知识库服务对象，封装业务逻辑。
    kb_service = KnowledgeBaseService(db=db)

    # 创建知识库记录（内部执行参数处理、重复校验、持久化等）。
    await kb_service.create_kb(request.name, user_id)

    # print(kb)

    # ORM 对象转字典，便于统一响应序列化。
    # resp_data = kb.as_dict()

    # print(resp_data)

    # 返回标准成功响应。
    return Result.success()
