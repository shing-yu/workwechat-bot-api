from typing import TypedDict


class Config(TypedDict):
    enterprise_id: str
    application_id: str
    application_secret: str
    token: str


config: Config = {
    "enterprise_id": "",        # 企业ID
    "application_id": "",       # 应用ID
    "application_secret": "",   # 应用密钥
    "token": "",                # 自定义的token，用于API调用鉴权（可填写任何内容或留空，但调用时必须传递相同的值）
}