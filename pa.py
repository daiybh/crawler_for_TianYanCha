#-*-coding:utf-8-*- #编码声明，不要忘记！
import requests  #这里使用requests，小脚本用它最合适！
from lxml import html    #这里我们用lxml，也就是xpath的方法
import json
import numpy as np
xItemList=[]
g_debug=False
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
    
    yy = tree.xpath('//*[@id="web-content"]/div/div[1]/div/div[3]/div[1]/div/div[2]/div[2]/div[3]/span/text()')
    
    return x[0],yy[0]

def getContent(text,date):
    #对获取到的page格式化操作，方便后面用XPath来解析
    if False:
        f = open("111.html","w",encoding='utf-8')
        f.write(text)
        f.close()
    #print(text)
    tree = html.fromstring(text)
    #print(tree)
    
    result=''
    for a in xItemList:
        if len(a['title']) <1:
            continue
        if g_debug:
            print(f"{a['title']} \t>>>\t {a['xpath']}")
        if a['title']=='x时间x':
            result +=date
        elif a['title']=='曾用名':
            ff  = tree.xpath("//div[@class='history-content']")
            if len(ff)>0:
                xf = ff[0].xpath('string(.)')
                print(xf)
                result+=xf
            
        if len(a['xpath']) >2:
            try:
                value= tree.xpath(a['xpath'])        
                #a['value'] = value
                #print(a['xpath'])
                #for v in value:
                #    print(v)
                if g_debug:
                    print(f"{a['title']} \t>>>\t {value}")
                #result[a['title']]=a['value']
                for x in value:
                    result+=x+" "
                #if len(value) >0:
                #    result +=value[0] 
            except:
                print(f"{a['title']} \t>>>\t Exception")
        result +=","
    return result

   
   


def getContentbyURL(url,raw_cookies):
    cookie = {}     
    for line in raw_cookies.split(';'):    
        if len(line)<2:continue
        key,value = line.split("=", 1)
        cookie[key] = value #一些格式化操作，用来装载cookies

    #重点来了！用requests，装载cookies，请求网站
    page = requests.get(url,cookies=cookie)

    #print(page.text)
    getContent(page.text,"1923-9-9")

def testGetContentX(htmlUrl):
    print("----"*20)
    with open(htmlUrl,"r",encoding='utf-8') as f:
        text = f.read()
        print(getContent(text,'1892-2-3'))
        f.close()

def testGetContent():
    htmlArr=["大连奥格窗业有限公司.html","深商科技.html","mafengwo.html"]
    htmlArr=['沈阳繁荣金晨标识标牌有限公司.html']
    for a in htmlArr:
        testGetContentX(a)        
def testGetSearch():
    with open('search.html','r',encoding='utf-8') as f:
        getSearchMode(f.read())


if __name__ == "__main__":
    raw_cookies = ''#引号里面是你的cookie，用之前讲的抓包工具来获得
    raw_cookies='BAIDUID=03D092E5EE025A3FDBED7117A060E281:FG=1;BIDUPSID=03D092E5EE025A3FDBED7117A060E281;PSTM=1540264574;HMACCOUNT=7ACA8249760B55A2;BD_UPN=12314753;TYCID=e136a230d67211e8a0e2d57a3724c6fe;undefined=e136a230d67211e8a0e2d57a3724c6fe;ssuid=7594491667;_ga=GA1.2.1427534363.1540264953;_gid=GA1.2.1598589380.1540264953;_gat_gtag_UA_123487620_1=1;Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1540264696,1540264914,1540264953,1540265017;aliyungf_tc=AQAAAIx9KABa/AMAg/nT3leXYZrCe7xV;csrfToken=cjcWC8O7_qL4_DQK4EvcYUgl;HMVT=e92c8d65d92d534b0fc290df538b4758|1540265017|;Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1540265017;'
    #getContentbyURL('https://www.tianyancha.com/company/21475430',raw_cookies)
    #testGetSearch()
    #testGetContent()  
    g_debug = True
    testGetContentX("save.html")
