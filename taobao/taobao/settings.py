# -*- coding: utf-8 -*-

# Scrapy settings for taobao project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'taobao'

USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'

DEFAULT_REQUEST_HEADERS = {
		'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		# Accept-Encoding:gzip, deflate, sdch
		'Accept-Language' : 'zh-CN,zh;q=0.8',
		'Cache-Control' : 'max-age=0',
}

ITEM_PIPELINES = {'scrapy.contrib.pipeline.images.ImagesPipeline': 1}
# IMAGES_STORE = '/home/immars/work/search/scrapy/taobao/image_data'
IMAGES_STORE = '/home/immars/work/search/images/taobao'

COOKIES_ENABLED = True

COOKIES_DEBUG = False

SPIDER_MODULES = ['taobao.spiders']
NEWSPIDER_MODULE = 'taobao.spiders'

AUTOTHROTTLE_ENABLED = True
CONCURRENT_REQUESTS_PER_DOMAIN = 4

DEPTH_LIMIT = 6

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'taobao (+http://www.yourdomain.com)'
