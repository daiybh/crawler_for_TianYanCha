import sys

from PyQt5.QtCore import QUrl,QTimer
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtNetwork import QNetworkProxy
from  urllib import parse as urlparse

proxy=[["114.119.116.93","61066	"],
["59.53.141.144	","9000	"],
["124.235.145.79","80	"],
["119.163.7.159	","8060	"],
["58.251.49.4	","5872	"],
["117.21.191.154","32340	"],
["116.62.134.173","9999	"],
["115.223.217.13","9000	"],
["183.147.221.43","9000	"],
["111.160.96.34	","45032"],
["122.243.15.22	","9000	"],
["106.75.14.190	","9998	"],
["114.234.81.181","9000	"],
["61.133.245.70	","41299"],
["211.159.171.58","80	"],
["119.163.7.159","8060"]]
for x in proxy:
  print(x)

def setMyProxy(idx):
  #proxy_string ="http://username:password@ip:port"
  proxy_string="http://114.119.116.93:61066"
  proxy_string="http://107.189.36.34:3128"
  proxy_string="http://"+proxy[idx][0].strip().strip('\t\n')+":"+proxy[idx][1].strip().strip('\t\n')
  print(proxy_string)
  set_proxy(proxy_string)

def set_proxy(string_proxy):
    proxy = QNetworkProxy()
    urlinfo = urlparse.urlparse(string_proxy)
    if urlinfo.scheme == 'socks5':
        proxy.setType(QNetworkProxy.Socks5Proxy)
    elif urlinfo.scheme == 'http':
        proxy.setType(QNetworkProxy.HttpProxy)
    else:
        proxy.setType(QNetworkProxy.NoProxy)
    proxy.setHostName(urlinfo.hostname)
    proxy.setPort(urlinfo.port)
    proxy.setUser(urlinfo.username)
    proxy.setPassword(urlinfo.password)
    QNetworkProxy.setApplicationProxy(proxy)

def handleProxyAuthReq(url, auth, proxyhost):
    print("handleProxyAuthReq>>>",url)
    auth.setUser(username)
    auth.setPassword(password)
idx =0
def autoProxy():
  global idx
  setMyProxy(idx)
  idx +=1

def mainC():
    # 创建一个 application实例
    app = QApplication(sys.argv)
    win = QWidget()
    win.setWindowTitle('Web页面中的JavaScript与 QWebEngineView交互例子')

    # 创建一个垂直布局器
    layout = QVBoxLayout()
    win.setLayout(layout)

    # 创建一个 QWebEngineView 对象
    view = QWebEngineView()
    
    #view.page().proxyAuthenticationRequired.connect(handleProxyAuthReq)
    #view.load(QUrl("https://www.ipip.net/ip.html"))
    view.load(QUrl("https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-1"))
    view.load(QUrl("http://www.ip138.com/"))
    
    # 创建一个按钮去调用 JavaScript代码
    button = QPushButton('设置全名')


    def js_callback( result ):
        print(result)


    def complete_name():
        #view.page().runJavaScript('completeAndReturnName();', js_callback)
        global idx
        setMyProxy(idx)
        idx+=1
        view.load(QUrl("http://www.ip138.com/"))



    # 按钮连接 'complete_name'槽，当点击按钮是会触发信号
    button.clicked.connect(complete_name)

    # 把QWebView和button加载到layout布局中
    layout.addWidget(view)
    layout.addWidget(button)

    # 显示窗口和运行app
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
  mainC()