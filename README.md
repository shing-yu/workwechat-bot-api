# workwechat-bot-api
一个基于[wecomchan](https://github.com/easychen/wecomchan)，使用python，fastapi实现的企业微信机器人接口

## 运行方式
1. 安装依赖
```shell
pip install -r requirements.txt
# pip3 install -r requirements.txt
```
2. 运行
```shell
python botapi.py
# python3 botapi.py
# uvicorn botapi:app --reload
```
3. （可选）加入到systemd（Linux）
```shell
vim wwcbotapi.service  # 替换 /path/to/your/project 为项目文件根目录的绝对路径 
sudo cp wwcbotapi.service /etc/systemd/system/botapi.service
sudo systemctl daemon-reload
sudo systemctl start botapi
sudo systemctl enable botapi  # 开机自启
```
