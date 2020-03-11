# -*- coding: utf-8 -*-
import scrapy
from pcProxy.items import PcProxyItem

class ListdailySpider(scrapy.Spider):
    name = 'listdaily'
    allowed_domains = ['proxylistdaily.net']
    start_urls = ['https://www.proxylistdaily.net/']

    def parse(self, response):
        item = PcProxyItem()
        post_body = response.xpath("//div[contains(@id, 'post-body')]")
        for body in post_body:
            proxy_list = body.xpath(".//div[@class='centeredProxyList freeProxyStyle']")
            proxys = proxy_list.xpath('.//span/span/text()').extract_first()
            free_prosy = proxys.split('\n')[1:]
            for ip_port in free_prosy:
                item['ip'], item['port'] = ip_port.split(':')
                item['protocol'] = 'http'
                item['anonymity_levels'] = None
                item['position'] = None
                item['country'] = None
                yield item
                item['protocol'] = 'https'
                yield item
