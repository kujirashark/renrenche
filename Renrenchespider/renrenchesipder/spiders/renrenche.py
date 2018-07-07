from scrapy_redis.spiders import RedisSpider
from scrapy import Selector, Request
from scrapy.spiders import Spider

from renrenchesipder.items import RenrenchesipderItem


class RenRenCheSipder(RedisSpider):
    name = 'renrenche'

    # 指定访问爬虫爬取urls队列
    reids_keys = 'renrenche:start_urls'

    # # 网站域名
    # domain_url = 'https://www.renrenche.com'
    # # 设置过滤爬取的域名
    # allowed_domains = ['www.renrenche.com']
    # # 二手车的url
    # ershouche_url = 'https://www.renrenche.com/cd/ershouche/'
    #
    # def start_requests(self):
    #     yield Request(self.ershouche_url)
    #
    # # 解析所有的品牌
    # def parse(self, response):
    #     res = Selector(response)
    #     brand_url_list = res.xpath('//*[@id="brand_more_content"]/div/p/span/a')
    #     for a in brand_url_list:
    #         band_url = a.xpath('./@href').extract()[0]
    #         yield Request(self.domain_url + band_url, callback=self.parse_page_url,
    #                       meta={'band_url': band_url, 'page': 1})
    #
    # # 解析某个品牌下面的页面
    # def parse_page_url(self, response):
    #     res = Selector(response)
    #     page = res.xpath('/html/body/div[3]/div[6]/ul/li/a/text()').extract()[-1]
    #     d = res.xpath('//*[@id="search_list_wrapper"]/div/div/div[1]/ul/li')
    #
    #     band_url = response.meta.get('band_url')
    #     for i in range(1, int(page) + 1):
    #         yield Request(self.domain_url + band_url + 'p' + str(i), callback=self.parse_car_url)
    #
    # # 获取车辆详情的车辆url
    # def parse_car_url(self, response):
    #     res = Selector(response)
    #     car_url = res.xpath('//*[@id="search_list_wrapper"]/div/div/div[1]/ul/li/a/@href')
    #     for c in car_url:
    #         one_car_url = c.extract()
    #         yield Request(self.domain_url + one_car_url, callback=self.parse_car_info)

    # 解析具体车辆详情页
    # def parse_car_info(self, response):
    def parse_car_info(self, response):
        res = Selector(response)
        items = RenrenchesipderItem()
        items['id'] = res.xpath('/html/body/@data-event-properties').extract()[0]
        # 标题
        items['title'] = res.xpath('//div[@class="title"]/h1/text()').extract()[0]
        # 客户出价
        items['price'] = res.xpath('//div[@class="middle-content"]/div/p[2]/text()').extract()[0]
        # 市场价
        items['new_car_price'] = res.xpath('//div[@class="middle-content"]/div/div[1]/span/text()').extract()[0]
        # 首付款
        down_payment = res.xpath('//div[@class="list"]/p[@class="money detail-title-right-tagP"]/text()')
        # 月供
        monthly_payment = res.xpath('//*[@id="basic"]/div[2]/div[2]/div[1]/div[3]/div[2]/p[5]/text()')
        # 判断是否可以分期购买
        if down_payment and monthly_payment:
            items['staging_info'] = [down_payment.extract()[0], monthly_payment.extract()[0]]
        # 服务费
        items['service_fee'] = res.xpath('//*[@id="js-service-wrapper"]/div[1]/p[2]/strong/text()').extract()[0]
        # 服务项
        items['service'] = res.xpath('//*[@id="js-box-service"]/table/tr/td/table/tr/td/text()').extract()
        # 车辆上牌时间 里程 外迁信息
        items['info'] = res.xpath('//*[@id="basic"]/div[2]/div[2]/div[1]/div[4]/ul/li/div/p/strong/text()').extract()
        # 车辆排量
        items['displacement'] = \
            res.xpath('//*[@id="basic"]/div[2]/div[2]/div[1]/div[4]/ul/li[4]/div/strong/text()').extract()[0]
        # 车辆上牌城市
        items['registration_city'] = res.xpath('//*[@id="car-licensed"]/@licensed-city').extract()[0]
        # 车源号
        items['options'] = \
            res.xpath('//*[@id="basic"]/div[2]/div[2]/div[1]/div[5]/p/text()').extract()[0].strip().split("：")[1]
        # 判断是都有图片
        if res.xpath('//div[@class="info-recommend"]/div/img/@src'):
            # 车辆图片
            items['car_img'] = res.xpath('//div[@class="info-recommend"]/div/img/@src').extract()[0]
        items['city'] = res.xpath('//div[@rrc-event-scope="city"]/a[@class="choose-city"]/text()').extract()[0].strip()
        items['color'] = res.xpath('//div[@class="card-table"]/table/tr/td[2]/text()').extract()[0]

        yield items
