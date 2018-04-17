# 分析了《三体》全集，我看到了这样的三体

> jieba分词模块的基本用法参加我的另一篇博文：[好玩的分词（1）——python jieba分词模块的基本用法](http://www.jianshu.com/p/7ba4d177a2ea)

《三体》是一部很好看的硬科幻作品，当初是一口气把三部全都看完的，包括《三体1》、《三体2：黑暗森林》和《三体3：死神永生》，洋洋洒洒几十万字，看的叫一个酣畅淋漓。本文就使用jieba分词，对《三体》三部曲全集文本做一些有趣的分析，涉及到分词和词频分析等。

# 文本准备

到网上随便一搜"三体全集"，就很容易下载到三体三部曲的全集文本（txt文档大概有2~3Mb），这里重命名为santi.txt，并存放到当前目录下。

# 读取三体全集文本


```python
# coding:utf-8
import sys

# 设置环境为utf-8编码格式，防止处理中文出错
reload(sys)
sys.setdefaultencoding('utf-8')

# 读取三体全集文本
santi_text = open('./santi.txt').read()
```


```python
print len(santi_text)

# 输出：
'''
2681968
'''
```

可以看出文本的长度有2681968字节，数据量还是很庞大的，语料库足够丰富。

# 对文本分词并缓存到文件中

下面用`jieba.posseg`模块对文本进行分词并标注词性，这里标注词性的目的是为了后面接下来根据词性过滤掉那些没有实际意义的词（如'好的'、'一般'、'他的'等等这种词），而将分词结果缓存到文件中是为了提高每次运行脚本的效率，毕竟这么大的数据量，分词一次还是耗时很长的（大概为几分钟），缓存到文件中，只需第一次做一次分词，后面再运行脚本就只需从文件中读取分词结果即可，毕竟读文件的速度比分词要快很多。下面上代码：


```python
import jieba.posseg as psg

# 将三体全集文本分词，并附带上词性，因为数据量比较大，防止每次运行脚本都花大量时间，所以第一次分词后就将结果存入文件out.txt中
# 相当于做一个缓存，格式为每个词占一行，每一行的内容为：
# 词    词性
santi_words_with_attr = [(x.word,x.flag) for x in psg.cut(santi_text) if len(x.word) >= 2]  # 这里的x.word为词本身，x.flag为词性
print len(santi_words_with_attr)　　#　输出：
with open('out.txt','w+') as f:
    for x in santi_words_with_attr:
        f.write('{0}\t{1}\n'.format(x[0],x[1]))
```

运行上面一段代码，几分钟之后在当前目录生成了一个out.txt文件，有273033行，数据量还是非常大的，其前几行的内容如下：


```
手机	n
TXT	eng
小说	n
下载	v
www	eng
sjtxt	eng
com	eng
欢迎您	l
sjtxt	eng
推荐	v
好书	n
	x
	x
	x
```

看到这，肯定会说：这什么鬼!?!!! [黑人问号.gif]

不急，这是因为文本中存在大量的我们不需要的词，甚至还有很多空白符词，这肯定是没法玩的，所以接下来我们对垃圾词进行过滤，对数据做一下清洗。

# 分词结果清洗

现在我们缓存的分词结果文件out.txt就可以派上用场了，为了清洗分词结果，我们需要再次获取分词结果，而现在就不需要再运行一次超级耗时的分词代码了，而只需从out.txt中读取即可，上代码：


```python
# 从out.txt中读取带词性的分词结果列表
santi_words_with_attr = []
with open('out.txt','r') as f:
    for x in f.readlines():
        pair = x.split()
        if len(pair) < 2:
            continue
        santi_words_with_attr.append((pair[0],pair[1]))

# 将分词列表的词性构建成一个字典，以便后面使用，格式为：
# {词:词性}
attr_dict = {}
for x in santi_words_with_attr:
    attr_dict[x[0]] = x[1]

# 要过滤掉的词性列表，这些词性的词都是没有实际意义的词，如连词、代词等虚词，这个列表初始化为空列表，后面根据分析结果手工往里面一个个添加
stop_attr = []

# 获取过滤掉stop_attr里的词性的词后的分词列表
words = [x[0] for x in santi_words_with_attr if x[1] not in stop_attr]

#　统计在分词表中出现次数排名前500的词的列表，并将结果输出到文件most.txt中，每行一个词，格式为：
# 词,出现次数,词性
from collections import Counter
c = Counter(words).most_common(500)
with open('most.txt','w+') as f:
    for x in c:
        f.write('{0},{1},{2}\n'.format(x[0],x[1],attr_dict[x[0]]))
```

第一次运行上述代码，生成的most.txt文件有500行，前10行内容如下：


```
一个,3057,m
没有,2128,v
他们,1690,r
我们,1550,r
程心,1451,n
这个,1357,r
自己,1347,r
现在,1273,t
已经,1259,d
罗辑,1256,n
```

可以看到词频排名前四的都是些没意义的词，而第5个'程心'才是三体中有实际意义的词(程圣母果然厉害)。等等，这是因为我们没有将前四名这些词的词性添加到stop_attr列表中，导致它们并没有被过滤掉，那我们现在就把这前4个词的词性添加到stop_attr列表中，stop_attr列表变成：`['m','v','r']`，再次运行脚本，most.txt的内容(前10个词)变为了：


```
程心,1451,n
现在,1273,t
已经,1259,d
罗辑,1256,n
世界,1243,n
地球,951,n
人类,935,n
太空,930,n
三体,879,n
宇宙,875,n
```

可以看到，我们成功清洗掉了刚刚前四名的无意义的词，'程心'成功变为词频最高的词。但是第2、3名的'现在'、'已经'等词显然也是我们不需要的，那么就重复上面的过程，把这些不需要的词性添加到stop_attr列表中，再看结果。然后继续重复以上过程，重复N次之后，我得到的stop_attr变成了：`['a','ad','b','c','d','f','df','m','mq','p','r','rr','s','t','u','v','z']`，长长的一串。而most.txt的内容变为了(前20行)：


```
程心,1451,n
罗辑,1256,n
世界,1243,n
地球,951,n
人类,935,n
太空,930,n
三体,879,n
宇宙,875,n
太阳,775,ns
舰队,649,n
飞船,644,n
汪淼,633,nrfg
时间,611,n
文明,561,nr
东西,515,ns
信息,480,n
感觉,468,n
智子,452,n
计划,451,n
叶文洁,446,nr
太阳系,428,n
```

世界一下子明朗了，可以看出分词结果已经被清洗的很干净了，也可以发现我们需要的有实际意义的词绝大多数都为名词（n或n开头的）。

# TopN词汇输出

接下来我们把文本中的TopN词汇及词频输出到result.txt中，每一行一个词，格式为：`词,词频`

```python
from collections import Counter
c = Counter(words).most_common(500)
with open('result.txt','w+') as f:
    for x in c:
        f.write('{0},{1}\n'.format(x[0],x[1]))
```

得到的result.txt的前10行内容如下：


```
程心,1451
罗辑,1256
世界,1243
地球,951
人类,935
太空,930
三体,879
宇宙,875
太阳,775
舰队,649
```

# 完整代码封装

将上述每一步的代码封装成一个完整的脚本，如下：


```python
# coding:utf-8
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
```

# 代码归档
[我的GitHub](https://github.com/dnxbjyj/py-project/tree/master/SantiCut)