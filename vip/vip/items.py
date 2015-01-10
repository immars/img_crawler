# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductItem(scrapy.Item):
    id = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    tags = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    price = scrapy.Field()


