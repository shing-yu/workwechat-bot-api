from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from config import config
import wecomchan as wec
import os
import uvicorn

# 从环境变量中获取配置，如果没有则使用config.py中的配置
token = os.getenv("TOKEN", config["token"])
enterprise_id = os.getenv("ENTERPRISE_ID", config["enterprise_id"])
application_id = os.getenv("APPLICATION_ID", config["application_id"])
application_secret = os.getenv("APPLICATION_SECRET", config["application_secret"])
if not enterprise_id or not application_id or not application_secret:
    raise ValueError("企业ID、应用ID和应用密钥不能为空；请在环境变量中设置或在config.py中设置。")

app = FastAPI()


class Message(BaseModel):
    token: str
    content: str


class Image(BaseModel):
    token: str
    image_base64: str


@app.post("/send_message")
async def send_message(message: Message):
    if message.token != token:
        raise HTTPException(status_code=403, detail="Token错误")
    response = wec.send_message(message.content, enterprise_id, application_id, application_secret)
    if response:
        # return {"client_status": "success", **response}
        return response
    else:
        raise HTTPException(status_code=500, detail="发送失败，请查看控制台输出")


@app.post("/send_image")
async def send_image(image: Image):
    if image.token != token:
        raise HTTPException(status_code=403, detail="Token错误")
    response = wec.send_image(image.image_base64, enterprise_id, application_id, application_secret)
    if response:
        # return {"client_status": "success", **response}
        return response
    else:
        raise HTTPException(status_code=500, detail="发送失败，请检查Base64编码格式是否正确或查看控制台输出")


@app.post("/send_markdown")
async def send_markdown(message: Message):
    if message.token != token:
        raise HTTPException(status_code=403, detail="Token错误")
    response = wec.send_markdown(message.content, enterprise_id, application_id, application_secret)
    if response:
        # return {"client_status": "success", **response}
        return response
    else:
        raise HTTPException(status_code=500, detail="发送失败，请查看控制台输出")


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=2333)
