from scrapy_redis.spiders import RedisSpider
from scrapy import Selector

from renrenchesipder.items import RenrenchesipderItem


class RenRenCheSipder(RedisSpider):
    # 爬虫名称
    name = 'renrenche'

    # 指定访问爬虫爬取urls队列
    reids_keys = 'renrenche:start_urls'
    
    # 解析详情页
    def parse(self, response):
        res = Selector(response)
        items = RenrenchesipderItem()
        items['id'] = res.xpath('//div[@class="detail-wrapper"]/@data-encrypt-id').extract()[0]
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
        # 车辆所在城市
        items['city'] = res.xpath('//div[@rrc-event-scope="city"]/a[@class="choose-city"]/text()').extract()[0].strip()
        # 车辆颜色
        items['color'] = res.xpath('//div[@class="card-table"]/table/tr/td[2]/text()').extract()[0]

        yield items
