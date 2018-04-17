# coding:utf-8
# html工具函数
import requests

# 通用请求Hearders
HEADERS = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36'}

# html页面解析异常
class HtmlParseError(Exception):
    def __init__(self,value):
        self.value = value
        
    def __str__(self):
        return repr(self.value)

# 获取网页页面html全文
def get_html(url):
    resp = requests.get(url,headers = HEADERS)
    resp.encoding = 'utf-8'
    if resp:
        return resp.text
    return None