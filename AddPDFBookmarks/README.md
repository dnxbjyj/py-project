# 用Python为PDF文件批量添加书签

> 本文讲述的核心库：`PyPDF2`
> 官方文档：http://pythonhosted.org/PyPDF2/

平时看一些大部头的技术书籍，大多数都是PDF版的，而且有一些书籍是影印扫描版的，几百上千页的书，没有任何书签，想要找到一个章节的位置非常费劲。那么就想，能不能搞一个工具，来自动地为这些大部头的PDF书籍添加书签便于自己阅读呢？下面就是这样一个工具的开发过程。

# 为PDF文件添加一个最简单的书签
学习使用一个技术，我们都从最简单的开始入手。比如我现在想为一个名为`book.pdf`的PDF文件添加一个`Hello World`书签，该怎么做呢？show code：
```python
# coding:utf-8
# 往pdf文件中添加书签
from PyPDF2 import PdfFileReader as reader,PdfFileWriter as writer

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def main():
    # 读取PDF文件，创建PdfFileReader对象
    book = reader('./book.pdf')

    # 创建PdfFileWriter对象，并用拷贝reader对象进行初始化
    pdf = writer()
    pdf.cloneDocumentFromReader(book)

    # 添加书签
    # 注意：页数是从0开始的，中文要用unicode字符串，否则会出现乱码
    # 如果这里的页码超过文档的最大页数，会报IndexError异常
    pdf.addBookmark(u'Hello World! 你好，世界！',2)

    # 保存修改后的PDF文件内容到文件中
    with open('./book-with-bookmark.pdf','wb') as fout:
        pdf.write(fout)

if __name__ == '__main__':
    main()
```
运行上述代码，发现当前目录下生成了一个名为`book-with-bookmark.pdf`的文件，打开这个文件，看到成功添加了一个书签：
![](http://upload-images.jianshu.io/upload_images/8819542-2b7e97382c072042.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
点击这个书签，会自动跳转到第3页。

# PDF处理工具类
下面先编写一个功能更为丰富的PDF处理工具类，代码如下：
```python
# coding:utf-8
# 封装的PDF文档处理工具
from PyPDF2 import PdfFileReader as reader,PdfFileWriter as writer
import os

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class PDFHandleMode(object):
    '''
    处理PDF文件的模式
    '''
    # 保留源PDF文件的所有内容和信息，在此基础上修改
    COPY = 'copy'
    # 仅保留源PDF文件的页面内容，在此基础上修改
    NEWLY = 'newly'

class MyPDFHandler(object):
    '''
    封装的PDF文件处理类
    '''
    def __init__(self,pdf_file_path,mode = PDFHandleMode.COPY):
        '''
        用一个PDF文件初始化
        :param pdf_file_path: PDF文件路径
        :param mode: 处理PDF文件的模式，默认为PDFHandleMode.COPY模式
        '''
        # 只读的PDF对象
        self.__pdf = reader(pdf_file_path)

        # 获取PDF文件名（不带路径）
        self.file_name = os.path.basename(pdf_file_path)
        #
        self.metadata = self.__pdf.getXmpMetadata()
        #
        self.doc_info = self.__pdf.getDocumentInfo()
        #
        self.pages_num = self.__pdf.getNumPages()

        # 可写的PDF对象，根据不同的模式进行初始化
        self.__writeable_pdf = writer()
        if mode == PDFHandleMode.COPY:
            self.__writeable_pdf.cloneDocumentFromReader(self.__pdf)
        elif mode == PDFHandleMode.NEWLY:
            for idx in range(self.pages_num):
                page = self.__pdf.getPage(idx)
                self.__writeable_pdf.insertPage(page, idx)

    def save2file(self,new_file_name):
        '''
        将修改后的PDF保存成文件
        :param new_file_name: 新文件名，不要和原文件名相同
        :return: None
        '''
        # 保存修改后的PDF文件内容到文件中
        with open(new_file_name, 'wb') as fout:
            self.__writeable_pdf.write(fout)
        print 'save2file success! new file is: {0}'.format(new_file_name)

    def add_one_bookmark(self,title,page,parent = None, color = None,fit = '/Fit'):
        '''
        往PDF文件中添加单条书签，并且保存为一个新的PDF文件
        :param str title: 书签标题
        :param int page: 书签跳转到的页码，表示的是PDF中的绝对页码，值为1表示第一页
        :paran parent: A reference to a parent bookmark to create nested bookmarks.
        :param tuple color: Color of the bookmark as a red, green, blue tuple from 0.0 to 1.0
        :param list bookmarks: 是一个'(书签标题，页码)'二元组列表，举例：[(u'tag1',1),(u'tag2',5)]，页码为1代表第一页
        :param str fit: 跳转到书签页后的缩放方式
        :return: None
        '''
        # 为了防止乱码，这里对title进行utf-8编码
        self.__writeable_pdf.addBookmark(title.decode('utf-8'),page - 1,parent = parent,color = color,fit = fit)
        print 'add_one_bookmark success! bookmark title is: {0}'.format(title)

    def add_bookmarks(self,bookmarks):
        '''
        批量添加书签
        :param bookmarks: 书签元组列表，其中的页码表示的是PDF中的绝对页码，值为1表示第一页
        :return: None
        '''
        for title,page in bookmarks:
            self.add_one_bookmark(title,page)
        print 'add_bookmarks success! add {0} pieces of bookmarks to PDF file'.format(len(bookmarks))

    def read_bookmarks_from_txt(self,txt_file_path,page_offset = 0):
        '''
        从文本文件中读取书签列表
        文本文件有若干行，每行一个书签，内容格式为：
        书签标题 页码
        注：中间用空格隔开，页码为1表示第1页
        :param txt_file_path: 书签信息文本文件路径
        :param page_offset: 页码便宜量，为0或正数，即由于封面、目录等页面的存在，在PDF中实际的绝对页码比在目录中写的页码多出的差值
        :return: 书签列表
        '''
        bookmarks = []
        with open(txt_file_path,'r') as fin:
            for line in fin:
                line = line.rstrip()
                if not line:
                    continue
                # 以'@'作为标题、页码分隔符
                print 'read line is: {0}'.format(line)
                try:
                    title = line.split('@')[0].rstrip()
                    page = line.split('@')[1].strip()
                except IndexError as msg:
                    print msg
                    continue
                # title和page都不为空才添加书签，否则不添加
                if title and page:
                    try:
                        page = int(page) + page_offset
                        bookmarks.append((title, page))
                    except ValueError as msg:
                        print msg

        return bookmarks

    def add_bookmarks_by_read_txt(self,txt_file_path,page_offset = 0):
        '''
        通过读取书签列表信息文本文件，将书签批量添加到PDF文件中
        :param txt_file_path: 书签列表信息文本文件
        :param page_offset: 页码便宜量，为0或正数，即由于封面、目录等页面的存在，在PDF中实际的绝对页码比在目录中写的页码多出的差值
        :return: None
        '''
        bookmarks = self.read_bookmarks_from_txt(txt_file_path,page_offset)
        self.add_bookmarks(bookmarks)
        print 'add_bookmarks_by_read_txt success!'

```
`MyPDFHandler`类可以用一个PDF对象进行初始化，支持从一个txt文件中读取要添加的书签列表，然后根据这个书签列表自动为PDF添加书签，书签列表txt文件是类似这样格式的文件，书签标题和页码（一个整数，代表书签的相对页码数，可以为负数）用`@`作为分隔符隔开：
```
目录@-5
【第一篇 开发基础】@1
第1章 Eclipse平台简介@1
    1.1 Eclipse集成开发环境（IDE）介绍@2
    1.2 什么是Eclipse@9
    1.3 SWT/JFace技术@11
    1.4 插件技术和OSGi@12
    1.5 RCP技术@15
    1.6 EMF技术@16
    1.7 GEF技术@17
```

# 编写书签列表txt文件
从网上找到一本大部头的书籍`Eclipse插件开发学习笔记.pdf`，这是一本非常好的Eclipse插件开发入门书籍，但是是扫描版的，没有任何书签，看起来比较费劲。

这是这本书的目录：
![](http://upload-images.jianshu.io/upload_images/8819542-c4491ce0c7b13e17.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

下面手工将目录内容和页码信息录入添加书签所需的书签列表文本文件中（`bookmarks-eclipse_plutin.txt`）：
```
[meta]
page_offset = 11

目录@-5
【第一篇 开发基础】@1
第1章 Eclipse平台简介@1
    1.1 Eclipse集成开发环境（IDE）介绍@2
    1.2 什么是Eclipse@9
    1.3 SWT/JFace技术@11
    1.4 插件技术和OSGi@12
    1.5 RCP技术@15
    1.6 EMF技术@16
    1.7 GEF技术@17

第2章 SWT/JFace概述@19

第3章 SWT编程基础@39

第4章 使用基本控件与对话框@64

第5章 容器与布局管理器@92

第6章 界面开发工具@121

第7章 高级控件使用@135

第8章 SWT/JFace的事件处理@166

【第二篇 核心技术】@183
第9章 Eclipse插件体系结构@183
    9.1 Eclipse体系结构@184
    9.2 插件的加载过程@187
    9.3 插件的扩展模式@191

第10章 开发第一个插件项目@196
    10.1 创建插件工程@197
    10.2 "插件开发"透视图@200
    10.3 插件工程结构@203
    10.4 插件文件@204
    10.5 插件类@207
    10.6 运行插件程序@208
    10.7 调试插件@210
    10.8 发布插件@211

第11章 操作（Actions）@213
    11.1 Eclipse中的操作概览@214
    11.2 添加工作台窗口操作@214
    11.3 IAction与IActionDelegate接口@222
    11.4 对象操作@224
    11.5 视图操作@230
    11.6 编辑器操作@234
    11.7 快捷键映射@237

第12章 视图（Views）@241
    12.1 Eclipse视图体系结构概览@242
    12.2 Eclipse工作环境中的视图@243
    12.3 创建一个视图@248
    12.4 视图类@250
    12.5 为视图添加操作@260
    12.6 视图间通信@265
    12.7 添加状态栏支持@272
    12.8 视图状态@273
    12.9 加载和卸载图标@279

第13章 编辑器（Editors）@282
    13.1 Eclipse编辑器体系结构概览@283
    13.2 Eclipse工作环境中的编辑器@284
    13.3 为例子增加一个编辑器@289
    13.4 编辑器使用的数据模型@294
    13.5 编辑器页面@301
    13.6 响应编辑器更改@313
    13.7 保存编辑器模型@318
    13.8 编辑器生命周期@322
    13.9 为编辑器添加操作@326

第14章 透视图（Perspectives）@334
    14.1 什么是透视图@335
    14.2 创建一个透视图@336
    14.3 IPageLayout@339
    14.4 填充透视图@341
    14.5 扩展现有透视图@344

第15章 对话框和向导@349
    15.1 对话框和向导概述@350
    15.2 对话框类别@350
    15.3 为例子增加SWT对话框@354
    15.4 创建JFace对话框@355
    15.5 向导介绍@362
    15.6 添加向导@364

第16章 首选项（Preferences）@379
    16.1 首选项页面结构@381
    16.2 添加首选项页面@382
    16.3 示例首选项@383
    16.4 为例子创建首选项页面@387

第17章 帮助内容（Help Contents）@397

第18章 备忘单（CheatSheet）@410

【第三篇 高级进阶】@426
第19章 插件开发高级内容@426

第20章 富客户端平台（RCP）技术@473

第21章 Draw2d@509

第22章 GEF介绍与实现@526

【第四篇 综合实例】@586
第23章 插件开发实例@586

第24章 GEF实例@630
```
注：一开始的`page_offset `的值表示书签页码的偏移量，即某一页所在的实际页码与PDF目录中所写的页码值的差值，这是考虑到在PDF的目录页之前还会有其他的一些封面、前言等页面，实际页码会和目录中所写的页码不一致。

# 为PDF批量添加书签
上面的准备工作就做好了，下面来开始为`Eclipse插件开发学习笔记.pdf`这本书添加目录：
```python
# coding:utf-8
# 添加PDF书签
from pdf_utils import MyPDFHandler,PDFHandleMode as mode
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def main():
    pdf_handler = MyPDFHandler(u'Eclipse插件开发学习笔记.pdf',mode = mode.NEWLY)
    pdf_handler.add_bookmarks_by_read_txt('./bookmarks-eclipse_plutin.txt',page_offset = 11)
    pdf_handler.save2file(u'Eclipse插件开发学习笔记-目录书签版.pdf')

if __name__ == '__main__':
    main()
```
运行上面代码，发现在当前目录生成了一个名为`'Eclipse插件开发学习笔记-目录书签版.pdf`的文件，打开它，看到书签已经全部完美地添加了进去，并且点击各个书签页面跳转的位置也是正确的，大大地方便了平时的阅读：
![](http://upload-images.jianshu.io/upload_images/8819542-33d2ffaac6d5e3ab.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


# 本文代码GitHub地址
本文涉及到的代码都放在了[本人的GitHub](https://github.com/dnxbjyj/py-project/tree/master/AddPDFBookmarks)