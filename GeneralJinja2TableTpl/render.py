# coding:utf-8
# 豆瓣爬虫核心方法 
from __future__ import unicode_literals
from jinja2 import Environment, FileSystemLoader

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class TableTplRender(object):
    '''
    通用的HTML表格渲染工具
    '''
    def __init__(self, title, keys, data_dicts):
        '''
        初始化
        :param title: 表格表头字符串列表 
        :param keys: 数据字典的键列表 
        :param data_dicts: 数据字典列表
        :return: None
        '''
        self.title = title
        self.keys = keys
        self.data_dicts = data_dicts
        # 模板文件位置，默认为当前位置
        self.tpl_dir = './'
        # 模板文件，默认为table_tpl.html
        self.tpl_file = 'table_tpl.html'
        
    def render(self):
        '''
        把把数据字典列表内容按照默认表格模板渲染到HTML文件中
        :return: 渲染后的HTML代码字符串
        '''
        env = Environment(loader = FileSystemLoader(self.tpl_dir))
        tpl = env.get_template(self.tpl_file)

        render_content = tpl.render(title = self.title, keys = self.keys, data_dicts = self.data_dicts)
        print '[render] render finished'
        return render_content
        
def sample():
    '''
    测试
    '''
    title = ['姓名', '年龄', '成绩']
    keys = ['name', 'age', 'score']
    data_dicts = [
        {
            'name': 'Tom',
            'age': 20,
            'score': 90
        },
        {
            'name': 'John',
            'age': 22,
            'score': 88
        },
        {
            'name': 'Jane',
            'age': 19,
            'score': 95
        }
    ]
    render = TableTplRender(title, keys, data_dicts)
    with open('result.html', 'w+') as fout:
        fout.write(render.render())
    
if __name__ == '__main__':
    sample()
    print 'end'
