from scrapy.conf import settings

import redis


class RenrenchesipderPipeline(object):

    def process_item(self, item, spider):
        return item


class MasterPipeline(object):

    def __init__(self):
        self.REDIS_HOST = settings['REDIS_HOST']
        self.REDIS_PORT = settings['REDIS_PORT']
        # 链接redis
        self.r = redis.Redis(host=self.REDIS_HOST, port=self.REDIS_PORT)

    def process_item(self, item, spider):
        # 向redis中插入需要爬取的链接地址
        self.r.lpush('renrenche:start_urls', item['url'])

        return item
