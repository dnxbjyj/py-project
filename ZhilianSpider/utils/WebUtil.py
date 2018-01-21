# coding:utf-8
# 和网络请求有关的工具类
import sys
import requests
from ZhilianSpider.constants import HtmlConstant

reload(sys)
sys.setdefaultencoding('utf-8')

class HtmlUtil(object):
    '''
    抓取网页的工具类
    '''
    def __init__(self,url):
        self.url = url

        # 创建请求会话对象
        self.session = requests.Session()
        self.session.headers.update(HtmlConstant.COMMON_HEADERS)
        self.session.verify = False

    def get_text(self):
        '''
        获取一个网页的返回内容
        :return: 网页的HTML内容
        '''
        resp = self.session.get(self.url,timeout = HtmlConstant.DEFAULT_TIME_OUT)
        if self.check_ok(resp.status_code):
            resp.encoding = 'utf-8'
            return resp.text
        return None

    def check_ok(self,status_code):
        '''
        根据一个请求的响应码（整型），判断响应是否成功
        :param status_code:
        :return:
        '''
        if status_code / 100 == 2:
            return True
        return False



def main():
    url = 'http://www.baidu.com'
    html = HtmlUtil(url)
    print html.get_text()
    pass

if __name__ == '__main__':
    main()