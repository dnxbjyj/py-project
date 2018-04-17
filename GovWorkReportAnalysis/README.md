# 分析了六十多年间100万字的政府工作报告，我看到了这样的变迁

> 版权声明：本文为博主m2fox原创文章，转载请注明出处：http://www.jianshu.com/p/bfde4f742294

每年我国政府都会发布年度政府工作报告，而报告中出现最多的TopN关键词都会成为媒体热议的焦点，更是体现了过去一年和未来政府工作的重点和趋势。

在中央政府网站上也可以看到从1954年至今每年的政府工作报告，链接：http://www.gov.cn/guoqing/2006-02/16/content_2616810.htm

那么突发奇想，从这60多年间的政府工作报告中可以看出来什么样的变迁呢？说干就干，下面就是实现这一想法的历程。

# 目标是什么

* 获取1954年至今历年政府工作报告的全文，并统计出每年政府工作报告中Top20的关键词，并用图表可视化展示出来。

* 统计每十年的政府工作报告的合并Top20关键词，并用图表直观展示出来，从中分析出变迁的趋势。

# 准备工作

### 数据获取

数据获取阶段需要有两个准备：

* 网页链接：

2017年政府工作报告链接：http://www.gov.cn/premier/2017-03/16/content_5177940.htm

1954~2017年政府工作报告汇总页面链接：http://www.gov.cn/guoqing/2006-02/16/content_2616810.htm

* 技术准备

使用非常好用的web库——requests获取网页内容。

### 数据解析

使用BeautifulSoup库解析网页HTML内容，从中解析出政府工作报告的文本内容。

### 数据处理与分析

使用结巴分词库（jieba）对政府工作报告文本内容进行分词、过滤无效词、统计词频。

### 结果展示

使用matplotlib库画出每十年政府工作报告关键词的散点分布图，通过对比不同年代的图，分析其中的变化趋势。

# 动手搞

准备工作做好后，我们开始按照计划一步步地开始实施。

### 获取网页HTML内容

为了代码复用，创建一个html_utils.py文件，提供下载网页内容的函数，并提供了一个HTML页面解析异常类：

```python
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
```

### 创建一个分词工具

我们的总体思路是先获取网页内容，然后从网页内容中解析出政府工作报告正文，然后对其进行分词，这里分词需要用到jieba模块，我们创建一个cut_text_utils.py文件，在其中提供分词的函数，内容如下：

```python
# coding:utf-8
# 分词操作工具函数
import sys
import jieba
from collections import Counter

# 对一段文本进行分词，并过滤掉长度小于2的词（标点、虚词等），用全模式分词
def cut_text(text):
    cut_list = jieba.cut(text.lower())
    return [word for word in cut_list if len(word) >= 2]
    
# 统计出一段文本中出现数量最多的前n个关键词及数量
def get_topn_words(text,topn):
    cut_list = cut_text(text)
    counter = Counter(cut_list)
    return counter.most_common(topn)

if __name__ == '__main__':
    # 设置字节流编码方式为utf-8
    reload(sys)
    sys.setdefaultencoding('utf-8')
    
    s = u'我想和女朋友一起去北京故宫博物院参观和闲逛。'
    # print cut_text(s)
    print get_topn_words(s,5)
```

运行上述Demo脚本，输出：

[(u'参观', 1), (u'北京故宫博物院', 1), (u'一起', 1), (u'女朋友', 1), (u'闲逛', 1)]

### 创建一个绘图工具

最终要使用matplotlib库绘出关键词的散点图，可以更直观地进行分析，所以我们再写一个绘图工具文件visual_utils.py，内容如下：

```python
# coding:utf-8
import matplotlib.pyplot as plt

# 指定默认字体，防止画图时中文乱码
plt.rcParams['font.sans-serif'] = ['SimHei']  

# 传入一组关键词及词频列表，从高到低绘出每个关键词频率的散点图
# keywords示例：[(u'张三',10),(u'李四',12),(u'王五',7)]
def draw_keywords_scatter(keywords,title = None,xlabel = None,ylabel = None):
    # 先对keywords按词频从高到低排序
    keywords = sorted(keywords,key = lambda item:item[1],reverse = True)

    # 解析出关键词列表
    words = [x[0] for x in keywords]
    # 解析出对应的词频列表
    times = [x[1] for x in keywords]
    
    x = range(len(keywords))
    y = times
    plt.plot(x, y, 'b^')
    plt.xticks(x, words, rotation=45)
    plt.margins(0.08)
    plt.subplots_adjust(bottom=0.15)
    # 图表名称
    plt.title(title)
    # x,y轴名称
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()
    
def main():
    draw_keywords_scatter([(u'张三',10),(u'李四',12),(u'王五',7)],u'出勤统计图',u'姓名',u'出勤次数')
    
if __name__ == '__main__':
    main()
    
```

运行上面的Demo脚本，绘图结果如下：

![](http://upload-images.jianshu.io/upload_images/8819542-9e9b467897169970.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


### 解析2017年政府工作报告

接下来我们先获取到2017年的政府工作报告试试水，创建一个文件year2017_analysis.py，内容如下：

```python
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
    article = soup.find('div',attrs = {'id':'UCAP-CONTENT'})  # 报告正文，这里可以通过分析网页HTML结构获取到解析的方法
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
```

运行上述脚本，然后在当前目录下可以看到产生了一个out.tmp文件，其内容如下：

[(u'发展', 125), (u'改革', 68), (u'推进', 65), (u'建设', 54), (u'经济', 52), (u'加强', 45), (u'推动', 42), (u'加快', 40), (u'政府', 39), (u'创新', 36), (u'完善', 35), (u'全面', 35), (u'企业', 35), (u'促进', 34), (u'提高', 32), (u'就业', 31), (u'实施', 31), (u'中国', 31), (u'工作', 29), (u'支持', 29)]

从中可以看出2017年的前五关键词是：发展，改革，推进，建设，经济，和我们经常在媒体上看到的情况也比较吻合。

### 解析1954到2017每年的政府工作报告

思路是这样的，首先从汇总页面获取到每年政府工作报告网页的链接，然后分别爬取每个链接获取到网页内容，接着解析出每年的政府工作报告正文，最后对每10年的政府工作报告合并分析出Top20关键词并展示出来。

导包：

```python
# coding:utf-8
# 1954~2017年政府工作报告汇总分析
import sys
import json
from collections import OrderedDict
from bs4 import BeautifulSoup as BS
import html_utils
from html_utils import HtmlParseError
import cut_text_utils
```

汇总页面URL：

```python
# 汇总URL
SUMMARY_URL = 'http://www.gov.cn/guoqing/2006-02/16/content_2616810.htm'
```

从汇总页面解析出每年政府工作报告全文页面的URL列表：

```python
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
```

从报告正文页面html中解析出正文内容：

注：这里要考虑两种不同的页面结构进行解析。

```python
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
```

通过上述函数结合使用，可以爬取到1954年到2017年的所有政府工作报告的文本，总字数为100万零7000多字。

接着以下几个函数用来解析关键词：

```python
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
```

汇总以上代码，合并为summary_analysis.py文件，内容如下：

```python
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
```

运行该文件，在当前目录下的out.tmp文件可以看到其内容如下：

【1954-1964】
我们:932;人民:695;国家:690;我国:664;建设:650;发展:641;社会主义:618;生产:509;工业:491;农业:481;工作:396;增长:385;增加:376;必须:361;计划:339;已经:328;方面:299;进行:298;全国:295;企业:267;

【1975-1987】
发展:1012;我们:1011;经济:875;建设:664;我国:609;企业:586;人民:577;国家:569;社会主义:535;改革:499;工作:488;生产:486;必须:451;提高:368;增长:349;方面:349;进行:349;问题:320;增加:290;加强:288;

【1988-1997】
发展:1182;经济:789;建设:696;改革:537;工作:495;加强:485;企业:485;继续:455;国家:435;社会:432;我们:399;我国:378;社会主义:350;积极:340;进一步:334;人民:331;提高:311;政府:289;增加:276;必须:275;

【1998-2007】
发展:814;建设:597;加强:536;经济:459;工作:430;改革:402;企业:368;继续:320;社会:287;政府:284;推进:261;增加:245;加快:240;积极:240;进一步:236;坚持:228;我们:221;提高:217;农村:207;管理:203;

【2008-2017】
发展:1115;建设:597;经济:554;推进:507;改革:479;加强:456;社会:345;加快:344;政府:320;提高:312;实施:301;促进:301;我们:294;工作:287;制度:272;增长:259;完善:248;政策:240;就业:240;企业:240;

同时也绘出了5张图，分别如下：

![](http://upload-images.jianshu.io/upload_images/8819542-e2a9e5d54f09d575.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![](http://upload-images.jianshu.io/upload_images/8819542-d7faaab009287939.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![](http://upload-images.jianshu.io/upload_images/8819542-0462f1fbfe838599.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![](http://upload-images.jianshu.io/upload_images/8819542-ba8effcae085435a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![](http://upload-images.jianshu.io/upload_images/8819542-9a460540ca1a7c44.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


### 结果分析

从以上5张图可以看出，1954~1964年间，“我们”是绝对的关键词，其次第二梯队是：人民，国家，我国，建设，发展，社会主义，第三梯队是：生产，工业，农业，从中可以感受到鲜明的时代气息。

到了1978年改革开放及其后的十年间，“发展”成为了绝对的关键词，而第二梯队的关键词是：经济，建设，我国，企业...“生产”也是提到的次数很多的关键词。

1988~1997这十年间，“发展”依然是绝对的关键词，而第二梯队的关键词基本还是：经济，建设，改革，企业....

1998~2007是进入新世纪的十年，“发展”的主旋律依然没有变化，“农村”这一关键词进入前20，体现国家对农业的重视。印象中也就是在这几年间国家取消了延续了2000多年历史的农业税，从此不用再“交公粮”了。

再看最近的十年：2008~2017，“发展”依然是第一要务，而“制度”、“政策”、“就业”等关键词进入前20，具有新时代的特色。

# 获取本文项目源码

[dnxbjyj · GitHub](https://github.com/dnxbjyj/py-project/tree/master/GovWorkReportAnalysis)

# 1954~2017政府工作报告原文汇总

https://github.com/dnxbjyj/py-project/blob/master/GovWorkReportAnalysis/reports-bak.txt