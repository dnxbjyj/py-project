# coding:utf-8
# 往pdf文件中添加书签
from PyPDF2 import PdfFileReader as reader,PdfFileWriter as writer

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def main():
    # 读取PDF文件，创建PdfFileReader对象
    book = reader('./book.pdf')

    # 创建PdfFileWriter对象，并用reader对象进行初始化
    pdf = writer()
    pdf.cloneDocumentFromReader(book)

    # 添加书签
    # 注意：页数是从0开始的，中文要用unicode字符串，否则会出现乱码
    # 如果这里的页码超过文档的最大页数，会报IndexError异常
    # 3表示书签链接到的页码数为第3页
    pdf.addBookmark(u'Hello World! 你好，世界！',3)

    # 保存修改后的PDF文件内容到文件中
    with open('./book-with-bookmark.pdf','wb') as fout:
        pdf.write(fout)

if __name__ == '__main__':
    main()