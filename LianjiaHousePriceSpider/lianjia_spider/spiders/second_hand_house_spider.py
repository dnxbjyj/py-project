# coding:utf-8
# 链家二手房信息爬虫
import sys
import scrapy
from scrapy import Request
from scrapy import Selector

reload(sys)
sys.setdefaultencoding('utf-8')

class SecondHandHouseSpider(scrapy.Spider):
    name = 'SecondHandHouseSpider'
    # 主页：链家深圳二手房首页
    host = 'https://sz.lianjia.com/ershoufang/'
    # 准备爬取的初始页面
    start_urls = ['https://sz.lianjia.com/ershoufang/']
    
    # 入口解析函数，解析初始页面的内容
    def start_requests(self):
        for url in self.start_urls:
            # 将url加入爬取队列，并指定解析函数，scrapy会自动进行调度
            yield Request(url = url,callback = self.parse_page)
    
    # 从上一步返回的页面内容中解析单个页面，解析出房子信息列表
    def parse_page(self,resp):
        # 创建Selector对象
        selector = Selector(resp)
        
        # 房子条目信息结构示例
        '''
        <li class="clear">
            <a class="img " href="https://sz.lianjia.com/ershoufang/105100842418.html" target="_blank"data-log_index="1" data-el="ershoufang" data-housecode="105100842418" data-is_focus="1" data-sl="">
                <div class="focus_tag"></div>
                <img class="lj-lazy" src="https://s1.ljcdn.com/feroot/pc/asset/img/blank.gif?_v=20170817190344" data-original="https://image1.ljcdn.com/440300-inspection/99d8e05f-6284-4c6b-a8c1-d94fe2e31c87.jpg.232x174.jpg" alt="方圆五公里再也找不到的南北双阳台的户型。">
            </a>
            <div class="info clear">
                <div class="title">
                    <a class="" href="https://sz.lianjia.com/ershoufang/105100842418.html" target="_blank" data-log_index="1"   data-el="ershoufang" data-housecode="105100842418" data-is_focus="1"  data-sl="">方圆五公里再也找不到的南北双阳台的户型。
                    </a>
                </div>
                <div class="address">
                    <div class="houseInfo"><span class="houseIcon"></span><a href="https://sz.lianjia.com/xiaoqu/2411050750393/" target="_blank" data-log_index="1" data-el="region">新锦安雅园 </a> | 3室2厅 | 119.42平米 | 东南 | 简装 | 有电梯
                    </div>
                </div>
                <div class="flood">
                    <div class="positionInfo"><span class="positionIcon"></span>低楼层(共17层)2000年建板塔结合  -  <a href="https://sz.lianjia.com/ershoufang/baoanzhongxin/" target="_blank">宝安中心</a>
                    </div>
                </div>
                <div class="followInfo">
                    <span class="starIcon"></span>77人关注 / 共51次带看 / 2个月以前发布
                </div>
                <div class="tag">
                    <span class="taxfree">房本满五年</span><span class="haskey">随时看房</span>
                </div>
                <div class="priceInfo">
                    <div class="totalPrice">
                        <span>675</span>万
                    </div>
                    <div class="unitPrice" data-hid="105100842418" data-rid="2411050750393" data-price="56524">
                        <span>单价56524元/平米</span>
                    </div>
                </div>
            </div>
            <div class="listButtonContainer">
                <div class="btn-follow followBtn" data-hid="105100842418"><span class="follow-text">关注</span></div>
                <div class="compareBtn LOGCLICK" data-hid="105100842418" log-mod="105100842418" data-log_evtid="10230">加入对比</div>
            </div>
        </li>
        '''
        
        # 房子信息li标签列表
        house_info_list = selector.xpath('//li[@class="clear"]')

        for info in house_info_list:
            # 标题
            title = info.xpath('.//div[@class="title"]/a[re:test(@href, "https://sz\.lianjia\.com/ershoufang/\d+\.html$")]/text()').extract_first()
            
            # 房屋详细信息，这里用'string(.)'解析出多个不同标签的文本内容
            house_detail = info.xpath('.//div[@class="houseInfo"]').xpath('string(.)').extract_first()

            print house_detail
            
            