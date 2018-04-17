# coding:utf-8
# 三体三部曲全文文本分词分析
import jieba.posseg as psg
from collections import Counter
import sys

# 对文本分词并标注词性，并缓存到文件
def cut_and_cache(text):
    # 将三体全集文本分词，并附带上词性，因为数据量比较大，防止每次运行脚本都花大量时间，所以第一次分词后就将结果存入文件cut_result.txt中
    # 相当于做一个缓存，格式为每个词占一行，每一行的内容为：
    # 词,词性
    santi_words_with_attr = [(x.word,x.flag) for x in psg.cut(santi_text) if len(x.word) >= 2]
    print len(santi_words_with_attr)
    with open('cut_result.txt','w+') as f:
        for x in santi_words_with_attr:
            f.write('{0}\t{1}\n'.format(x[0],x[1]))    

# 从cut_result.txt中读取带词性的分词结果列表
def read_cut_result():
    santi_words_with_attr = []
    with open('cut_result.txt','r') as f:
        for x in f.readlines():
            pair = x.split()
            if len(pair) < 2:
                continue
            santi_words_with_attr.append((pair[0],pair[1]))
    return santi_words_with_attr

# 将分词列表的词性构建成一个字典，以便后面使用，格式为：
# {词:词性}
def build_attr_dict(santi_words_with_attr):
    attr_dict = {}
    for x in santi_words_with_attr:
        attr_dict[x[0]] = x[1]
    return attr_dict

#　统计在分词表中出现次数排名前500的词的列表，并将结果输出到文件result.txt中，每行一个词，格式为：
# 词,出现次数
def get_topn_words(words,topn):
    c = Counter(words).most_common(topn)
    with open('result.txt','w+') as f:
        for x in c:
            f.write('{0},{1}\n'.format(x[0],x[1]))
        
        
def main():
    # 设置环境为utf-8编码格式，防止处理中文出错
    reload(sys)
    sys.setdefaultencoding('utf-8')
    
    # 读取三体全集文本
    santi_text = open('./santi.txt').read()
    
    # 分词并缓存，只需运行一次，后续可注释掉
    cut_and_cache(santi_text)
    
    # 从cut_result.txt中读取带词性的分词结果列表
    santi_words_with_attr = read_cut_result()
    
    # 构建词性字典，这个字典在探索stop_attr的时候会有帮助
    # attr_dict = build_attr_dict(santi_words_with_attr)
    
    # 要过滤掉的词性列表
    stop_attr = ['a','ad','b','c','d','f','df','m','mq','p','r','rr','s','t','u','v','z']
    
    # 过滤掉不需要的词性的词
    words = [x[0] for x in santi_words_with_attr if x[1] not in stop_attr]
    
    # 获取topn的词并存入文件result.txt
    get_topn_words(words = words,topn = 500)
    
if __name__ == '__main__':
    main()