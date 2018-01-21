# coding:utf-8
# 网页解析工具类
import re
import sys
import urljoin
import logging
from bs4 import BeautifulSoup
from ZhilianSpider.constants import HtmlConstant

reload(sys)
sys.setdefaultencoding('utf-8')

class XiaoyuanParseUtil(object):
    '''
    "校园招聘"板块网页解析工具类
    '''
    def __init__(self,html):
        '''
        初始化
        :param html: 网页HTML源代码
        '''
        self.html = html
        self.soup = BeautifulSoup(html,'html.parser',from_encoding = 'utf-8')

    def get_page_urls(self):
        '''
        从初始页面HTML中解析出每一页的URL
        :return:
        '''
        # 解析出页码列表
        pages_ul = self.soup.find('ul',class_ = 'npage fr')
        pages_lis = pages_ul.find_all('li')
        pages_lis = [li for li in pages_lis if re.search(r'\d+',li.text)]

        # 最后一页的li对象
        last_page_li = pages_lis[-1]
        # 从最后一页的li对象中解析出页面URL和页码数
        # URL格式：/full/0/765_0_180000_0_0_0_0_10_1，其中最后的'10'表示页码数
        last_page_url = last_page_li.find('a')['href']
        last_page_url = urljoin.url_path_join(HtmlConstant.ZHILIAN_XIAOYUAN_HOST)
        page_num = int(last_page_li.text)
        logging.debug('get_page_urls method, last_page_url = {}, page_num = {}',last_page_url,page_num)

        # 组建URL格式化字符串
        splited_url = last_page_url.split('_')
        page_formatter_url = '_'.join()

def main():
    pass

if __name__ == '__main__':
    main()