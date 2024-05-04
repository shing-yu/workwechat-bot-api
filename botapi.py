from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
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
    touid: str = "@all"


class Image(BaseModel):
    token: str
    image_base64: str
    touid: str = "@all"


@app.post("/sendmessage")
async def send_message(message: Message):
    if message.token != token:
        raise HTTPException(status_code=403, detail="Token错误")
    touid = message.touid
    response = wec.send_message(message.content, enterprise_id, application_id, application_secret, touid)
    if response:
        # return {"client_status": "success", **response}
        return response
    else:
        raise HTTPException(status_code=500, detail="发送失败，请查看控制台输出")


@app.post("/sendimage")
async def send_image(image: Image):
    if image.token != token:
        raise HTTPException(status_code=403, detail="Token错误")
    touid = image.touid
    # 移除Base64编码中的前缀
    if image.image_base64.startswith("data:image/jpeg;base64,"):
        image.image_base64 = image.image_base64.replace("data:image/jpeg;base64,", "")
    elif image.image_base64.startswith("data:image/png;base64,"):
        image.image_base64 = image.image_base64.replace("data:image/png;base64,", "")
    response = wec.send_image(image.image_base64, enterprise_id, application_id, application_secret, touid)
    if response:
        # return {"client_status": "success", **response}
        return response
    else:
        raise HTTPException(status_code=500, detail="发送失败，请检查Base64编码格式是否正确或查看控制台输出")


@app.post("/sendmarkdown")
async def send_markdown(message: Message):
    if message.token != token:
        raise HTTPException(status_code=403, detail="Token错误")
    touid = message.touid
    response = wec.send_markdown(message.content, enterprise_id, application_id, application_secret, touid)
    if response:
        # return {"client_status": "success", **response}
        return response
    else:
        raise HTTPException(status_code=500, detail="发送失败，请查看控制台输出")


# 域名验证相关
@app.get("/{file_name}")
async def root(file_name: str):
    file_path = os.path.join(os.getcwd(), "files", file_name)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        raise HTTPException(status_code=404, detail="路径不存在")


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=2333)
