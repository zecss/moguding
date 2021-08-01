# -*- coding: utf-8 -*-
import re
import requests
import json
import hashlib

#账号信息
user="" #账号
password="" #密码
#签到参数
type="START" #START上班/END下班
device="Android"
latitude="" #纬度
longitude="" #经度
address="" #地址
#其他信息
MD5="3478cbbc33f84bd00d75d7dfa69e0daa" #不用动
UA="Mozilla/5.0 (Linux; U; Android 11; zh-cn; PCKM00 Build/RKQ1.200903.002) AppleWebKit/533.1 (KHTML, like Gecko) Version/5.0 Mobile Safari/533.1"

def getMd5(str):
    hl = hashlib.md5()
    hl.update(str.encode(encoding='utf-8'))
    md5=hl.hexdigest()
    return (md5)

def getPlanId(token,sign):
    data = {
        "state": ""
    }
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'User-Agent': UA,
        'sign': sign,
        'authorization': token,
        'rolekey': 'student'
    }
    url = "https://api.moguding.net:9000/practice/plan/v3/getPlanByStu"
    res = requests.post(url=url, data=json.dumps(data), headers=headers).text
    res = json.loads(res)
    code = res['code']
    if code == 200:
        planId = res['data'][0]['planId']
    return(planId)

#登录账号
def loading():
    url1 = "https://api.moguding.net:9000/session/user/v1/login"
    headers1 = {
        "Content-Type": "application/json; charset=UTF-8",
        "User-Agent": UA,
    }
    data1 = {
        "password": password,
        "phone": user,
        "loginType": "android",
        "uuid": ""
    }
    r = requests.post(url=url1, data=json.dumps(data1), headers=headers1).text
    token = re.findall("token\":\"(.*?)\",\"expiredTime", r)
    userid = re.findall("userId\":\"(.*?)\",\"phone", r)
    code1 = re.findall("code\":(.*?),\"msg", r)
    if code1[0] == "200":
        planid=getPlanId(token[0],getMd5(userid[0]+"student"+MD5))
        sign=getMd5(device+type+planid+userid[0]+address+MD5)
        print("planid: " + planid + "\n" + "sign: " + sign)
        print("登录成功")
        save(token[0],sign,planid)
    else:
        print(r)
        exit()

def save(token,sign,planid):
    url2 = "https://api.moguding.net:9000/attendence/clock/v2/save"
    headers2 = {
        'User-Agent': UA,
        'sign': sign,
        'authorization': token,
        'rolekey': 'student',
        'Content-Type': 'application/json; charset=UTF-8'
    }
    data2 = {
        "address": address,
        "latitude": latitude,
        "description": "",
        "planId": planid,
        "type": type,
        "device": device,
        "longitude": longitude
    }
    r2 = requests.post(url=url2, data=json.dumps(data2), headers=headers2).text
    code2 = re.findall("code\":(.*?),\"msg", r2)
    if code2[0] == "200":
        print("签到成功")
    else:
        print(r2)
    exit()

loading()
