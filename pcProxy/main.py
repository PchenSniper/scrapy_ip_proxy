#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
@ File Name   : main.py
@ Description : 
@ Author      : muYangChen
@ Created Time: 2020-03-11 15:44:18
'''

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.spiderloader import SpiderLoader

# 根据项目配置获取CrawlerProcess实例
process = CrawlerProcess(get_project_settings())

# 获取spiderloader对象，以获取项目下所有爬虫名称
spider_loader = SpiderLoader(get_project_settings())

# 添加需要执行的爬虫
for spidername in spider_loader.list():
    process.crawl(spidername)


# 执行
process.start()
