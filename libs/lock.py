# _*_ coding:UTF-8 _*_
# 开发人员: 理想国真恵玩-张大鹏
# 开发团队: 理想国真恵玩
# 开发时间: 2019-07-17 14:28
# 文件名称: lock.py
# 开发工具: PyCharm

# 封装加密的功能
import hashlib


def get_sha256(string):
    sha256 = hashlib.sha256(bytes('加一些东西', encoding='utf8') + b'lxgzhw')
    sha256.update(bytes(string, encoding='utf8'))
    password = sha256.hexdigest()
    return password
