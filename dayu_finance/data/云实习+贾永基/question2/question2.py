# coding:utf-8
# 题目描述：读取data里的600036这只股票的DataFrame,将其收盘价转换成用Numpy的Array格式，并用talib计算10日均线值，返回ndarray的最后五个值
import pandas as pd
import numpy as np
import talib

def solution():
    # 读取Excel文件
    xlsx_file = pd.ExcelFile('sz50.xlsx')
    # 读取600036.XSHG股票的数据
    dataframe = xlsx_file.parse('600036.XSHG')
    # 读取收盘价（close）的Series对象
    close_price_series = dataframe['close']
    # 转为收盘价的ndarray对象
    close_price_array = np.array(close_price_series)
    # 计算10日均线值
    close_price_sma = talib.SMA(close_price_array,10)
    # 打印出10日均线值的最后5个值
    print close_price_sma[-5:]

if __name__ == '__main__':
    solution()