# coding:utf-8
# 分析2017年政府工作报告，从中提取出前20个高频词
import sys
from bs4 import BeautifulSoup as BS
import html_utils
import cut_text_utils

# 2017年政府工作报告全文URL
REPORT_URL = 'http://www.gov.cn/premier/2017-03/16/content_5177940.htm'

# 从2017年政府工作报告html页面内容中解析出正文
def parse_report_article(html):
    soup = BS(html,'html.parser')
    article = soup.find('div',attrs = {'id':'UCAP-CONTENT'})
    return article.text
    
# 传入2017年政府工作报告全文的URL，解析出topn关键词及词频
def get_topn_words(url,topn):
    html = html_utils.get_html(url)
    article = parse_report_article(html)
    return cut_text_utils.get_topn_words(article,topn)
    
def main():
    # 设置字节流编码方式为utf-8
    reload(sys)
    sys.setdefaultencoding('utf-8')
    
    with open('out.tmp','w+') as fout:
        fout.write(str(get_topn_words(REPORT_URL,20)))
    
if __name__ == '__main__':
    main()