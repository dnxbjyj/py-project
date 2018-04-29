# coding:utf-8
# 一个基于Flask和SQLAlchemy+SQLite的极简博客应用
from __future__ import unicode_literals
from flask import Flask,render_template,redirect,request,url_for
from flask_sqlalchemy import SQLAlchemy
import os

# 创建应用程序对象
app = Flask(__name__)
# 获取当前目录的绝对路径
basedir = os.path.abspath(os.path.dirname(__file__))
# sqlite数据库文件存放路径
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'app.sqlite')
# 创建数据库对象
db = SQLAlchemy(app)

class Blog(db.Model):
    '''
    博文数据模型
    '''
    # 主键ID
    id = db.Column(db.Integer,primary_key = True)
    # 博文标题
    title = db.Column(db.String(100))
    # 博文正文
    text = db.Column(db.Text)
    
    def __init__(self,title,text):
        '''
        初始化方法
        '''
        self.title = title
        self.text = text
        
@app.route('/')
def home():
    '''
    主页
    '''
    # 渲染首页HTML模板文件
    return render_template('home.html')

@app.route('/blogs/create',methods = ['GET', 'POST'])
def create_blog():
    '''
    创建博客文章
    '''
    if request.method == 'GET':
        # 如果是GET请求，则渲染创建页面
        return render_template('create_blog.html')
    else:
        # 从表单请求体中获取请求数据
        title = request.form['title']
        text = request.form['text']
        
        # 创建一个博文对象
        blog = Blog(title = title,text = text)
        db.session.add(blog)
        # 必须提交才能生效
        db.session.commit()
        # 创建完成之后重定向到博文列表页面
        return redirect('/blogs')

@app.route('/blogs',methods = ['GET'])
def list_notes():
    '''
    查询博文列表
    '''
    blogs = Blog.query.all()
    # 渲染博文列表页面目标文件，传入blogs参数
    return render_template('list_blogs.html',blogs = blogs)
        
@app.route('/blogs/update/<id>',methods = ['GET', 'POST'])
def update_note(id):
    '''
    更新博文
    '''
    if request.method == 'GET':
        # 根据ID查询博文详情
        blog = Blog.query.filter_by(id = id).first_or_404()
        # 渲染修改笔记页面HTML模板
        return render_template('update_blog.html',blog = blog)
    else:
        # 获取请求的博文标题和正文
        title = request.form['title']
        text = request.form['text']
        
        # 更新博文
        blog = Blog.query.filter_by(id = id).update({'title':title,'text':text})
        # 提交才能生效
        db.session.commit()
        # 修改完成之后重定向到博文详情页面
        return redirect('/blogs/{id}'.format(id = id))

@app.route('/blogs/<id>',methods = ['GET','DELETE'])
def query_note(id):
    '''
    查询博文详情、删除博文
    '''
    if request.method == 'GET':
        # 到数据库查询博文详情
        blog = Blog.query.filter_by(id = id).first_or_404()
        # 渲染博文详情页面
        return render_template('query_blog.html',blog = blog)
    else:
        # 删除博文
        blog = Blog.query.filter_by(id = id).delete()
        # 提交才能生效
        db.session.commit()
        # 返回204正常响应，否则页面ajax会报错
        return '',204
        
if __name__ == '__main__':
    # 以debug模式启动程序
    app.run(debug = True)