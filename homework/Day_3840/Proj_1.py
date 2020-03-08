# 打開瀏覽器 -----------------------------------------------------------------------
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import datetime

browser = webdriver.Chrome(executable_path='D:\PythonProjects\Spyder\chromedriver')
browser.get("https://www.cupoy.com/newsfeed/topicgrp/Sports_tw")

# 每隔 x 秒鐘自動往下滑, 資料存檔-----------------------------------------------------------
x=5
cnt=0
brkFlg=0
fo = open("SportCtgry.txt", "w", encoding='UTF-8')
ft = open("SportNews.txt", "w", encoding='UTF-8')
srcLst=[]
contentLst=[]
for i in range(100):
    # 取得資料，丟到 BeautifulSoup 解析 --------------------------------
    html_source = browser.page_source
    soup = BeautifulSoup(html_source, "lxml")
    for d in soup.find_all('div', class_='sc-eEieub sc-iuDHTM ibJqYc'):
        ctgry=d.find('div', class_='sc-gacfCG bPSpUf').text
        news=d.find(class_="sc-erNlkL sc-ekulBa hDLssh").text
        cnt+=1
        print(str(cnt), ctgry, news)
        print(ctgry, file=fo)
        print(news, file=ft)
        if cnt>=500 :
            brkFlg=5
            break

    if brkFlg>0:
        break
    time.sleep(random.randint(3,x))
    browser.execute_script("window.scrollTo(0, 100000);")  
    
# 關閉瀏覽器 -------------------------------------------------------
browser.quit()
fo.close()
ft.close()

# Pandas Dataframe, table -----------------------------------------------------
import pandas as pd

def RtnSource(str1):
    str2=''
    bk=len(str1)-1
    for i in range(len(str1)):
        if(str1[bk]=='｜' or str1[bk]=='-'):
            str2=str1[(bk+1):].strip()
            break
        bk-=1    
    return(str2)
    
# read from file, then create pandas series ------------------
NewsLst=[]
srcLst=[]
ctgryLst=[]

with open("SportCtgry.txt", 'r', encoding='UTF-8') as f:
    lines=f.readlines()
    for data in lines:
        data=data.strip()
        ctgryLst.append(data)
        print(data)
f.close()

with open("SportNews.txt", 'r', encoding='UTF-8') as f:
    lines=f.readlines()
    for data in lines:
        data=data.strip()
        src=RtnSource(data)
        srcLst.append(src)
        NewsLst.append(data)
        print(src, data)
f.close()

# create dataframe from lists --------------------------------
sCtgry=pd.Series(ctgryLst)
s1=pd.Series(srcLst)
s2=pd.Series(NewsLst)

df=pd.concat([sCtgry, s1, s2], axis=1)
head=['category', 'src', 'news']
df.columns=head
df.to_csv('sports.csv', encoding='utf_8_sig')   #must assign utf_8_sig, otherwise it will be un-readable

# bar, pie chart by category list ---------------------------------------------
# delete the duplicated elements in the list ------------------
def delDuplicatedItemsInList(listA):
    return sorted(set(listA), key = listA.index)
    
# counts for each category ------------------------------------
newsCtgry=delDuplicatedItemsInList(ctgryLst)
cntCtgry=[]
for i in range(len(newsCtgry)):
    data=ctgryLst[i]
    cnt=ctgryLst.count(data)
    cntCtgry.append(cnt)

# pie chart ---------------------------------------------------
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

pieS=pd.Series(cntCtgry, index=newsCtgry, name='Pie chart for category')
explode=[]
for i in range(len(newsCtgry)):
    explode.append(0.2)
    
plt.rcParams['font.sans-serif']=['Microsoft JhengHei']
plt.figure(figsize=(10,10))
pieChrt=pieS.plot.pie(explode=explode, labels=newsCtgry, autopct='%1.2f%%')
plt.legend(loc = "upper right")
plt.show()

# bar chart ---------------------------------------------------
plt.figure(figsize=(10,10))
pieChrt=pieS.plot(kind='bar')
plt.legend(loc = "upper right")
plt.show()

# jieba 分析文章字詞 ----------------------------------------------------------------
import jieba
import jieba.analyse

def RtnTitle(str1):
    str2=''
    cnt=str1.count("-")
    if cnt>0:
        idx=str1.find("-")
        str2=str1[0:(idx-1)].strip()
    else:
        str2=str1

    cnt=str2.count("｜")
    if cnt>0:
        idx=str2.find("｜")
        str2=str2[0:(idx-1)].strip()

    cnt=str2.count("|")
    if cnt>0:
        idx=str2.find("|")
        str2=str2[0:(idx-1)].strip()

    return(str2)
    
# generator seq list ------------------------------------------
fw = open("generator.txt", "w", encoding='UTF-8')
with open("SportNews.txt", 'r', encoding='UTF-8') as f:
    lines=f.readlines()
    for data in lines:
        data=RtnTitle(data)
        seg_list = jieba.cut(data, cut_all=False)
        for seg in seg_list:
            print(seg, file=fw)
f.close()
fw.close()
        
new_list=[]
with open("generator.txt", 'r', encoding='UTF-8') as f:
    lines=f.readlines()
    for data in lines:
        data=data.strip()
        new_list.append(data)
f.close()

# delete the stopWords from seq list --------------------------
def remove_stop_words(file_name,seg_list):
    stopWords=[]
    new_list=[]
    with open(file_name, 'r', encoding='UTF-8') as f:
        lines=f.readlines()
        for data in lines:
            data=data.strip()
            stopWords.append(data)
            
    for seg in seg_list:
        if seg not in stopWords:
            new_list.append(seg)
    return new_list
        
def suggest_words(file_name,seg_list):
    #with open("suggest.txt", 'r', encoding='UTF-8') as f:
    with open(file_name, 'r', encoding='UTF-8') as f:
        lines=f.readlines()
        for data in lines:
            data=data.strip()
            jieba.suggest_freq(data, True)
        
seg_list = remove_stop_words('StopWrd.txt',new_list)

# wordcloud -------------------------------------------------------------------
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
import imageio

seg_list=' '.join(seg_list)
font_path = './KAIU.TTF'
wc = WordCloud(background_color='black',font_path=font_path)
wc.generate(seg_list)
plt.imshow(wc)
