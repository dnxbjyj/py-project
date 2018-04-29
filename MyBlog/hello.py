# coding:utf-8
# Hello World
from __future__ import unicode_literals
from flask import Flask

# 创建应用程序对象
app = Flask(__name__)

@app.route('/')
def hello():
    '''
    hello请求
    '''
    # 直接返回字符串
    return 'Hello, Flask World!'
        
if __name__ == '__main__':
    # 以debug模式启动程序
    app.run(debug = True)