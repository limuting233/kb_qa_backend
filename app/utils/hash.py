import hashlib

from fastapi import UploadFile


async def calculate_uploadfile_sha256(file: UploadFile) -> str:
    """
    计算一个文件的sha256值
    :param file:
    :return:
    """
    sha256 = hashlib.sha256()

    chunk = await file.read(1024 * 1024)
    while chunk:
        sha256.update(chunk)
        chunk = await file.read(1024 * 1024)

    await file.seek(0)
    return sha256.hexdigest()
