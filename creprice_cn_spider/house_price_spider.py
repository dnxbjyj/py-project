# coding:utf-8
# 爬取中国房价行情网不同城市、历年来的房价数据（http://www.creprice.cn/rank/cityforsale.html）
import sys
import requests
from bs4 import BeautifulSoup as BS
from collections import OrderedDict
import json
from datetime import date
import xlsxwriter

reload(sys)
sys.setdefaultencoding('utf-8')

def build_html_page_url(year,month,city_level):
    '''
    构建查询某个月、某级别城市房价网页的URL
    :param year: 年份
    :param month: 月份
    :param city_level: 城市级别
    :return: 网页URL
    '''
    url_template = 'http://www.creprice.cn/rank/cityforsale.html?type=11&citylevel={city_level}&y={year}&m={month}'
    return url_template.format(city_level = city_level,year = year, month = month)

def build_month_html_page_url(date_,city_level):
    '''
    传入一个日期对象，构建查询某个月、某级别城市房价网页的URL
    :param date_: 日期对象
    :param city_level: 城市级别
    :return: 网页URL
    '''
    return build_html_page_url(date_.year,date_.month,city_level)

def get_dates(min_date,max_date):
    '''
    获取一个时间段内的date对象列表，包含开始日期和结束日期
    :param min_date: 最小日期
    :param max_date: 最大日期
    :return: 每个月1日的日期对象列表
    '''
    dates = []
    for m in range(min_date.month,13):
        dates.append(date(min_date.year,m,1))

    if min_date.year == max_date.year:
        return dates

    for y in range(min_date.year + 1,max_date.year):
        for m in range(1,13):
            dates.append(date(y,m,1))

    for m in range(1,max_date.month + 1):
        dates.append(date(max_date.year,m,1))
    return dates

def build_html_page_urls(min_date,max_date,city_level):
    '''
    构建一段时间内的查询某个月、某级别城市房价网页的URL列表，以月为最小单位，包含最小日期和最大日期
    :param min_date: 最小日期
    :param max_date: 最大日期
    :param city_level: 城市级别
    :return: 每月的网页URL列表
    '''
    urls = []
    for m in range(min_date.month,13):
        urls.append(build_html_page_url(min_date.year,m,city_level))

    if min_date.year == max_date.year:
        return urls

    for y in range(min_date.year + 1,max_date.year):
        for m in range(1,13):
            urls.append(build_html_page_url(y, m, city_level))

    for m in range(1,max_date.month + 1):
        urls.append(build_html_page_url(max_date.year,m,city_level))
    return urls

def get_html_content(url):
    '''
    下载网页的HTML文本
    :param url: 网页URL
    :return: 网页的HTML文本（UTF-8编码格式）
    '''
    headers = {}
    headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
    headers['Host'] = 'www.creprice.cn'

    resp = requests.get(url,headers = headers,timeout = 30)
    resp.encoding = 'utf-8'
    return resp.text

def store_html_files(min_date,max_date,city_level):
    '''
    存储某级别城市某一时间段内的房价网页HTML内容到文件中，防止频繁请求网页，一是效率低，二是可能触发反爬虫措施
    文件命名格式示例：2018-1-level1.txt
    :param min_date: 开始日期
    :param max_date: 结束日期
    :param city_level: 城市级别
    :return: None
    '''
    # 1. 获取时间段内所有的日期
    dates = get_dates(min_date, max_date)

    # 2. 遍历日期列表，获取所有的URL，并解析数据
    for date_ in dates:
        url = build_month_html_page_url(date_, city_level)
        html = get_html_content(url)
        file_name = './data-tmp/{year}-{month}-level{city_level}.txt'.format(year = date_.year,month = date_.month,city_level = city_level)
        with open(file_name,'w+') as fout:
            fout.write(html)
        print 'finish to store file: {0}'.format(file_name)

def parse_html(html_content):
    '''
    从房价HTML页面中解析出房价数据，返回一个以城市名为key、房价为vlaue的字典
    :param html_content: 房价HTML网页内容
    :return: 以城市名为key、房价为vlaue的字典
    '''
    soup = BS(html_content, 'html.parser')
    tr_list = soup.find('div', attrs={'id': 'nowmonthshow'}).find('table').find('tbody').find_all('tr')
    price_dict = OrderedDict()
    # 因网站收费限制，只能爬取前20条数据
    for tr in tr_list if len(tr_list) <= 20 else tr_list[:20]:
        city_name = tr.find_all('td')[1].text.strip()
        price_str = tr.find_all('td')[2].text.strip()
        price = int(''.join([d for d in price_str if d != ',']))
        price_dict[city_name] = price
    return price_dict

def parse_month_html(date_,html_content):
    '''
    从某月的数据页面解析出数据，返回一个以该月date对象为key、各个城市房价数据为value的字典
    :param html_content: 日期对象
    :return: 以该月date对象为key、各个城市房价数据为value的字典
    '''
    return {date_:parse_html(html_content)}

def get_level1_2_city_all_data_from_stored_file(min_date,max_date,city_name_list = None,reverse = False):
    '''
    读取预存数据（防止频繁爬虫被屏蔽），获取1级、2级城市在一段时间内的所有房价数据
    以字典形式返回，日期为key，各个城市的房价数据为value
    :param min_date: 开始日期
    :param max_date: 结束日期
    :param city_name_list: 如果该列表不为空，只获取该列表中的城市的数据
    :param reverse: 是否倒序排列
    :return: 以日期为key，各个城市的房价数据为value的字典
    '''
    # 1. 获取时间段内所有的日期
    dates = get_dates(min_date, max_date)
    if reverse:
        dates = dates[::-1]

    summary_data = OrderedDict()
    for date_ in dates:
        # '年-月'日期字符串
        date_str = '{0}-{1}'.format(date_.year,date_.month)
        month_data = OrderedDict()
        # 遍历1、2级城市
        for city_level in [1,2]:
            # 从预存的文件中读取网页内容并解析数据
            file_name = './data-tmp/{year}-{month}-level{city_level}.txt'.format(year=date_.year, month=date_.month,city_level=city_level)
            with open(file_name,'r') as fin:
                html = fin.read()
                data = parse_html(html)
                # 按照传入的城市名列表过滤
                if city_name_list:
                    data = {city:data[city] for city in data if city in city_name_list}
                month_data.update(data)
        print 'finish to parse: {0}'.format(date_str)
        summary_data[date_str] = month_data
    return summary_data

def write_price_dict_to_excel(min_date,max_date,city_name_list = None,reverse = False):
    '''
    把指定城市、指定时间段的房价数据写入Excel，第一行为城市名（表头），第一列为日期列，第2~N列为每个城市的房价
    :param min_date: 开始日期
    :param max_date: 结束日期
    :param city_name_list: 城市名列表
    :param reverse: 是否按时间倒序排列
    :return: None
    '''
    # 获取数据字典
    summary_data = get_level1_2_city_all_data_from_stored_file(min_date,max_date,city_name_list,reverse)

    # 写入Excel
    workbook = xlsxwriter.Workbook('price_data.xlsx')
    worksheet = workbook.add_worksheet()
    # 表头
    title = [u'月份'] + summary_data[summary_data.keys()[0]].keys()
    # 日期列表
    date_list = summary_data.keys()
    worksheet.write_row('A1',title)
    worksheet.write_column('A2',date_list)

    # 房价数据行数计数变量
    row_num = 2
    for month,data in summary_data.items():
        row_price_list = []
        for city,price in data.items():
            row_price_list.append(price)
        worksheet.write_row('B{0}'.format(row_num),row_price_list)
        row_num = row_num + 1

    workbook.close()

def main():
    # 开始日期
    min_date = date(2008,1,1)
    # 结束日期
    max_date = date(2018,2,1)

    # 1. 第1步：预存所有的网页HTML内容到文件
    # store_html_files(min_date, max_date, 2)

    # 2. 第2步：上一步完成后，从预存的文件中读取HTML内容并解析成数据、输出到Excel文件
    city_name_list = [u'北京',u'上海',u'广州',u'深圳',u'重庆',u'长春',u'贵阳',u'兰州',u'长沙',u'福州']
    write_price_dict_to_excel(min_date, max_date, city_name_list=city_name_list, reverse=True)
    print 'all finish!'

if __name__ == '__main__':
    main()