# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

# product for sale
class ProductItem(scrapy.Item):
	id = scrapy.Field()
	name = scrapy.Field()
	tags = scrapy.Field()
	url = scrapy.Field()
	price = scrapy.Field()
	images = scrapy.Field()
	image_urls = scrapy.Field()
    # define the fields for your item here like:
    # name = scrapy.Field()

# attributes for filter product search

class AttrItem(scrapy.Item):
	name = scrapy.Field()

