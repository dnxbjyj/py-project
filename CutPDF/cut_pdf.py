# coding:utf-8
# 切割PDF文件
from __future__ import unicode_literals
from PyPDF2 import PdfFileReader as reader,PdfFileWriter as writer
import ConfigParser
import os
from collections import OrderedDict

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class PDFPages(object):
    '''
    PDF文件页面处理类
    '''
    def __init__(self,pdf_file_path):
        '''
        用一个PDF文件路径初始化
        
        :param pdf_file_path: PDF文件路径
        '''
        # 读取PDF
        pdf = reader(pdf_file_path)
        # PDF页面列表对象
        self.pages = pdf.pages
        # PDF写对象
        self.pdf_writer = writer()
        # 当前已保存的页码总数，初始化为0
        self.saved_page_num = 0
    def __getitem__(self,item):
        '''
        支持切片语法获取页面对象，page_num从0开始
        
        :param item: 数字或slice对象
        '''
        return self.pages[item]
        
    def __save_page(self,page_num):
        '''
        保存指定页码的页面对象到self.pdf_writer对象，page_num从0开始
        
        :param page_num: 页码，从0开始
        '''
        self.pdf_writer.addPage(self[page_num])
        
    def save_pages(self,page_num_seq):
        '''
        保存多个页面对象到self.pdf_writer对象，页码从0开始
        
        :param page_num_seq: 页码序列，格式：'0,3-7,12'
        '''
        if not page_num_seq:
            return
        
        seqs = page_num_seq.split(',')
        for seq in seqs:
            if '-' in seq:
                start = int(seq.split('-')[0])
                end = int(seq.split('-')[1])
                for i in range(start,end + 1):
                    self.__save_page(i)
                # 当前已保存的页面总数+(end - start + 1)
                self.saved_page_num += (end - start + 1)
            else:
                self.__save_page(int(seq))
                # 当前已保存的页面总数+1
                self.saved_page_num += 1
    
    def save_pages_with_bookmark(self,book_mark,page_num_seq):
        '''
        附带书签，保存一个或多个连续的页面对象到self.pdf_writer对象，页码从0开始

        :param book_mark: 书签字符串
        :param page_num_seq: 页码序列，只支持单个页码范围，不支持多个，格式：'0'，或'3-7'
        '''
        if not book_mark or not page_num_seq:
            return
        
        if '-' in page_num_seq:
            start = int(page_num_seq.split('-')[0])
            end = int(page_num_seq.split('-')[1])
            for i in range(start,end + 1):
                self.__save_page(i)
            # 添加书签
            self.pdf_writer.addBookmark(book_mark,self.saved_page_num)
            # 当前已保存的页面总数+(end - start + 1)
            self.saved_page_num += (end - start + 1)
        else:
            page = int(page_num_seq)
            self.__save_page(page)
            # 添加书签
            self.pdf_writer.addBookmark(book_mark,self.saved_page_num)
            # 当前已保存的页面总数+1
            self.saved_page_num += 1
        
    def save_as_file(self,file_name):
        '''
        把保存的PDF页面另存为一个新的PDF文件
        
        :param file_name: 指定的PDF文件名
        '''
        with open(file_name,'wb') as fout:
            self.pdf_writer.write(fout)

def basename(file_path):
    '''
    获取一个文件的文件名（不带后缀名）
    
    :param file_path: 文件路径
    '''
    return '.'.join(os.path.basename(file_path).split('.')[:-1])
            
def sample():
    config = ConfigParser.SafeConfigParser()
    config.read('./pdf_info.conf')
    # PDF文件根路径
    pdf_root_path = config.get('path','root_path')
    # PDF(文件名,文件路径列表)
    pdf_file_paths = [(basename(path),os.path.join(pdf_root_path,path)) for path in os.listdir(pdf_root_path)]
    
    for pdf in pdf_file_paths:
        name = pdf[0]
        path = pdf[1]
        
        # 创建PDFPages对象
        pages = PDFPages(path)
        
        # 以name为section的书签配置项key列表
        bookmarks = config.options(name)
        for bookmark in bookmarks:
            # 页码（范围）
            page_seq = config.get(name,bookmark)
            # 添加带书签的页面
            pages.save_pages_with_bookmark(bookmark.upper(),page_seq)
        # 把pages对象保存成文件
        pages.save_as_file('{name}-CONCEPT CHECKERS.pdf'.format(name = name))
        print 'finish {name}'.format(name = name)
        # 删除pages对象
        del pages
    print 'end'

if __name__ == '__main__':
    sample()