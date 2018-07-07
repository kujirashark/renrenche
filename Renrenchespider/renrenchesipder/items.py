
import scrapy


class RenrenchesipderItem(scrapy.Item):
    '''定义车辆信息的item'''

    # 定义表名称
    collection = 'car_info'
    # 定义字段名称
    id = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    new_car_price = scrapy.Field()
    staging_info = scrapy.Field()
    service_fee = scrapy.Field()
    service = scrapy.Field()
    info = scrapy.Field()
    displacement = scrapy.Field()
    registration_city = scrapy.Field()
    options = scrapy.Field()
    car_img = scrapy.Field()
    city = scrapy.Field()
    color = scrapy.Field()
