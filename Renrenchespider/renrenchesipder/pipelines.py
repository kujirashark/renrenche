from scrapy.conf import settings
import pymongo

from renrenchesipder.items import RenrenchesipderItem


class RenrenchesipderPipeline(object):

    def process_item(self, item, spider):

        return item


class PymongoPiperline(object):
    """连接mongodb"""

    def __init__(self):
        self.MONGODB_HOST = settings['MONGODB_HOST']
        self.MONGODB_PORT = settings['MONGODB_PORT']
        self.MONGODB_DB = settings['MONGODB_DB']
        # 创建连接
        conn = pymongo.MongoClient(host=self.MONGODB_HOST, port=self.MONGODB_PORT)
        # 连接数据库
        db = conn[self.MONGODB_DB]
        # 创建表
        self.colltection = db[RenrenchesipderItem.collection]

    def process_item(self, item, spider):
        # 使用id去定位数据库中是否有此数据,如果没有就添加数据.如果已经存在就更新数据
        self.colltection.update({'id': item['id']}, {'$set': item}, True)
        return item
