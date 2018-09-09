# coding:utf-8
# 自如租房爬虫
from __future__ import unicode_literals
import re
from lxml import etree
import webutil as wu
from constants import page_cache_path,url_tpl1
from collections import OrderedDict
import os
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def pipline():
    '''
    调度流水线
    '''
    # 初始化
    # init()
    
    # 解析每个页面的信息
    for root,dirs,files in os.walk(page_cache_path):
        if not files:
            print 'page cache files list is empty!'
            return
        for f in files:
            path = os.path.join(root,f)
            with open(path,'r') as fin:
                page_content = fin.read()
                parse_single_page(page_content)

def init():
    '''
    初始化，做一些初始化操作
    '''
    # 创建网页HTML文本缓存目录
    if not os.path.exists(page_cache_path):
        os.makedirs(page_cache_path)
        
    # 获取所有页面的URL列表
    page_urls = get_urls_from_first_page(url_tpl1)
    
    # 缓存页面的html内容到page_cache文件夹下的文本文件中，文本文件命名为
    cache_page_html(page_urls)
    
def get_urls_from_first_page(page_url_tpl):
    '''
    从页面的第一页获取所有网页的URL
    :param page_url_tpl: 页面URL模板
    :return: URL列表
    '''
    first_page_url = page_url_tpl.format(page = 1)
    html = wu.get_html(first_page_url)
    # 解析出总页数
    total_page_matcher = re.search(r'共(\d+)页',html)
    if not total_page_matcher:
        raise Exception('parse total page number error!')
    total_page_num = int(total_page_matcher.group(1))
    print 'end get_urls_from_first_page, total_page_num = {0}'.format(total_page_num)
    return [page_url_tpl.format(page = page) for page in range(1,total_page_num + 1)]

def cache_page_html(page_urls):
    '''
    缓存多个页面的URL网页内容到文本文件，并存到缓存文件夹中
    '''
    total_page_num = len(page_urls)
    # 页码计数
    page = 1
    for url in page_urls:
        # 获取网页内容
        content = wu.get_html(url)
        # 存入文件
        with open(os.path.join(page_cache_path,'{0}.txt'.format(page)),'w+') as fout:
            fout.write(content)
        page += 1
    
def parse_single_page(page_content):
    '''
    解析单个页面
    :param page_content: 页面HTML内容
    :return: 单个页面的租房信息字典列表
    '''
    # 构建etree对象
    html = etree.HTML(page_content)
    # 选取租房信息列表
    house_lis = html.xpath('//ul[@id="houseList"]/li')
    
    return [parse_single_house_info(house_li) for house_li in house_lis]
    
def parse_single_house_info(house_li):
    '''
    解析单条租房信息
    :param house_li: 单条房屋信息HTML li标签对象
    :return: 单条房屋信息字典
    '''
    # 标题
    title = house_li.xpath('./div[2]/h3/a/text()')[0]
    # 链接
    link = 'http:' + house_li.xpath('./div[2]/h3/a/@href')[0]
    # 地址
    addr = house_li.xpath('./div[2]/h4/a/text()')[0]
    # 面积
    
    # 楼层
    
    # 楼高（层数）
    
    # 房型
    
    # 标签
    
    # 价格

def combine_house_info(page_urls):
    '''
    把多个页面的租房信息字典列表整合为一个字典列表
    '''
    house_info_dicts = []
    for url in page_urls:
        house_info_dicts.extend(parse_single_page(url))
    return house_info_dicts
    
def output2excel(house_info_dicts):
    '''
    把房屋信息列表写入到Excel文件中，包含的列有：
    '''
    pass
    
def main():
    pipline()

if __name__ == '__main__':
    main()
