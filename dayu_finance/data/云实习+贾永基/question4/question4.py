# coding:utf-8
# 用talib计算50只股票的周期为5的ROCR100，生成Dataframe，并将前5只股票的ROCR100（参数timeperiod=20）用一张图显示出来
import pandas as pd
from pandas import DataFrame
from pandas import Series
import talib
import numpy as np
from collections import OrderedDict
import matplotlib.pyplot as plt

def solution():
    # 读取Excel文件
    xlsx_file = pd.ExcelFile('sz50.xlsx')
    # 构建以股票代码为key的字典
    excel_data = OrderedDict()
    for sheet_name in xlsx_file.sheet_names:
        excel_data[sheet_name] = xlsx_file.parse(sheet_name)
    
    # 1. 计算50只股票的周期为5的ROCR100，生成Dataframe
    # rocr100_dateframe即为50只股票的周期为5的ROCR100 DataFrame数据
    rocr100_dateframe = get_rocr100_dataframe(excel_data,5)
    
    # 2. 将前5只股票的ROCR100（参数timeperiod=20）用一张图显示出来
    first_five_rocr100_dataframe = get_rocr100_dataframe(excel_data,20).ix[:,:5]
    
    #绘图
    first_five_rocr100_dataframe.plot()
    plt.show()
    

def get_rocr100_dataframe(excel_data,timeperiod):
    '''
    从Excel表格数据获取指定周期的ROCR100 DataFrame
    '''
    
    rocr100_dict = OrderedDict()
    for key,stock in excel_data.items():
        if 'close' in stock and 'datetime' in stock:
            rocr100 = talib.ROCR100(np.array(stock['close']),timeperiod = timeperiod) 
            rocr100_series = Series(rocr100,index = stock['datetime'])
            rocr100_dict[key] = rocr100_series
    rocr100_dateframe = DataFrame(rocr100_dict)
    return rocr100_dateframe
    
if __name__ == '__main__':
    solution()