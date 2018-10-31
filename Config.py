#-*-coding:utf-8-*- #编码声明，不要忘记！
timer=8000

import configparser

cf = configparser.ConfigParser()
try:
    cf.read("config.cfg")
    timer = cf.getint("main","timer")  

except:
    pass
print("timer>>",timer)
