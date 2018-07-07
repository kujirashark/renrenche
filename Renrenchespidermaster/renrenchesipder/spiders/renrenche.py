from scrapy_redis.spiders import RedisSpider
from scrapy import Selector, Request

from renrenchesipder.items import MasterItem


class RenRenCheSipder(RedisSpider):
    name = 'renrenche'

    # 网站域名
    domain_url = 'https://www.renrenche.com'
    # 设置过滤爬取的域名
    allowed_domains = ['www.renrenche.com']
    # 二手车的url
    ershouche_url = 'https://www.renrenche.com/cd/ershouche/'

    def start_requests(self):
        yield Request(self.ershouche_url)

    # 解析所有的品牌
    def parse(self, response):
        res = Selector(response)
        brand_url_list = res.xpath('//*[@id="brand_more_content"]/div/p/span/a')
        for a in brand_url_list:
            band_url = a.xpath('./@href').extract()[0]
            yield Request(self.domain_url + band_url, callback=self.parse_page_url,
                          meta={'band_url': band_url, 'page': 1})

    # 解析某个品牌下面的页面
    def parse_page_url(self, response):
        res = Selector(response)
        page = res.xpath('/html/body/div[3]/div[6]/ul/li/a/text()').extract()[-1]
        d = res.xpath('//*[@id="search_list_wrapper"]/div/div/div[1]/ul/li')

        band_url = response.meta.get('band_url')
        for i in range(1, int(page) + 1):
            yield Request(self.domain_url + band_url + 'p' + str(i), callback=self.parse_car_url)

    # 获取车辆详情的车辆url
    def parse_car_url(self, response):
        res = Selector(response)
        item = MasterItem()
        car_url = res.xpath('//*[@id="search_list_wrapper"]/div/div/div[1]/ul/li/a/@href')
        for c in car_url:
            one_car_url = c.extract()
            item['url'] = self.domain_url + one_car_url
            yield item

