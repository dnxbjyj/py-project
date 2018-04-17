# 绘制《三体》全集词云

> 另参见：[好玩的分词（2）——分析了《三体》全集，我看到了这样的三体](http://www.jianshu.com/p/0c291d9e81d2)

在[好玩的分词（2）——分析了《三体》全集，我看到了这样的三体](http://www.jianshu.com/p/0c291d9e81d2)一文中，通过分词获取到了三体全集文本中topn的词及词频，那么本文中进一步用词云的形式来展现出来。

废话不多说，直接上代码：

```python
#!/usr/bin/python
# coding:utf-8
# 绘制一个《三体》全集词云
import sys
from collections import Counter
import jieba.posseg as psg
import matplotlib.pyplot as plt
from scipy.misc import imread
from wordcloud import WordCloud,ImageColorGenerator

# 对文本分词并标注词性，并缓存到文件
def cut_and_cache(text):
    # 将文本分词，并附带上词性，因为数据量比较大，防止每次运行脚本都花大量时间，所以第一次分词后就将结果存入文件cut_result.txt中
    # 相当于做一个缓存，格式为每个词占一行，每一行的内容为：
    # 词,词性
    words_with_attr = [(x.word,x.flag) for x in psg.cut(text) if len(x.word) >= 2]
    print len(words_with_attr)
    with open('cut_result.txt','w+') as f:
        for x in words_with_attr:
            f.write('{0}\t{1}\n'.format(x[0],x[1]))  
    return words_with_attr 

# 从cut_result.txt中读取带词性的分词结果列表
def read_cut_result():
    words_with_attr = []
    with open('cut_result.txt','r') as f:
        for x in f.readlines():
            # 这里解码成utf-8格式，是为了防止后面生成词云的时候出现乱码
            x = x.decode('utf-8')
            pair = x.split()
            if len(pair) < 2:
                continue
            words_with_attr.append((pair[0],pair[1]))
    return words_with_attr

#　统计在分词表中出现次数排名前topn的词的列表，并将结果输出到文件topn_words.txt中，每行一个词，格式为：
# 词,出现次数
def get_topn_words(words,topn):
    c = Counter(words).most_common(topn)
    top_words_with_freq = {}
    with open('top{0}_words.txt'.format(topn),'w+') as f:
        for x in c:
            f.write('{0},{1}\n'.format(x[0],x[1]))
            top_words_with_freq[x[0]] = x[1]
    return top_words_with_freq

# 传入文本文件的路径file_path和topn，获取文本文件中topn关键词列表及词频
def get_top_words(file_path,topn):
    # 读取文本文件，然后分词并缓存，只需运行一次，后续运行脚本可注释掉下面两行
    text = open(file_path).read()
    words_with_attr = cut_and_cache(text)
    
    # 从cut_result.txt中读取带词性的分词结果列表
    words_with_attr = read_cut_result()
    
    # 要过滤掉的词性列表
    stop_attr = ['a','ad','b','c','d','f','df','m','mq','p','r','rr','s','t','u','v','z']
    
    # 过滤掉不需要的词性的词
    words = [x[0] for x in words_with_attr if x[1] not in stop_attr]
    
    # 获取topn的词并存入文件topn_words.txt，top_words_with_freq为一个字典，在生成词云的时候会用到，格式为：
    # {'aa':1002,'bb':879,'cc':456}
    top_words_with_freq = get_topn_words(words = words,topn = topn)
    
    return top_words_with_freq

# 根据传入的背景图片路径和词频字典、字体文件，生成指定名称的词云图片
def generate_word_cloud(img_bg_path,top_words_with_freq,font_path,to_save_img_path,background_color = 'white'):
    # 读取背景图形
    img_bg = imread(img_bg_path)
    
    # 创建词云对象
    wc = WordCloud(font_path = font_path,  # 设置字体
    background_color = background_color,  # 词云图片的背景颜色，默认为白色
    max_words = 500,  # 最大显示词数为1000
    mask = img_bg,  # 背景图片蒙版
    max_font_size = 50,  # 字体最大字号
    random_state = 30,  # 字体的最多模式
    width = 1000,  # 词云图片宽度
    margin = 5,  # 词与词之间的间距
    height = 700)  # 词云图片高度
    
    # 用top_words_with_freq生成词云内容
    wc.generate_from_frequencies(top_words_with_freq)
    
    # 用matplotlib绘出词云图片显示出来
    plt.imshow(wc)
    plt.axis('off')
    plt.show()
    
    # 如果背景图片颜色比较鲜明，可以用如下两行代码获取背景图片颜色函数，然后生成和背景图片颜色色调相似的词云
    #img_bg_colors = ImageColorGenerator(img_bg)
    #plt.imshow(wc.recolor(color_func = img_bg_colors))
    
    # 将词云图片保存成图片
    wc.to_file(to_save_img_path)

def main():
    # 设置环境为utf-8编码格式，防止处理中文出错
    reload(sys)
    sys.setdefaultencoding('utf-8')
    
    # 获取topn词汇的'词:词频'字典，santi.txt是当前目录下三体全集的文本
    top_words_with_freq = get_top_words('./santi.txt',300)
    
    # 生成词云图片，bg.jpg是当前目录下的一副背景图片，yahei.ttf是当前目录下微软雅黑字体文件，santi_cloud.png是要生成的词云图片名
    generate_word_cloud('./bg.jpg',top_words_with_freq,'./yahei.ttf','./santi_cloud.png')
    
    print 'finish'
    
if __name__ == '__main__':
    main()
    
```

上述代码中，bg.jpg图片如下，是一只豹子的剪影，像一个在黑暗森林中潜伏的猎人：
![](http://upload-images.jianshu.io/upload_images/8819542-70f3a0d233c8a351.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

注：作为词云背景的图片一定要轮廓分明，且图片主体颜色要和图片自身的背景颜色对比度较大，这样生成的词云图片才能更清晰。一般剪影图片更容易满足这种要求。

此外，三体全集santi.txt文本从网上很好搜到。

**注：有个坑要注意，就是在生成词云前要把santi.txt的编码格式转为utf-8格式，否则可能并出不来预期的结果。**

运行上述代码，生成的词云图片如下：
![](http://upload-images.jianshu.io/upload_images/8819542-ebd45665aba2cfc7.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


最后，可以将这里的背景图片和文本文件修改成其他的图片和文本路径，那么运行上面代码就可以马上得到自己想要的词云了！

---
代码已经放到：[我的GitHub](https://github.com/dnxbjyj/py-project/tree/master/SantiWordCloud)
