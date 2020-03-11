# -*- coding: utf-8 -*-
import scrapy
import execjs
import re
from pcProxy.items import PcProxyItem
from pcProxy.settings import ANONYMITY_LEVELS

class ProxydbSpider(scrapy.Spider):
    name = 'proxydb'
    allowed_domains = ['proxydb.net']
    start_urls = ['http://proxydb.net/']

    def parse(self, response):
        item = PcProxyItem()
        tbody = response.css('tbody')
        tr_list = tbody.css('tr')
        for tr in tr_list:
            td_list = tr.css('td')
            item['ip'], item['port'] = self.get_proxy(td_list[0])
            item['country'] = td_list[2].xpath('abbr/text()').extract_first().strip()
            item['protocol'] = td_list[4].xpath('.//text()').extract_first().replace('\n','').strip().lower()
            anonymity_levels = td_list[5].xpath('span/text()').extract_first().strip()
            item['anonymity_levels'] = ANONYMITY_LEVELS[anonymity_levels]
            item['position'] = None
            yield item

    def get_proxy(self, td_tag):
        """
        从td_tag中提取参数ip_first, ip_second, port和data_rnnumr，
        eg: ip_first='.86.831', ip_second='\x4e\x44\x45\x75\x4f\x54\x41\x3d',
            port=3115, data_rnnumr=13(index页面data-rnnumy的值,页面加载成功后找不到)
        再利用execjs调用js代码,获取代理ip和port
        Args:
            td_tag: scrapy.selector.unified.Selector, 包含ip和port的td标签
        Returns:
            tuple, 返回一个(ip, port)的元组
        """

        ip_first = re.search("'([\.\d]*)\'.split", td_tag.get()).group(1)
        ip_second = re.search("atob\(\'(.*?)\'.replace", td_tag.get()).group(1)
        p = re.search('pp =  \((\d*) -', td_tag.get()).group(1)

        ctx = execjs.compile("""
            function get_ip_port(ip_first, ip_second, port, data_rnnumr=13) {
                var b = ip_first.split('').reverse().join('');

                var base64_str = ip_second.replace(/\\x([0-9A-Fa-f]{2})/g, function() {
                    return String.fromCharCode(parseInt(arguments[1], 16))
                });
                var str = Buffer(base64_str, 'base64').toString();

                var pp = (port - ([] + [])) + data_rnnumr - [] + [];

                ip_port = new Array(b+str, pp);
                return ip_port;
            }
        """)
        return ctx.call("get_ip_port", ip_first, ip_second, p)
