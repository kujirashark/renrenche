import random

from scrapy.contrib.downloadermiddleware.useragent import UserAgentMiddleware

from renrenchesipder.utils.useragentsource import PROXY, USER_AGENT_LIST


class ProxyMiddleware(object):

    def process_request(self, request, spider):
        # 随机去获取一个代理的ip
        proxy = random.choice(PROXY)
        # 设置代理的地址
        request.meta['proxy'] = 'https://%s' % proxy


class RandomUserAgent(UserAgentMiddleware):

    def process_request(self, request, spider):
        # 获取随机的一个user_agent的参数
        user_agent = random.choice(USER_AGENT_LIST)
        # 设置请求头中的User-Agent的参数
        request.headers.setdefault('User-Agent', user_agent)
