# coding:utf-8
# 用talib计算50只股票的周期为5的ROCR100，生成Dataframe，并将前5只股票的ROCR100（参数timeperiod=20）用一张图显示出来
import pandas as pd
from pandas import Series
from pandas import DataFrame
import numpy as np
import talib
import matplotlib.pyplot as plt
from collections import OrderedDict

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
    
    # 收盘价序列
    close_price_series = Series(dataframe['close'].values,index = dataframe['datetime'].values)
    # 收盘价MA序列
    close_price_sma_series = Series(close_price_sma,index = dataframe['datetime'].values)
    # 合并收盘价和MA数据
    merged_data = OrderedDict()
    merged_data['close_price'] = close_price_series
    merged_data['MA'] = close_price_sma_series
    merged_dataframe = DataFrame(merged_data)
    
    # 绘图
    merged_dataframe.plot()
    plt.show()

if __name__ == '__main__':
    solution()