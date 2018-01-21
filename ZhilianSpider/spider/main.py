# coding:utf-8
# 主爬虫
import sys
from ZhilianSpider.utils.WebUtil import HtmlUtil
from ZhilianSpider.utils.ParseUtil import XiaoyuanParseUtil

reload(sys)
sys.setdefaultencoding('utf-8')

def main():
    url = 'https://xiaoyuan.zhaopin.com/full/0/765_0_180000_0_0_0_0_1_0'
    html = HtmlUtil(url)
    parser = XiaoyuanParseUtil(html.get_text())

    parser.get_page_urls()


if __name__ == '__main__':
    main()