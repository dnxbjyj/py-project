# coding:utf-8
# 分词操作工具函数
import sys
import jieba
from collections import Counter

# 对一段文本进行分词，并过滤掉长度小于2的词（标点、虚词等），用全模式分词
def cut_text(text):
    cut_list = jieba.cut(text.lower())
    return [word for word in cut_list if len(word) >= 2]
    
# 统计出一段文本中出现数量最多的前n个关键词及数量
def get_topn_words(text,topn):
    cut_list = cut_text(text)
    counter = Counter(cut_list)
    return counter.most_common(topn)

if __name__ == '__main__':
    # 设置字节流编码方式为utf-8
    reload(sys)
    sys.setdefaultencoding('utf-8')
    
    s = u'我想和女朋友一起去北京故宫博物院参观和闲逛。'
    # print cut_text(s)
    print get_topn_words(s,5)