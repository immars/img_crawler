#!/usr/bin/python

# -*- coding: utf-8 -*-
import re
import sys
import scrapy

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from vip.items import ProductItem

class VipSpider(CrawlSpider):
    name = "vip"
    allowed_domains = ["vip.com","vipstatic.com", "vpimg1.com","vpimg2.com","vpimg3.com"]
    start_urls = ["http://www.vip.com/"]
    rules = (
            # Extract links matching 'category.php' (but not matching 'subsection.php')
            # and follow links from them (since no callback means follow=True by default).
            Rule(LinkExtractor(allow=('show.*html', )), process_links='filter_links', follow=True),

            # Extract links matching 'item.php' and parse them with the spider's method parse_item
            Rule(LinkExtractor(allow=('detail-.*html', )), process_links='filter_links', callback='parse_product', follow=True),
    )

    def filter_links(self, links):
        for link in links:
            link.url=link.url.split("?")[0]
        return links

    def parse_product(self, response):
        self.log('Hi, this is an item page! %s' % response.url)
        product = ProductItem()
        try:
            product['id'] = response.url.split('-')[2].split('.')[0]
        except:
            pass
        product['tags'] = response.css("div.M_class a::text").extract()
        product['url'] = response.url
        product['name'] =  response.xpath("//p[@class='pib_title_detail']/text()").extract()
        product['image_urls'] = response.css("div.show_midpic a::attr(href)").extract()
        return product

