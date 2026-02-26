import argparse
import requests
import alibabacloud_oss_v2 as oss
from alibabacloud_oss_v2 import Client
from dotenv import load_dotenv

from app.core.config import settings

client: Client | None = None


def create_aliyun_oss_client():
    global client
    if client:
        return None

    # load_dotenv(dotenv_path=settings.PROJECT_ROOT / f".env.{settings.ENV}", override=True)

    # 从环境变量中加载凭证信息，用于身份验证
    credentials_provider = oss.credentials.EnvironmentVariableCredentialsProvider()

    # 加载SDK的默认配置，并设置凭证提供者
    cfg = oss.config.load_default()
    cfg.credentials_provider = credentials_provider

    cfg.region = settings.REGION
    cfg.endpoint = f"oss-{settings.REGION}.aliyuncs.com"

    # 使用配置好的信息创建OSS客户端
    client = oss.Client(cfg)
    # return None


def upload_file_to_aliyun_oss(file, key:str):
    # 执行上传对象的请求，指定存储空间名称、对象名称和数据内容
    global client
    if client is None:
        create_aliyun_oss_client()

    result = client.put_object(oss.PutObjectRequest(
        bucket=settings.BUCKET,
        key=key,
        body=file,
    ))

    # 输出请求的结果状态码、请求ID、内容MD5、ETag、CRC64校验码和版本ID，用于检查请求是否成功
    print(f'status code: {result.status_code},'
          f' request id: {result.request_id},'
          f' content md5: {result.content_md5},'
          f' etag: {result.etag},'
          f' hash crc64: {result.hash_crc64},'
          f' version id: {result.version_id},'
          )
