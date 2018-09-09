# coding:utf-8
# 用webdriver登录并获取cookies，并用requests发送请求，以豆瓣为例
from selenium import webdriver
import requests
import time
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def main():
    # 从命令行参数获取登录用户名和密码
    user_name = sys.argv[1]
    password = sys.argv[2]

    # 豆瓣登录页面URL
    login_url = 'https://www.douban.com/accounts/login'

    # 获取chrome的配置
    opt = webdriver.ChromeOptions()
    # 在运行的时候不弹出浏览器窗口
    # opt.set_headless()

    # 获取driver对象
    driver = webdriver.Chrome(chrome_options = opt)
    # 打开登录页面
    driver.get(login_url)

    print 'opened login page...'
    
    # 向浏览器发送用户名、密码，并点击登录按钮
    driver.find_element_by_name('form_email').send_keys(user_name)
    driver.find_element_by_name('form_password').send_keys(password)
    # 多次登录需要输入验证码，这里给一个手工输入验证码的时间
    time.sleep(6)
    driver.find_element_by_class_name('btn-submit').submit()
    print 'submited...'
    # 等待2秒钟
    time.sleep(2)

    # 创建一个requests session对象
    s = requests.Session()
    # 从driver中获取cookie列表（是一个列表，列表的每个元素都是一个字典）
    cookies = driver.get_cookies()
    # 把cookies设置到session中
    for cookie in cookies:
        s.cookies.set(cookie['name'],cookie['value'])

    # 关闭driver
    driver.close()
        
    # 需要登录才能看到的页面URL
    page_url = 'https://www.douban.com/accounts/'
    # 获取该页面的HTML
    resp = s.get(page_url)
    resp.encoding = 'utf-8'
    print 'status_code = {0}'.format(resp.status_code)
    # 将网页内容存入文件
    with open('html.txt','w+') as  fout:
        fout.write(resp.text)
    
    print 'end'

if __name__ == '__main__':
    main()
