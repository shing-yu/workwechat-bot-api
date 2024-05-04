# workwechat-bot-api
一个基于[wecomchan](https://github.com/easychen/wecomchan)，使用python，fastapi实现的企业微信机器人API接口

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
vim wecombotapi.service  # 替换 /path/to/your/project 为项目文件根目录的绝对路径 
sudo cp wecombotapi.service /etc/systemd/system/wecombotapi.service
sudo systemctl daemon-reload
sudo systemctl start wecombotapi
sudo systemctl enable wecombotapi  # 开机自启
```
