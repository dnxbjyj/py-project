# coding:utf-8
# 题目描述：下载并用pandas导入sz50.xlsx的所有股票，索引设置为datetime，将所有股票的keys打印出来
import pandas as pd

def solution():
    # 读取Excel文件
    xlsx_file = pd.ExcelFile('sz50.xlsx')
    # 构建以股票代码为key的字典
    data = {sheet_name:xlsx_file.parse(sheet_name) for sheet_name in xlsx_file.sheet_names}
    # 打印出所有股票的key
    print data.keys()

if __name__ == '__main__':
    solution()