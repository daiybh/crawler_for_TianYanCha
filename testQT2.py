import sys

from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineCore import QWebEngineUrlRequestInterceptor
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage, QWebEngineProfile

import qt_proxy
class WebEngineUrlRequestInterceptor(QWebEngineUrlRequestInterceptor):
    def interceptRequest(self, info):
        # info.setHttpHeader("X-Frame-Options", "ALLOWALL")
        #print("interceptRequest")
        #print(info.requestUrl()) 
        pass

class MyWebEnginePage(QWebEnginePage):
    def acceptNavigationRequest(self, url, _type, isMainFrame):
        #print("acceptNavigationRequest")
       # print(url)
        return QWebEnginePage.acceptNavigationRequest(self, url, _type, isMainFrame)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    browser = QWebEngineView()
    interceptor = WebEngineUrlRequestInterceptor()
    profile = QWebEngineProfile()
    profile.setRequestInterceptor(interceptor)
    page = MyWebEnginePage(profile, browser)
    qt_proxy.autoProxy()
    #page.setUrl(QUrl("https://stackoverflow.com/questions/50786186/qwebengineurlrequestinterceptor-not-working"))
    page.setUrl(QUrl("http://www.ip138.com/"))
    browser.setPage(page)
    browser.show()
    sys.exit(app.exec_())