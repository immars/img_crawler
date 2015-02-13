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
    url_stack = scrapy.Field()
    price = scrapy.Field()
    images = scrapy.Field()
    image_urls = scrapy.Field()
    # product properties
    # 材质 / 面料
    material = scrapy.Field()
    # 领子
    collar = scrapy.Field()
    # 厚薄
    thickness = scrapy.Field()
    # 图案
    pattern = scrapy.Field()
    # 款式
    style = scrapy.Field()
    # 品牌
    brand = scrapy.Field()
    # 袖长
    sleeve = scrapy.Field()
    # 拉链
    zipper = scrapy.Field()
    # 裙长
    skirt = scrapy.Field()
    # 鞋头款式
    shoe_head = scrapy.Field()
    # 鞋跟
    heel = scrapy.Field()
    # 包包的 提拎部件类型
    handle = scrapy.Field()
    # 包包的 肩带样式
    girdle = scrapy.Field()
    # 旅行箱/包包 箱包硬度
    hardness = scrapy.Field()
    # 包包 形状
    shape = scrapy.Field()
    # 旅行箱 有无拉杆
    case_handle = scrapy.Field()
    # 滚轮样式
    wheel = scrapy.Field()

# attributes for filter product search

class AttrItem(scrapy.Item):
    name = scrapy.Field()

