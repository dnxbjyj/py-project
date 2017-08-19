# coding:utf-8
# 链家二手房信息爬虫
import sys
import scrapy

reload(sys)
sys.setdefaultencoding('utf-8')

class SecondHandHouseSpider(scrapy.Spider):
    name = 'SecondHandHouseSpider'
    # 主页：链家深圳二手房首页
    host = 'https://sz.lianjia.com/ershoufang/'
    # 准备爬取的初始页面
    start_urls = ['https://sz.lianjia.com/ershoufang/']
    
    # 页面解析函数
    