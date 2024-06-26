"""
本文件经过了修改，原始代码来自：easychen/wecomchan
原始代码包含函数：send_message、send_image、send_markdown
新增函数：send_file, send_card
原始代码许可证：
MIT License

Copyright (c) 2021 Easy

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


import json
import requests
import base64


def get_access_token(wecom_cid, wecom_secret):
    # 获取access_token的URL
    get_token_url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={wecom_cid}&corpsecret={wecom_secret}"
    response = requests.get(get_token_url).content
    access_token = json.loads(response).get('access_token')
    return access_token


send_url = "https://qyapi.weixin.qq.com/cgi-bin/message/send"
upload_url = "https://qyapi.weixin.qq.com/cgi-bin/media/upload"


def send_message(text, wecom_cid, wecom_aid, wecom_secret, wecom_touid='@all'):
    try:
        access_token = get_access_token(wecom_cid, wecom_secret)

        if access_token and len(access_token) > 0:
            # 发送消息的参数
            params = {
                "access_token": access_token
            }
            data = {
                "touser": wecom_touid,
                "agentid": wecom_aid,
                "msgtype": "text",
                "text": {
                    "content": text
                },
                "duplicate_check_interval": 10
            }
            response = requests.post(send_url, data=json.dumps(data), params=params).content
            return response
        else:
            return False
    except Exception as e:
        print("发送消息失败：", e)
        return False


def send_image(base64_content, wecom_cid, wecom_aid, wecom_secret, wecom_touid='@all'):
    try:
        access_token = get_access_token(wecom_cid, wecom_secret)

        if access_token and len(access_token) > 0:
            # 上传图片的参数
            # upload_url = f'https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token={access_token}&type=image'
            params = {
                "access_token": access_token,
                "type": "image"
            }
            upload_response = requests.post(upload_url,
                                            files={"picture": base64.b64decode(base64_content)},
                                            params=params).json()

            if "media_id" in upload_response:
                media_id = upload_response['media_id']
            else:
                return False

            # 发送图片消息的参数
            params = {
                "access_token": access_token
            }
            data = {
                "touser": wecom_touid,
                "agentid": wecom_aid,
                "msgtype": "image",
                "image": {
                    "media_id": media_id
                },
                "duplicate_check_interval": 10
            }
            response = requests.post(send_url, data=json.dumps(data), params=params).content
            return response
        else:
            return False
    except Exception as e:
        print("发送图片失败：", e)
        return False


def send_markdown(text, wecom_cid, wecom_aid, wecom_secret, wecom_touid='@all'):
    try:
        access_token = get_access_token(wecom_cid, wecom_secret)

        if access_token and len(access_token) > 0:
            # 发送Markdown消息的参数
            params = {
                "access_token": access_token
            }
            data = {
                "touser": wecom_touid,
                "agentid": wecom_aid,
                "msgtype": "markdown",
                "markdown": {
                    "content": text
                },
                "duplicate_check_interval": 10
            }
            response = requests.post(send_url, data=json.dumps(data), params=params).content
            return response
        else:
            return False
    except Exception as e:
        print("发送Markdown失败：", e)
        return False


def send_file(file, name, wecom_cid, wecom_aid, wecom_secret, wecom_touid='@all'):
    try:
        access_token = get_access_token(wecom_cid, wecom_secret)

        if access_token and len(access_token) > 0:
            # 上传文件的参数
            # upload_url = f'https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token={access_token}&type=file'
            params = {
                "access_token": access_token,
                "type": "file"
            }
            files = {"media": (name, file, 'application/octet-stream')}
            upload_response = requests.post(upload_url, files=files, params=params).json()

            if "media_id" in upload_response:
                media_id = upload_response['media_id']
            else:
                print(upload_response.json())
                return False

            # 发送文件消息的参数
            params = {
                "access_token": access_token
            }
            data = {
                "touser": wecom_touid,
                "agentid": wecom_aid,
                "msgtype": "file",
                "file": {
                    "media_id": media_id
                },
                "duplicate_check_interval": 10
            }
            response = requests.post(send_url, data=json.dumps(data), params=params).content
            return response
        else:
            return False
    except Exception as e:
        print("发送文件失败：", e)
        return False


def send_card(title, description, url, wecom_cid, wecom_aid, wecom_secret, btntxt="详情", wecom_touid='@all'):
    try:
        access_token = get_access_token(wecom_cid, wecom_secret)

        if access_token and len(access_token) > 0:
            # 发送卡片消息的参数
            params = {
                "access_token": access_token
            }
            data = {
                "touser": wecom_touid,
                "agentid": wecom_aid,
                "msgtype": "textcard",
                "textcard": {
                    "title": title,
                    "description": description,
                    "url": url,
                    "btntxt": btntxt
                },
                "duplicate_check_interval": 10
            }
            response = requests.post(send_url, data=json.dumps(data), params=params).content
            return response
        else:
            return False
    except Exception as e:
        print("发送卡片消息失败：", e)
        return False


if __name__ == '__main__':
    enterprise_id = "企业ID"
    application_id = "应用ID"
    application_secret = "应用Secret"
    ret = send_message("推送测试\r\n测试换行", enterprise_id, application_id, application_secret)
    print(ret)
    ret = send_message('<a href="https://www.example.com/">文本中支持超链接</a>',
                       enterprise_id, application_id, application_secret)
    print(ret)
    ret = send_image("此处填写图片Base64", enterprise_id, application_id, application_secret)
    print(ret)
    ret = send_markdown("**Markdown 内容**", enterprise_id, application_id, application_secret)
    print(ret)
    ret = send_file(open("文件路径", "rb"), "test", enterprise_id, application_id, application_secret)
    print(ret)
    ret = send_card("卡片标题", "卡片描述", "https://www.example.com/", enterprise_id, application_id, application_secret)
    print(ret)
