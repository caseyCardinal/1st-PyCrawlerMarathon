# -*- coding: utf-8 -*-
# check path data existed? --------------------------------------------
#
import os
import os.path
import csv
import json

if not os.path.isfile("example.csv"):
    print("example.csv not existed!!")
    os._exit(1)

# read csv file -------------------------------------------------------
#
try:
    shft1tm=[]
    shft15tm=[]
    with open("example.csv", 'r', encoding="utf-8") as fin:
        csvReader=csv.reader(fin, delimiter=',')
        hdr=next(csvReader)
        for row in csvReader:
            #print(row)
            shft1tm.append(row[5])
            shft15tm.append(row[5:10])

    json=json.dumps(shft1tm)
    #json15=json.dumps(shft15tm)
    print(json)       
    fin.close()

except FileNotFoundError:
     print("example.txt 檔案不存在。")
except IsADirectoryError:
  print("目錄 only")

