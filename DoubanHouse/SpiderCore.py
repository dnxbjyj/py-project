# coding:utf-8
# 豆瓣爬虫核心方法
from selenium import webdriver
import requests
import time
import json
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
        resp = self.session.get(url, params = params)

        if resp:
            print '[get] status_code = {0}'.format(resp.status_code)
            resp.encoding = 'utf-8'
            # 这里很重要，每次发送请求后，都更新session的cookie，防止cookie过期
            if resp.cookies.get_dict():
                self.session.update(resp.cookies)
                print '[get] updated cookies, new cookies = {0}'.format(resp.cookies.get_dict())
            return resp
        else:
            print '[get] response is None'
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
        self.url = 'https://www.douban.com/group/{group_name}/discussion'.format(group_name = self.group_name)
        print '[__init__] url = {0}'.format(self.url)

    def get_discussion_list(self, start=0, limit=100):
        '''
        获取讨论列表
        '''

def sample():
    '''
    测试
    '''
    user_name = sys.argv[1]
    password = sys.argv[2]
    group_name = 'nanshanzufang'
    spider = DoubanDiscussionSpider(user_name, password, group_name)

    # 需要登录才能看到的页面URL
    page_url = 'https://www.douban.com/accounts/'
    # 获取网页内容
    html = spider.get_page_source(page_url)
    # 将网页内容存入文件
    with open('html.txt','w+') as  fout:
        fout.write(html)    

if __name__ == '__main__':
    sample()
    print 'end'
