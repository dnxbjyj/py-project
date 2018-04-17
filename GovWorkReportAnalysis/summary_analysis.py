# coding:utf-8
# 1954~2017年政府工作报告汇总分析
import sys
import json
from collections import OrderedDict
from bs4 import BeautifulSoup as BS
import html_utils
from html_utils import HtmlParseError
import cut_text_utils
import visual_utils

# 汇总URL
SUMMARY_URL = 'http://www.gov.cn/guoqing/2006-02/16/content_2616810.htm'

# 2017年政府工作报告全文URL
REPORT2017_URL = 'http://www.gov.cn/premier/2017-03/16/content_5177940.htm'

# 从汇总页面解析出每年政府工作报告全文页面的URL
# 注：只有2017年的页面URL是专题页面而非全文页面
def get_report_urls(summary_url):
    html = html_utils.get_html(summary_url)
    soup = BS(html,'html.parser')
    reports_table = soup.select('#UCAP-CONTENT table tbody')[0]
    reports = [(atag.text,atag['href']) for trtag in reports_table.select('tr') for tdtag in trtag.select('td') if len(tdtag.select('a')) != 0 for atag in tdtag.select('a')]
    
    # 过滤去2017年的URL
    report_urls = [x for x in reports if x[0] != '2017']
    report_urls.append(('2017',REPORT2017_URL))
    # 按照年份升序排序
    report_urls = sorted(report_urls,key = lambda item:item[0])
    return report_urls

# 从报告页面html中解析出正文内容
# 考虑到不同年份报告的2种不同的html结构，采用两种解析方案
def parse_report_article(html):
    soup = BS(html,'html.parser')
    # 解析方案1
    article = soup.select('#UCAP-CONTENT')
    # 若article为空，则换方案2来解析
    if len(article) == 0:
        article = soup.select('.p1')
        # 若还为空，则抛出异常
        if len(article) == 0:
            raise HtmlParseError('parse report error!')
            
    return article[0].text

# 传入某一年政府工作报告全文的URL，解析出topn关键词及词频
def get_topn_words(url,topn):
    html = html_utils.get_html(url)
    article = parse_report_article(html)
    return cut_text_utils.get_topn_words(article,topn)

# 传入若干个政府工作报告全文的URL，解析出合并topn关键词
# save_reports：是否保存文本到文件中（reports.txt）
def get_topn_words_from_urls(urls,topn,save_reports = False):
    htmls = [html_utils.get_html(url) for url in urls]
    # 汇总文本
    summary_atricle = '\n'.join([parse_report_article(html) for html in htmls])
    if save_reports:
        with open('reports.txt','w+') as fout:
            fout.write(summary_atricle)
    return cut_text_utils.get_topn_words(summary_atricle,topn)

# 根据传入的每年的政府工作报告全文URL，解析出每年的topn关键词
def get_topn_words_yearly(report_urls,topn):
    keywords = OrderedDict()
    # 遍历url列表，解析出每年政府工作报告的top30关键词并存入字典keywords
    for year,url in report_urls:
        print 'start to parse {year} report...'.format(year = year)
        keywords[year] = get_topn_words(url,topn)
    return keywords

# 根据传入的每年的政府工作报告全文URL，解析出每个十年的合并topn关键词
def get_topn_words_decadal(report_urls,topn):
    # 统计出每个10年的topn关键词
    decade1 = ['1964','1960','1959','1958','1957','1956','1955','1954']
    decade2 = ['1987','1986','1985','1984','1983','1982','1981','1980','1979','1978','1975']
    decade3 = ['1997','1996','1995','1994','1993','1992','1991','1990','1989','1988']
    decade4 = ['2007','2006','2005','2004','2003','2002','2001','2000','1999','1998']
    decade5 = ['2017','2016','2015','2014','2013','2012','2011','2010','2009','2008']
    
    keywords = OrderedDict()
    decade_items = [('1954-1964',decade1),('1975-1987',decade2),('1988-1997',decade3),('1998-2007',decade4),('2008-2017',decade5)]
    for years,decade in decade_items:
        print 'start to parse {years} reports...'.format(years = years)
        urls = [item[1] for item in report_urls if item[0] in decade]
        keywords[years] = get_topn_words_from_urls(urls,topn)
        
    return keywords

def main():
    # 设置字节流编码方式为utf-8
    reload(sys)
    sys.setdefaultencoding('utf-8')
    
    # 按年代分析每10年的政府工作报告
    report_urls = get_report_urls(SUMMARY_URL)
    keywords = get_topn_words_decadal(report_urls,20)
    
    # 将结果保存到文件
    with open('out.tmp','w+') as fout:
        for years,words in keywords.items():
            fout.write('【{years}】\n'.format(years = years.decode('unicode-escape').encode('utf-8')))
            for word,count in words:
                fout.write('{word}:{count};'.format(word = word,count = count))
            fout.write('\n\n')
            
    # 绘出散点图
    for years,words in keywords.items():
        visual_utils.draw_keywords_scatter(words[:20],u'{years}年政府工作报告关键词Top{topn}'.format(years = years,topn = 20),u'关键词',u'出现总次数')
    

if __name__ == '__main__':
    main()