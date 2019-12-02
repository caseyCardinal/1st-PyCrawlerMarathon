# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import requests
import json
import time

headers = {'user-agent': 'my-app/0.0.1'}
r = requests.get('https://www.zhihu.com/api/v4/questions/55493026/answers',headers=headers)
if r.status_code == requests.codes.ok:
    print('requests.get OK!')
else:
    print('requests.get FAIL!')
    
response=r.text
data=json.loads(response)

# 回傳幾筆資料 ------------------------------------------------------
idCnt=0
for d in data['data']:
    print(d['id'])
    idCnt+=1
print('資料筆數: '+(idCnt))

d0=data['data'][0]
d0.keys()

# 取出知乎問題發問時間」 -------------------------------------------------
dTm=d0['question']['created']
localtime = time.localtime(dTm)
asciiTm=time.asctime( localtime )
print(asciiTm)

#取出第一筆與最後一筆回答的時間 ----------------------------------------------    
dTm=d0['created_time']
localtime = time.localtime(dTm)
asciiTm=time.asctime( localtime )
print(asciiTm)

dLst=data['data'][(idCnt-1)]
dTm=dLst['created_time']
localtime = time.localtime(dTm)
asciiTm=time.asctime( localtime )
print(asciiTm)




