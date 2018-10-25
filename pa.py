#-*-coding:utf-8-*- #编码声明，不要忘记！
import requests  #这里使用requests，小脚本用它最合适！
from lxml import html    #这里我们用lxml，也就是xpath的方法
import json
import numpy as np
xItemList=[]
with open('itemInfo.json',"r",encoding='utf-8') as fjson:
    y = json.load(fjson)   
    xItemList = np.array(y['items'])    
    fjson.close()


def getSearchMode(text):
    if False:
        f = open("search.html","w",encoding='utf-8')
        f.write(text)
        f.close()
    tree = html.fromstring(text)
    x = tree.xpath('//*[@id="web-content"]/div/div[1]/div/div[3]/div/div/div[2]/div[1]/a/@href')
    return x[0]

def getContent(text):
    #对获取到的page格式化操作，方便后面用XPath来解析
    if True:
        f = open("111.html","w",encoding='utf-8')
        f.write(text)
        f.close()
    #print(text)
    tree = html.fromstring(text)
    for a in xItemList:
        if len(a['xpath']) <2:continue
        a['value'] = tree.xpath(a['xpath'])        
        print(f"{a['title']} \t>>>\t {a['value']}")

   
   


def getContentbyURL(url,raw_cookies):
    cookie = {}     
    for line in raw_cookies.split(';'):    
        if len(line)<2:continue
        key,value = line.split("=", 1)
        cookie[key] = value #一些格式化操作，用来装载cookies

    #重点来了！用requests，装载cookies，请求网站
    page = requests.get(url,cookies=cookie)

    #print(page.text)
    getContent(page.text)

def testGetContent():
    htmlArr=["深商科技.html","mafengwo.html"]
    for a in htmlArr:
        print("----"*20)
        with open(a,"r",encoding='utf-8') as f:
            text = f.read()
            getContent(text)
            f.close()

def testGetSearch():
    with open('search.html','r',encoding='utf-8') as f:
        getSearchMode(f.read())


if __name__ == "__main__":
    raw_cookies = ''#引号里面是你的cookie，用之前讲的抓包工具来获得
    raw_cookies='BAIDUID=03D092E5EE025A3FDBED7117A060E281:FG=1;BIDUPSID=03D092E5EE025A3FDBED7117A060E281;PSTM=1540264574;HMACCOUNT=7ACA8249760B55A2;BD_UPN=12314753;TYCID=e136a230d67211e8a0e2d57a3724c6fe;undefined=e136a230d67211e8a0e2d57a3724c6fe;ssuid=7594491667;_ga=GA1.2.1427534363.1540264953;_gid=GA1.2.1598589380.1540264953;_gat_gtag_UA_123487620_1=1;Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1540264696,1540264914,1540264953,1540265017;aliyungf_tc=AQAAAIx9KABa/AMAg/nT3leXYZrCe7xV;csrfToken=cjcWC8O7_qL4_DQK4EvcYUgl;HMVT=e92c8d65d92d534b0fc290df538b4758|1540265017|;Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1540265017;'
    #getContentbyURL('https://www.tianyancha.com/company/21475430',raw_cookies)
    testGetSearch()
    
