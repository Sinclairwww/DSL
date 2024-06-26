# 首先引入RunPy模块
from src import RunPy
import requests

import sqlite3

# 调用getInstance类方法获取全局的runpy实例
runpy = RunPy.getInstance()


# 编写完脚本函数以后，只需要加上runpy.register装饰器并传入你想赋予的
# 脚本名称就可以了，之后便可以使用callpy命令调用
@runpy.register("GetName")
def getname(number):
    conn = sqlite3.connect("data/random_users.db")
    cur = conn.cursor()
    cur = cur.execute("select name from users where number = (?)", (number,))
    res = cur.fetchone()[0]
    conn.close()
    return res


# 获取用户余额
@runpy.register("GetBalance")
def getbalance(number):
    conn = sqlite3.connect("data/random_users.db")
    cur = conn.cursor()
    cur = cur.execute("select balance from users where number = (?)", (number,))
    res = cur.fetchone()[0]
    conn.close()
    return res


# 上传投诉
@runpy.register("UploadComplaint")
def uploadcomplaint(complaint):
    conn = sqlite3.connect("data/complaints.db")
    cur = conn.cursor()
    cur = cur.execute("insert into complaints values (?)", (complaint,))
    conn.commit()
    conn.close()


# 为用户充值
@runpy.register("Topup")
def topup(number):
    conn = sqlite3.connect("data/random_users.db")
    cur = conn.cursor()
    cur = cur.execute("update users set balance = balance + (?)", (int(number),))
    conn.commit()
    conn.close()


# 从wttr.in获取天气信息
@runpy.register("weather")
def weather(loc):
    resp = requests.get("http://wttr.in/{}?format=3".format(loc))
    if resp.status_code == 404:
        return ""
    else:
        return resp.text
