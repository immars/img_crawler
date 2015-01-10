# -*- coding: utf-8 -*-

# Scrapy settings for vip project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'vip'

ITEM_PIPELINES = {'scrapy.contrib.pipeline.images.ImagesPipeline': 1}
IMAGES_STORE = '/home/immars/work/search/scrapy/vip/image_data'

SPIDER_MODULES = ['vip.spiders']
NEWSPIDER_MODULE = 'vip.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'vip (+http://www.yourdomain.com)'
