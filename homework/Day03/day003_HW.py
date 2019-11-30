# -*- coding: utf-8 -*-
# check path data existed? --------------------------------------------
#
import os
import os.path
import xmltodict
import json

if not os.path.isfile("sample.xml"):
    print("sample.xml not existed!!")
    os._exit(1)
    
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

# read xml file -------------------------------------------------------
#
try:
    tree = ET.parse('sample.xml')
    root = tree.getroot()
    
# location numbers ----------------------------------------------------
    cnt=0
    for child in root.iter():
        if(child.tag.count('locationName')>0):
            print(child.tag, child.text)
            cnt=cnt+1
            
    print('地區總數: '+str(cnt))
    
# 1st temp start time, degree for each location -----------------------
    for child in root.iter('{urn:cwb:gov:tw:cwbcommon:0.1}location'):
        print(child[0].text)
        weather=child[4]
        elemText=weather[0].text
        strtTm=weather[2][0].text
        temp=weather[2][1][0].text
        tempUnt=weather[2][1][1].text
        if(elemText=='T'):
            print('1st Time='+strtTm, ' Temp.='+temp+' '+tempUnt)
    
# all temp start time, degree for 1st  location -----------------------
    for child in root.iter('{urn:cwb:gov:tw:cwbcommon:0.1}location'):
        print(child[0].text)
        for childWthr in child.iter('{urn:cwb:gov:tw:cwbcommon:0.1}time'):
            unt=childWthr[1][1].text
            if unt=='攝氏度':
                print(childWthr[0].text, ' Temp.=', childWthr[1][0].text, ' ',  unt)
        break
    
    del tree
    
except FileNotFoundError:
     print("sample.xml 檔案不存在。")
except IsADirectoryError:
  print("目錄 only")

