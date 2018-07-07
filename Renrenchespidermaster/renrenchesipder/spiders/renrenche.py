import re
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
    #ershouche_url = 'https://www.renrenche.com/cd/ershouche/'

    def start_requests(self):
        yield Request(self.domain_url)

    # 解析所有城市
    def parse(self,response):
        res = Selector(response)
        city_url_list = res.xpath('//div[@class="area-city-letter"]/div/a[@class="province-item "]/@href')
        for city_url in city_url_list:
            city = city_url.extract()
            yield Request(self.domain_url + city,callback=self.parse_brand)

    # 解析所有的品牌
    def parse_brand(self, response):
        res = Selector(response)
        brand_url_list = res.xpath('//*[@id="brand_more_content"]/div/p/span/a')
        for a in brand_url_list:
            band_url = a.xpath('./@href').extract()[0]
            yield Request(self.domain_url + band_url, callback=self.parse_page_url)

    # 解析某个品牌下面的具体某辆车的页面
    def parse_page_url(self, response):
        item = MasterItem()
        res = Selector(response)
        # page = res.xpath('/html/body/div[3]/div[6]/ul/li/a/text()').extract()[-1]
        li_list = res.xpath('//ul[@class="row-fluid list-row js-car-list"]/li')
        # 判断页面
        # 判断页面是否有li标签
        if li_list:
            for c in li_list:
                one_car_url = c.xpath('./a[@class="thumbnail"]/@href').extract()
                if one_car_url:
                    item['url'] = self.domain_url + one_car_url[0]
                    yield item

            # 下一页信息
            page = response.meta.get('page',2)
            url = response.url
            url = re.sub(r'p\d+','',url)
            car_info_url = url + 'p{page}/'
            # 回调 获取下一页
            yield Request(car_info_url.format(page=page),meta={'page':page + 1},callback=self.parse_page_url)


