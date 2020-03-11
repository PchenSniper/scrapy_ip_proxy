# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PcProxyItem(scrapy.Item):
    ip = scrapy.Field()
    port = scrapy.Field()
    anonymity_levels = scrapy.Field() # 匿名度
    protocol = scrapy.Field() # 协议类型http https socket
    position = scrapy.Field() # 地理位置
    country = scrapy.Field() # 代理所属国家
