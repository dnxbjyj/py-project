# coding:utf-8
# 豆瓣爬虫核心方法 
from __future__ import unicode_literals
from selenium import webdriver
import requests
import time
import datetime
import json
from lxml import etree
import random
from operator import itemgetter
from jinja2 import Environment, FileSystemLoader
import traceback
import ConfigParser

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class DoubanSpider(object):
    '''
    豆瓣爬虫
    '''
    def __init__(self, user_name, password, headless = False):
        '''
        初始化
        :param user_name: 豆瓣登录用户名
        :param password: 豆瓣登录用户密码
        :param headless: 是否显示webdriver浏览器窗口
        :return: None
        '''
        self.user_name = user_name
        self.password = password
        self.headless = headless

        # 登录
        self.login()
        
    def login(self):
        '''
        登录，并持久化cookie
        :return: None
        '''
        # 豆瓣登录页面URL
        login_url = 'https://www.douban.com/accounts/login'

        # 获取chrome的配置
        opt = webdriver.ChromeOptions()
        # 在运行的时候不弹出浏览器窗口
        if self.headless:
            opt.set_headless()

        # 获取driver对象
        self.driver = webdriver.Chrome(chrome_options = opt)
        # 打开登录页面
        self.driver.get(login_url)

        print '[login] opened login page...'

        # 向浏览器发送用户名、密码，并点击登录按钮
        self.driver.find_element_by_name('form_email').send_keys(self.user_name)
        self.driver.find_element_by_name('form_password').send_keys(self.password)
        # 多次登录需要输入验证码，这里给一个手工输入验证码的时间
        time.sleep(6)
        self.driver.find_element_by_class_name('btn-submit').submit()
        print '[login] submited...'
        # 等待2秒钟
        time.sleep(2)

        # 创建一个requests session对象
        self.session = requests.Session()
        # 从driver中获取cookie列表（是一个列表，列表的每个元素都是一个字典）
        cookies = self.driver.get_cookies()
        # 把cookies设置到session中
        for cookie in cookies:
            self.session.cookies.set(cookie['name'],cookie['value'])

    def get_page_source(self, url):
        '''
        获取浏览器窗口中的页面HTML内容
        :param url: 网页链接
        :return: 网页页面HTML内容
        '''
        self.driver.get(url)
        page_source = self.driver.page_source
        print '[get_page_source] page_source head 100 char = {}'.format(page_source[:100])
        return page_source
    
    def get(self, url, params = None):
        '''
        向一个url发送get请求，返回response对象
        :param url: 网页链接
        :param params: URL参数字典
        :return: 发送请求后获取的response对象
        '''
        # 等待一个随机的时间，防止被封IP，这里随机等待0~6秒，亲测可用有效地避免触发豆瓣的反爬虫机制
        time.sleep(6 * random.random())
        resp = self.session.get(url, params = params, headers = self.get_headers())

        if resp:
            print '[get] url = {0}, status_code = {1}'.format(url, resp.status_code)
            resp.encoding = 'utf-8'
            # 这里很重要，每次发送请求后，都更新session的cookie，防止cookie过期
            if resp.cookies.get_dict():
                self.session.update(resp.cookies)
                print '[get] updated cookies, new cookies = {0}'.format(resp.cookies.get_dict())
            return resp
        else:
            print '[get] url = {0}, response is None'.format(url)
            return None
    def get_html(self,url, params = None):
        '''
        获取一个url对应的页面的HTML代码
        :param url: 网页链接
        :param params: URL参数字典
        :return: 网页的HTML代码
        '''
        resp = self.get(url)
        if resp:
            return resp.text
        else:
            return ''
    def get_headers(self):
        '''
        随机获取一个headers
        '''
        user_agents =  ['Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1','Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50','Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11']
        headers = {'User-Agent':random.choice(user_agents)}
        return headers

class DoubanDiscussionSpider(DoubanSpider):
    '''
    豆瓣小组讨论话题爬虫
    '''
    def __init__(self, user_name, password, group_name, headless = False):
        '''
        初始化
        :param user_name: 豆瓣登录用户名
        :param password: 豆瓣登录用户密码
        :param group_name: 豆瓣小组名称
        :param headless: 是否显示webdriver浏览器窗口
        :return: None
        '''
        super(DoubanDiscussionSpider,self).__init__(user_name, password, headless)
        self.group_name = group_name

        # 豆瓣小组讨论列表URL模板
        self.url_tpl = 'https://www.douban.com/group/{group_name}/discussion?start={start}&limit={limit}'.format(group_name = self.group_name,start = '{start}', limit = '{limit}')
        print '[__init__] url = {0}'.format(self.url_tpl)

    def get_discussion_list(self, start=0, limit=100, filter = []):
        '''
        获取讨论列表
        :param start: 开始条目数，默认值为0
        :param limit: 总条数，默认值为100，最大值也为100
        :param filter: 关键词列表，只过滤出标题或详情中含有关键词列表中关键词的项
        :return: 话题讨论内容字典列表
        '''
        list_url = self.url_tpl.format(start = start, limit = limit)
        page_html = self.get_html(list_url)
        
        html = etree.HTML(page_html)
        # 解析话题讨论列表
        trs = html.xpath('//*[@class="olt"]/tr')[1:]
        # 话题字典列表
        topics = []
        # 已结被添加的topic link列表，用于去重
        added_links = []
        for tr in trs:
            title = tr.xpath('./td[1]/a/text()')[0].strip()
            link = tr.xpath('./td[1]/a/@href')[0].strip()
            # 继续解析话题详情页面，从中解析出发布时间、描述详情
            topic_page_html = self.get_html(link)
            topic = etree.HTML(topic_page_html)
            # 发布时间字符串
            post_time_str = topic.xpath('//*[@class="topic-doc"]/h3[1]/span[2]/text()')[0].strip()
            # 详情
            detail = topic.xpath('//*[@class="topic-content"]')[0].xpath('string(.)').strip()

            # 根据关键词过滤
            if filter and not self.contains(title, filter) and not self.contains(detail, filter):
                continue
            
            topic_dict = {}
            topic_dict['title'] = title
            topic_dict['link'] = link
            if link in added_links:
                continue
            else:
                added_links.append(link)
            
            topic_dict['post_time_str'] = post_time_str
            topic_dict['post_time'] = time.mktime(time.strptime(post_time_str,'%Y-%m-%d %H:%M:%S'))
            topic_dict['detail'] = detail
            topics.append(topic_dict)
            print '[get_discussion_list] parse topic: {0} finished'.format(link)
        print '[get_discussion_list] get all topics finished, count of topics = {0}'.format(len(topics))
        # 对topics按照发布时间排序（降序）
        topics = sorted(topics, key = itemgetter('post_time'), reverse = True)
        return topics
    def get_discussion_list_cyclely(self, start = 0, limit = 100, filter = []):
        '''
        循环获取讨论列表
        :param start: 开始条目数，默认值为0
        :param limit: 总条数，默认值为100
        :param filter: 关键词列表，只过滤出标题或详情中含有关键词列表中关键词的项
        :return: 话题讨论内容字典列表
        '''
        topics = []
        if limit <= 100:
            topics = self.get_discussion_list(start, limit, filter)
        else:
            for start in range(start, limit, 100):
                topics.extend(self.get_discussion_list(start, 100, filter))
        print '[get_discussion_list_cyclely] get all topics finished, count of topics = {0}'.format(len(topics))
        # 对topics按照发布时间排序（降序）
        topics = sorted(topics, key = itemgetter('post_time'), reverse = True)
        return topics

    def contains(self, text, filter):
        '''
        判断一个字符串中是否包含了一个关键词列表中的至少一个关键词
        :param text: 字符串
        :param filter: 关键词字符串列表
        :return: bool
        '''
        for kw in filter:
            if kw in text:
                return True
        return False

    def render_topics(self, topics):
        '''
        把topic列表内容渲染到HTML文件中
        :param topics: topic列表
        :return: None
        '''
        env = Environment(loader = FileSystemLoader('E:/code/py-project/DoubanHouse/'))
        tpl = env.get_template('topics_tpl.html')
        with open('douban-house-topics-{0}.html'.format(datetime.datetime.now().strftime('%Y-%m-%d')),'w+') as fout:
            render_content = tpl.render(topics = topics)
            fout.write(render_content)
        print '[render_topics] render finished'
        
def sample():
    '''
    测试
    '''
    # 豆瓣账号用户名、密码
    user_name = sys.argv[1]
    password = sys.argv[2]

    # 创建配置文件对象
    config = ConfigParser.SafeConfigParser()
    config.read('config.conf')

    # 小组名称
    group_name = config.get('base','douban_group_name')    
    # 起始位置
    start = int(config.get('base','start'))
    # 打算爬取的小组讨论条数
    limit = int(config.get('base','limit'))

    # 关键词
    filter = [x.strip() for x in config.get('content','filter').split(',')]
    # 排除词
    exclude = [x.strip() for x in config.get('content','exclude').split(',')]

    # 创建爬虫spider对象
    spider = DoubanDiscussionSpider(user_name, password, group_name)    
    topics = spider.get_discussion_list_cyclely(start,limit, filter)
    # 将topics列表内容渲染到HTML表格中
    spider.render_topics(topics)

if __name__ == '__main__':
    try:
        sample()
        print 'end'
    except Exception as e:
        print 'error occurs! traceback: {0}'.format(traceback.format_exc())
