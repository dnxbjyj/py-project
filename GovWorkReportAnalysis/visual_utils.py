# coding:utf-8
import matplotlib.pyplot as plt

# 指定默认字体，防止画图时中文乱码
plt.rcParams['font.sans-serif'] = ['SimHei']  

# 传入一组关键词及词频列表，从高到低绘出每个关键词频率的散点图
# keywords示例：[(u'张三',10),(u'李四',12),(u'王五',7)]
def draw_keywords_scatter(keywords,title = None,xlabel = None,ylabel = None):
    # 先对keywords按词频从高到低排序
    keywords = sorted(keywords,key = lambda item:item[1],reverse = True)

    # 解析出关键词列表
    words = [x[0] for x in keywords]
    # 解析出对应的词频列表
    times = [x[1] for x in keywords]
    
    x = range(len(keywords))
    y = times
    plt.plot(x, y, 'b^')
    plt.xticks(x, words, rotation=45)
    plt.margins(0.08)
    plt.subplots_adjust(bottom=0.15)
    # 图表名称
    plt.title(title)
    # x,y轴名称
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()
    
def main():
    draw_keywords_scatter([(u'张三',10),(u'李四',12),(u'王五',7)],u'出勤统计图',u'姓名',u'出勤次数')
    
if __name__ == '__main__':
    main()
    