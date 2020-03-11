#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
@ Author      : muYangChen
@ EMail       : cp0825@163.com
@ Created Time: 2020-03-07 13:55:19
@ File Name   : kuaidaili.py
@ Description : 使用scrapy框架爬取快代理页面免费代理
'''

import scrapy
from pcProxy.items import PcProxyItem
from pcProxy.settings import ANONYMITY_LEVELS

class KuaidailiSpider(scrapy.Spider):
    name = "kuaidaili"

    def __init__(self, url="https://www.baidu.com"):
        """
        接受命令行传参，初始化类
        Args:
            url: string, 命令行中传入的测试网站链接
        Returns:
            pass
        """
        self.test_url = url #命令行传参中获取的测试url

    def start_requests(self):
        """
        重写start_requests方法，拼接抓取的url
        Args:
            pass
        Returns:
            pass
        """
        url = 'https://www.kuaidaili.com/free/inha/{page}'
        total_page = 20 # 抓取前20页
        for page in range(total_page):
            next_page = url.format(page=page+1)
            yield scrapy.Request(next_page)

    def parse(self, response):
        """
        解析页面
        Args:
            response: scrapy.http.response.html.HtmlResponse, http请求响应
        Returns:
            pass
        """
        item = PcProxyItem()
        tbody = response.css('tbody')
        for tr in tbody.css('tr'):
            item['ip'] = tr.xpath('td[1]/text()').extract_first()
            item['port'] = tr.xpath('td[2]/text()').extract_first()
            anonymity_levels = tr.xpath('td[3]/text()').extract_first()
            item['anonymity_levels'] = ANONYMITY_LEVELS[anonymity_levels]
            item['protocol'] = tr.xpath('td[4]/text()').extract_first().lower()
            item['position'] = tr.xpath('td[5]/text()').extract_first()
            item['country'] = 'CHINA'
            yield item

            #item['url'] = url
            #yield scrapy.Request(
            #    self.test_url,
            #    callback=self.test_parse,
            #    errback=self.error_back,
            #    meta={
            #        "proxy":url,
            #        "dont_retry":True, # 执行一次请求
            #        "download_timeout":10, # 超时时间
            #        "item":item,
            #    },
            #    dont_filter=True, # 不过滤重复请求
            #)

    def test_parse(self, response):
        yield response.meta['item']

    def error_back(self, failure):
        self.logger.error(repr(failure))
