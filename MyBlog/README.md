# Flask从HelloWorld到增删改查

> 参考：https://github.com/basco-johnkevin/note-taking-app

Flask是Python的一个轻量的Web框架，开发Web应用简单快速。本文就用一个Hello World演示程序和支持增删改查操作的极简博客Web应用来探索Flask的基本用法，以及与之相关的种种技术。

# 用到的库和安装方法
### flask库
本文的主角，一个轻量的Web框架，安装方式：`pip install flask`
### flask-sqlalchemy库
这是flask的一个数据库ORM（对象关系映射）库，封装了一系列对数据库的操作API，安装方式：`pip install flask-sqlalchemy`
### sqlite
sqlite是一个轻量型的关系型数据库，Python 2.5+版本自带sqlite数据库，不需要额外安装。

# Flask Hello World
将以下代码保存为`hello.py`并运行：
```python
# coding:utf-8
# Hello World
from __future__ import unicode_literals
from flask import Flask

# 创建应用程序对象
app = Flask(__name__)

@app.route('/')
def hello():
    '''
    hello请求
    '''
    # 直接返回字符串
    return 'Hello, Flask World!'
        
if __name__ == '__main__':
    # 以debug模式启动程序
    app.run(debug = True)
```
打开浏览器，在地址栏输入：`http://127.0.0.1:5000/`， 可以看到如下页面：
![](https://upload-images.jianshu.io/upload_images/8819542-4f7c8a7b60186ec3.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
我们的Hello World程序就完成了，因为开启了debug调试模式，所在在命令行中也可以看到发送的请求的日志：
![](https://upload-images.jianshu.io/upload_images/8819542-e1d14121098a0fc9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

开启debug模式的好处在于，每次对源代码的修改，保存一下刷新页面都可以立即生效，而不用重启程序。

# 一个支持增删改查操作的极简博客MyBlog
下面用`flask+sqlalchemy+sqlite`来编写一个极简的博客系统，麻雀虽小，五脏俱全，包含增删改查、数据库操作、Jinja2页面模板渲染、HTML表单操作、ajax请求发送等。
### 初始化程序和数据库
在一开始，需要做一些初始化的操作，包括初始化app对象和数据库。在当前目录创建一个文件`blog.py`，在其中写如下代码：
```python
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
```

### 定义博客文章数据Model类
初始化工作做完之后，下面需要定义一个数据库表的Model类`Blog`，以完成数据库表和数据对象之间的关系映射：
```python
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
```

### 创建sqlite数据库
在运行程序之前，还需创建sqlite数据库，它以一个文件的形式存放。如果不事先创建数据库，那么在运行程序的时候如果发送涉及数据库操作的请求就会报数据库异常。

打开命令行，切换到`blog.py`文件所在目录，打开`python`控制台，执行如下命令来创建sqlite数据库文件、创建数据库表：
```python
from blog import db
db.create_all()
```
注：此操作只需做一次。

### 使用模板渲染首页
先定义一个接口，用来接收首页请求：
```python
@app.route('/')
def home():
    '''
    主页
    '''
    # 渲染首页HTML模板文件
    return render_template('home.html')
```

然后在和`blog.py`文件同级目录下创建一个名为`templates`的文件夹，并在其中创建一个`home.html`文件，内容如下：
```html
<h1>我的博客</h1>
<a href="/blogs">博文列表</a>
<br>
<a href="/blogs/create">去写一篇博客</a>
<br>
```
flask在运行的时候，会去`templates`目录查找页面模板文件，渲染页面。下面我们运行`blog.py`，在浏览器中访问`http://127.0.0.1:5000`，就可以看到首页的效果了：
![](https://upload-images.jianshu.io/upload_images/8819542-a04ee2659c2e6f1b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

### 博文列表和Jinja2渲染引擎
上述首页中是有一个`博文列表`的链接的，但是我们还没有实现链接需要跳转到的博文列表页面，下面来实现这个页面。

在`blog.py`中新增一个请求方法，用于接收查询博文列表的请求：
```python
@app.route('/blogs',methods = ['GET'])
def list_notes():
    '''
    查询博文列表
    '''
    blogs = Blog.query.all()
    # 渲染博文列表页面目标文件，传入blogs参数
    return render_template('list_blogs.html',blogs = blogs)
```
这里返回了一个`blogs`列表对象，用于在HTML页面中获取并展示博文数据。

然后在`templates`目录下创建一个`list_blogs.html`文件，内容如下：
```html
<h3><a href="/">< 回到首页</a></h3>
<h1>博文列表</h1>
<!-- Jinja模板语法 -->
{% if blogs %}
    {% for blog in blogs%}
        <h3><a href="/blogs/{{blog.id}}">{{blog.title}}</a></h3>
    {% endfor %}
{% else %}
    <p>还没有一篇博文，去写一篇吧~</p>
    <a href="/blogs/create">去写一篇</a>
{% endif %}
```
`list_blogs.html`中用到了几个模板渲染语法，用来展示后台返回的数据。

在浏览器中访问`http://127.0.0.1:5000/blogs`，可以看到如下效果：
![](https://upload-images.jianshu.io/upload_images/8819542-3a708e87f2bac82f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

### 博文创建和HTML表单操作
在`blog.py`中新增一个请求方法，用于接收创建博文的请求，这个方法接收GET和POST两种请求，分别用于渲染创建博文的页面和执行创建博文的操作：
```python
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
```
然后在`templates`目录下创建一个`create_blog.html`文件：
```html
<h1>写博文</h1>
<!-- HTML表单 -->
<form action="/blogs/create" method="POST">
    <label>标题：</label>
    <input type="text" name="title">
    <br><br>
    <label>正文：</label>
    <input type="text" name="text">
    <br><br>
    <input type="submit" value="创建">
</form>
```
这里用到了HTML表单，来下发请求数据。

在浏览器中访问`http://127.0.0.1:5000/blogs/create`进入写博文页面：
![](https://upload-images.jianshu.io/upload_images/8819542-fa4d12a782f4f384.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

填入博文标题和正文，然后点击`创建`按钮，就跳转到博文列表页面，新创建的博文就显示在列表中了：
![](https://upload-images.jianshu.io/upload_images/8819542-c0af70b75ecd6906.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![](https://upload-images.jianshu.io/upload_images/8819542-e8fffb063cd0297e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

### 博文详情、删除和ajax请求发送
在`blog.py`中新增一个方法：
```python
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
```
在`templates`目录新增一个`query_blog.html`文件，用于展示博文详情，和定义删除操作，内容如下：
```html
<h3><a href="/blogs">< 回到博文列表</a></h3>
<h1>博文详情</h1>
<div>
    <a href="/blogs/update/{{blog.id}}" id="{{blog.id}}">更新</a>
    <h3>{{blog.title}}</h3>
    <p>{{blog.text}}</p>
    <a href="#" class="btn-delete" id="{{blog.id}}">删除</a>
</div>

<!-- 先引入jquery，下面要用到-->
<script src="https://cdn.bootcss.com/jquery/1.12.4/jquery.min.js"></script>
<!--发送ajax请求删除博文 -->
<script type="text/javascript">
    $('a.btn-delete').on('click',function(evt){
        // 通知浏览器不要执行与事件关联的默认动作
        evt.preventDefault();
        // 获取博文ID
        var blogid = $(this).attr('id');
        $.ajax({
            // 请求URL
            url: "/blogs/" + blogid,
            // 请求方法类型
            type: "DELETE",
            contentType:"application/json",
            // 删除成功响应函数
            success:function(resp){
                // 在当前页面打开博文列表页面
                window.open("/blogs","_self");
            },
            // 删除失败响应函数
            error:function(resp){
                // 删除失败，给出错误提示
                alert("删除博文失败！详情：" + resp.message);
            }
        })
    });
</script>
```
在这里使用到了jquery的ajax请求来发送删除博文的请求，博文删除成功后，跳转到博文列表页面。

在博文列表页面点击刚刚创建的博文的标题，就跳转到了博文详情页面：
![](https://upload-images.jianshu.io/upload_images/8819542-04869212827ff1c3.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

点击`删除`按钮，博文就被删除了，然后跳转到了博文列表页面：
![](https://upload-images.jianshu.io/upload_images/8819542-52af4b4d5214fd19.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

### 博文更新
在`blog.py`中新增一个请求方法：
```python
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
```
在`templates`目录下新增一个`update_blog.html`文件，内容如下：
```html
<h1>更新博文</h1>
<!-- HTML表单 -->
<form action="/blogs/update/{{blog.id}}" method="POST">
    <label>标题：</label>
    <input type="text" name="title" value="{{blog.title}}">
    <br><br>
    <label>正文：</label>
    <input type="text" name="text" value="{{blog.text}}">
    <br><br>
    <input type="submit" value="提交">
</form>
```
在博文详情页面，点击`更新`按钮，进入更新博文页面：
![](https://upload-images.jianshu.io/upload_images/8819542-705f81956b482250.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![](https://upload-images.jianshu.io/upload_images/8819542-f9a33f8ac88b8af3.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

更新博文的标题或正文之后，点击`提交`按钮，更新博文成功，跳转到博文详情页面：
![](https://upload-images.jianshu.io/upload_images/8819542-55e8de96c6231280.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

### 完整代码
* 代码结构
![](https://upload-images.jianshu.io/upload_images/8819542-10b6ce0d37c42637.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

* `blog.py`
```python
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
```

* `home.html`
```html
<h1>我的博客</h1>
<a href="/blogs">博文列表</a>
<br>
<a href="/blogs/create">去写一篇博客</a>
<br>
```

* `create_blog.html`
```html
<h1>写博文</h1>
<!-- HTML表单 -->
<form action="/blogs/create" method="POST">
    <label>标题：</label>
    <input type="text" name="title">
    <br><br>
    <label>正文：</label>
    <input type="text" name="text">
    <br><br>
    <input type="submit" value="创建">
</form>
```

* `list_blogs.html`
```html
<h3><a href="/">< 回到首页</a></h3>
<h1>博文列表</h1>
<!-- Jinja模板语法 -->
{% if blogs %}
    {% for blog in blogs%}
        <h3><a href="/blogs/{{blog.id}}">{{blog.title}}</a></h3>
    {% endfor %}
{% else %}
    <p>还没有一篇博文，去写一篇吧~</p>
    <a href="/blogs/create">去写一篇</a>
{% endif %}
```

* `query_blog.html`
```html
<h3><a href="/blogs">< 回到博文列表</a></h3>
<h1>博文详情</h1>
<div>
    <a href="/blogs/update/{{blog.id}}" id="{{blog.id}}">更新</a>
    <h3>{{blog.title}}</h3>
    <p>{{blog.text}}</p>
    <a href="#" class="btn-delete" id="{{blog.id}}">删除</a>
</div>

<!-- 先引入jquery，下面要用到-->
<script src="https://cdn.bootcss.com/jquery/1.12.4/jquery.min.js"></script>
<!--发送ajax请求删除博文 -->
<script type="text/javascript">
    $('a.btn-delete').on('click',function(evt){
        // 通知浏览器不要执行与事件关联的默认动作
        evt.preventDefault();
        // 获取博文ID
        var blogid = $(this).attr('id');
        $.ajax({
            // 请求URL
            url: "/blogs/" + blogid,
            // 请求方法类型
            type: "DELETE",
            contentType:"application/json",
            // 删除成功响应函数
            success:function(resp){
                // 在当前页面打开博文列表页面
                window.open("/blogs","_self");
            },
            // 删除失败响应函数
            error:function(resp){
                // 删除失败，给出错误提示
                alert("删除博文失败！详情：" + resp.message);
            }
        })
    });
</script>

```

* `update_blog.html`
```html
<h1>更新博文</h1>
<!-- HTML表单 -->
<form action="/blogs/update/{{blog.id}}" method="POST">
    <label>标题：</label>
    <input type="text" name="title" value="{{blog.title}}">
    <br><br>
    <label>正文：</label>
    <input type="text" name="text" value="{{blog.text}}">
    <br><br>
    <input type="submit" value="提交">
</form>
```

# MyBlog所涉及的技术点及参考资料
### flask
* 在线文档：http://docs.jinkan.org/docs/flask/
* flask范例：http://www.pythondoc.com/flask/patterns/index.html

### flask-sqlalchemy
* 在线文档：http://flask-sqlalchemy.pocoo.org/2.3/

### sqlite
* 在线文档：http://www.sqlite.org/docs.html

### jinja2
* 在线文档：http://jinja.pocoo.org/docs/dev/
* 模板渲染常用用法：https://blog.csdn.net/GeekLeee/article/details/52505605

### ajax
* 一个例子：http://www.pythondoc.com/flask/patterns/jquery.html

# 总结
本文用flask框架加上sqlite数据库实现了一个极简的博客应用，每一个模块都非常非常简单，但是却包含了很多的知识点，可以以本文这个简单的Demo为起点，继续深入学习下去。

---
本文代码存放路径：[我的GitHub](https://github.com/dnxbjyj/py-project/tree/master/MyBlog)