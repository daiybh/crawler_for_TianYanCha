#-*-coding:utf-8-*- #编码声明，不要忘记！
import sys
import json
 
import time
from PyQt5.QtCore import QUrl,QTimer

from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile

from PyQt5.QtWidgets import QApplication,QListWidgetItem, QWidget, QVBoxLayout, QPushButton,QListWidget

import pa

companyList=[]
with open('company.list') as f:
    while 1:
        line = f.readline()
        if not line:
            break
        companyList.append(line.strip().strip('\t\n'))
#print(companyList)
# 先来个窗口

class Loginwindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setup() 
        self.listResult=[]
        self.searchIdx=0
        try:
            with open('result.csv','r',encoding='utf-8') as f:
                self.searchIdx = len(f.readlines())-1
                print("lines:",self.searchIdx)  
        except:
            pass
        print("ccc",companyList[self.searchIdx])
        print("ccsss",self.searchIdx)

        self.fw = open('result.csv','a',encoding='utf-8')    
        if self.searchIdx==0:
            self.fw.write('序号,公司名称,注册资金,法定代表人,成立时间,经营状态,电话,邮箱,详细地址,统一社会信用代码,纳税人识别号,注册号,组织机构代码,公司类型,所属行业,所属地区,成立时间,曾经用名,企业类型,股东,历史股东,补充电话,备注')
    #        self.fw.write('\n')


        self.setWindowTitle(f"{self.searchIdx}/{len(companyList)}")

    def setup(self):

        self.box = QVBoxLayout(self)                      # 创建一个垂直布局来放控件
        self.btn_get = QPushButton('点击获取cookies')   # 创建一个按钮涌来了点击获取cookie
        self.btn_get.clicked.connect(self.get_cookie)     # 绑定按钮点击事件
        self.btn_search=QPushButton('search')
        self.btn_search.clicked.connect(self.btn_search_onClick)     # 绑定按钮点击事件
        
 
        self.web = MyWebEngineView()                      # 创建浏览器组件对象
        self.web.setFinishCallBack(self.anlyze_finish)
        self.web.resize(800, 600)                         # 设置大小
        #self.web.load(QUrl("https://www.tianyancha.com/login"))  # 打开百度页面来测试
        self.web.load(QUrl("https://www.tianyancha.com/search?key=成都市锦都工业建设投资有限公司"))
        self.box.addWidget(self.btn_get)                  # 将组件放到布局内，先在顶部放一个按钮
        self.box.addWidget(self.btn_search)                  # 将组件放到布局内，先在顶部放一个按钮
        self.box.addWidget(self.web)                      # 再放浏览器
        self.web.show()                                   # 最后让页面显示出来 

    def get_cookie(self):
        #cookie = self.web.get_cookie()
        #print('获取到cookie: ', cookie)       
        with open('save.html','w',encoding='utf-8') as f:
            f.write(self.web.html)
        
    def gotoSearch(self,companyName):
        print(companyName)
        self.web.searchX(QUrl('https://www.tianyancha.com/search?key='+companyName))
        
    def btn_search_onClick(self):
        print("search") 
        #pa.getContent('https://www.tianyancha.com/company/21475430',self.web.get_cookie())
        #self.web.loadX(QUrl('https://www.tianyancha.com/company/21475430'))
        #self.web.loadX(QUrl('https://www.tianyancha.com/company/2807842615'))
        self.onDoSearch()
    
    def onDoSearch(self):
        self.setWindowTitle(f"{self.searchIdx}/{len(companyList)}")
        if self.searchIdx < len(companyList):
            
            time.sleep(self.searchIdx%5+1)
            self.gotoSearch(companyList[self.searchIdx])
        else:
            print("searchOver")

            #aa = json.dumps(self.listResult,ensure_ascii=False)
            #self.fw.write(aa)

    def anlyze_finish(self,pResult):
        #print("anlyze_finish")
        #print(pResult)
        if pResult=='天眼查校验':
            time.sleep(20)
            self.onDoSearch()
            return
        
        self.fw.write("\n"+companyList[self.searchIdx]+",")
        
        if len(pResult) >4: 
            self.fw.write(pResult)
        
            
        #self.listResult.append(pResult)
        self.searchIdx =self.searchIdx+1
        self.onDoSearch()

# 创建自己的浏览器控件，继承自QWebEngineView
class MyWebEngineView(QWebEngineView):
    
    def __init__(self, *args, **kwargs):
        super(MyWebEngineView, self).__init__(*args, **kwargs)
        # 绑定cookie被添加的信号槽
        QWebEngineProfile.defaultProfile().cookieStore().cookieAdded.connect(self.onCookieAdd)
        self.cookies = {}          # 存放cookie字典 
        self.loadFinished.connect(self._loadFinished)
        self.Xmode=False
        self.searchMode = False
        self.date ='1900-0-0'
    
    def setFinishCallBack(self,pfun):
        self.FinishCallback = pfun

    def searchX(self,url):
        #print("searchX",url)
        self.searchMode = True
        self.Xmode=True
        self.load(QUrl(url))
        

    def loadX(self,url):
        self.Xmode=True
        #print("loadX",url)
        self.load(QUrl(url))


    def onCookieAdd(self, cookie):                       # 处理cookie添加的事件
        name = cookie.name().data().decode('utf-8')     # 先获取cookie的名字，再把编码处理一下
        value = cookie.value().data().decode('utf-8')   # 先获取cookie值，再把编码处理一下
        self.cookies[name] = value                       # 将cookie保存到字典里 

    # 获取cookie
    def get_cookie(self):
        cookie_str = ''
        for key, value in self.cookies.items():         # 遍历字典
            cookie_str += (key + '=' + value + ';')     # 将键值对拿出来拼接一下
        return cookie_str                               # 返回拼接好的字符串
    
    def _loadFinished(self,result):        
        if self.title()=='天眼查校验':
            self.FinishCallback(self.title())
            return
        if self.Xmode:
            self.page().toHtml(self.callable)


    def callable(self,data):
        self.html = data
        #print("search",self.searchMode)
        if self.searchMode:
            self.searchMode =False
            self.Xmode = False
            try:
                url,self.date = pa.getSearchMode(data)
                self.loadX(url)
            except:
                self.FinishCallback('')
        else:
            self.FinishCallback(pa.getContent(data,self.date))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Loginwindow()
    w.show()
    sys.exit(app.exec_())
