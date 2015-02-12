#
# -*- coding: utf-8 -*-
import sys
import scrapy
from taobao.items import ProductItem
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor


def prop_get(pmap, names):
    tmp = None
    for name in names:
        if not tmp:
            tmp = pmap.get(name)
        else:
            break
    if not tmp:
        tmp = ''

    return tmp

'''
main page:
    http://nvren.taobao.com/

markets:
    www.taobao.com/market/xxxx/yyyy.php
    important woman markets:
    http://www.taobao.com/market/nvzhuang/index.php
    http://www.taobao.com/market/mei/index.php
    http://www.taobao.com/market/nvbao/shouye.php
    http://www.taobao.com/market/nvxie/citiao/index.php

lists:
    http://s.taobao.com/list?q=%D6%D0%B8%FA
item:
    http://item.taobao.com/item.htm?id=41297993338


http://www.taobao.com/market/nvbao/shouye.php?spm=a217q.7279049.a214d6o.10.i0aDxl
http://s.taobao.com/list?q=%C5%AE%B0%FC+%C1%F7%CB%D5

http://detail.tmall.com/item.htm?id=43146919700&ali_refid=a3_430329_1006:1103685483:N:%C5%A3%D7%D0%CD%E2%CC%D7:5b0ac9df717b2ae4136d1507ba93ccc6&ali_trackid=1_5b0ac9df717b2ae4136d1507ba93ccc6&spm=a217f.1256815.1998111894.1793.la1FiE&scm=1029.minilist-17.1.16#detail
http://gi3.md.alicdn.com/bao/uploaded/i3/TB1iW.iGVXXXXajXXXXXXXXXXXX_!!0-item_pic.jpg_430x430q90.jpg

'''
class TaobaoSpider(CrawlSpider):
    name="taobao"
    allow_domains = ["taobao.com"]

    start_urls = ["http://nvren.taobao.com/"]

    rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php'
        # and follow links from them (since no callback means follow=True by default).
        Rule(LinkExtractor(allow=('/market/.*\.php', )), callback='check_response', follow=True, process_links='prolink_market', process_request='handle_cookie'),
        Rule(LinkExtractor(allow=('/list\?', )), callback='check_response', follow=True, process_links='prolink_list', process_request='handle_cookie'),

        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        Rule(LinkExtractor(allow=('item\.htm', )), process_links='prolink_item', callback='parse_item'),
    )

    def check_response(self, response):
        # self.log("response[%s]: %s" % (response.url, response.headers))
        pass

    def prolink_market(self, links):
        # self.log("market found:%s" % links)
        for l in links:
            l.url=l.url.split('?')[0]
        # self.log("market link processed:%s" % links)
        return links

    def prolink_list(self, links):

        for l in links:
            url = l.url
            qparam=filter(lambda x:x.startswith("q="), url[url.index('?')+1:].split('&'))
            if(len(qparam)>0):
                l.url= "%s?%s" % (url[:url.index('?')], qparam[0])
        # self.log("search link processed:%s" % links)
        return links

    def prolink_item(self, links):
        for l in links:
            url = l.url
            qparam=filter(lambda x:x.startswith("id="), url[url.index('?')+1:].split('&'))
            if(len(qparam)>0):
                l.url= "%s?%s" % (url[:url.index('?')], qparam[0])
        self.log("item link processed:%s" % links)
        return links

    def handle_cookie(self, request):
        # auto handled?
        # self.log("request[%s]cookie:%s" % (request.url, request.cookies))
        # self.log("request[%s] headers: %s" % (request.url, request.headers))
        return request

    def parse_item(self, response):
        self.log('Hi, this is an item page! %s' % response.url)
        item = ProductItem()
        image_urls=response.css("div.tb-s50 a img::attr(data-src)").extract()
        item['image_urls'] = [url.replace('50x50','400x400') for url in image_urls]
        #http://img02.taobaocdn.com/imgextra/i2/2118504882/TB285zRaVXXXXazXXXXXXXXXXXX_!!2118504882.jpg_50x50.jpg
        item['name'] = response.css(".tb-main-title::attr(data-title)").extract()
        item['price'] = response.css("div.tb-property-cont em.tb-rmb-num::text").extract()
        item['url'] = response.url
        item['id'] = response.css('div#J_Pine::attr("data-itemid")').extract()

        props = [x.split(u":\xa0") for x in response.css("#J_AttrUL li::text").extract()]
        pmap = {}
        for p in props:
            if(len(p)==2):
                pmap[p[0]]=p[1]

        item['material'] = prop_get(pmap, [u'材质', u'面料', u'面料材质', u'鞋面材质'])
        item['collar'] = prop_get(pmap, [u'领子'])
        item['thickness'] = prop_get(pmap, [u'厚薄'])
        item['pattern'] = prop_get(pmap, [u'图案'])
        item['style'] = prop_get(pmap, [u'款式'])
        item['brand'] = prop_get(pmap, [u'品牌'])
        item['sleeve'] = prop_get(pmap, [u'袖长'])
        item['zipper'] = prop_get(pmap, [u'衣门襟'])
        item['skirt'] = prop_get(pmap, [u'裙长'])
        item['shoe_head'] = prop_get(pmap, [u'鞋头款式'])
        item['heel'] = prop_get(pmap, [u'鞋跟'])
        item['handle'] = prop_get(pmap, [u'提拎部件类型'])
        return item


        return item


'''
    TMALL spider
main pages:
    http://nvzhuang.tmall.com/
    http://nvxie.tmall.com/
    http://bag.tmall.com/

topic pages:
    http://www.tmall.com/go/market/promotion-act/xiangbaofenqigoudierqi.php
    http://www.tmall.com/go/market/promotion-act/xiangbaowoshinianhuo.php
    http://www.tmall.com/go/market/fushi/chongaizj.php
    http://www.tmall.com/go/market/fushi/module2014-1.php
    http://www.tmall.com/go/market/fushi/loveziji.php
    http://www.tmall.com/go/market/fushi/module2014-2.php


market lists:
        page down:s=60
    http://list.tmall.com/search_product.htm?&vmarket=48386
    http://list.tmall.com/search_product.htm?sort=s&cat=51024008
    http://list.tmall.com/search_product.htm?sort=s&cat=51024008
    http://list.tmall.com/search_product.htm?brand=3713796&q=MCM&sort=s

brand pages:
        or:http://xxx.tmall.com/index.htm
    http://memxiangbao.tmall.com/
    http://qiwang.tmall.com/
    http://panbixuan.tmall.com/
    http://panbixuan.tmall.com/

item:
    http://detail.tmall.com/item.htm?id=13505747865

'''
class TMallSpider(CrawlSpider):
    name="tmall"
    allow_domains = ["tmall.com"]

    start_urls = ["http://nvzhuang.tmall.com/","http://nvxie.tmall.com/","http://bag.tmall.com/"]

    rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php'
        # and follow links from them (since no callback means follow=True by default).
        Rule(LinkExtractor(allow=('/go/market/.*\.php', ), pass_meta=['url_stack']), callback='check_response', follow=True, process_links='prolink_market', process_request='handle_cookie'),
        Rule(LinkExtractor(allow=('/list\?', ), pass_meta=['url_stack']), callback='check_response', follow=True, process_links='prolink_list', process_request='handle_cookie'),
        Rule(LinkExtractor(allow=('/', '/index.htm'), allow_domains=("tmall.com",), pass_meta=['url_stack'], ), callback='check_response', follow=True, process_links='prolink_brand', process_request='handle_cookie'),
        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        Rule(LinkExtractor(allow=('item\.htm', ), deny_domains=("chaoshi.detail.tmall.com",), pass_meta=['url_stack'],), process_links='prolink_item', callback='parse_item'),
    )

    def check_response(self, response):
        # self.log("response[%s]: %s" % (response.url, response.headers))
        pass

    def prolink_market(self, links):
        """
        http://www.tmall.com/go/market/promotion-act/xiangbaofenqigoudierqi.php
        """
        # self.log("market found:%s" % links)
        for l in links:
            l.url=l.url.split('?')[0]
        # self.log("market link processed:%s" % links)
        return links

    def prolink_list(self, links):
        """
        page down:s=60
        http://list.tmall.com/search_product.htm?&vmarket=48386
        http://list.tmall.com/search_product.htm?sort=s&cat=51024008
        http://list.tmall.com/search_product.htm?sort=s&cat=51024008
        http://list.tmall.com/search_product.htm?brand=3713796&q=MCM&sort=s
        """
        for l in links:
            url = l.url
            qparam=filter(lambda x:any(x.startswith(pre) for pre in ["vmarket=","sort=","cat=","brand=","q=","s="]), url[url.index('?')+1:].split('&'))
            if(len(qparam)>0):
                l.url= "%s?%s" % (url[:url.index('?')], qparam[0])
        # self.log("search link processed:%s" % links)
        return links

    def prolink_brand(self, links):
        """
        or:http://xxx.tmall.com/index.htm
        http://memxiangbao.tmall.com/
        http://qiwang.tmall.com/
        http://panbixuan.tmall.com/
        http://panbixuan.tmall.com/
        """
        # self.log("market found:%s" % links)
        for l in links:
            l.url=l.url.split('?')[0]
        # self.log("market link processed:%s" % links)
        return links


    def prolink_item(self, links):
        """
        http://detail.tmall.com/item.htm?id=13505747865
        """
        for l in links:
            url = l.url
            qparam=filter(lambda x:x.startswith("id="), url[url.index('?')+1:].split('&'))
            if(len(qparam)>0):
                l.url= "%s?%s" % (url[:url.index('?')], qparam[0])
        #self.log("item link processed:%s" % links)
        return links

    def handle_cookie(self, request):
        # auto handled?
        # url_stack
        if not request.meta:
            request.meta={}
        if not request.meta.get('url_stack'):
            request.meta['url_stack']=[]
        #request.meta['url_stack'].append({'url':request.url, 'text':request.meta['link_text']})
        #self.log("handle_cookie: meta:%s" % request.meta)
        return request

    def parse_item(self, response):
        self.log("item response meta:%s" % response.meta)
        if len(response.css(".errorPage")) > 0:
            self.log('item NOT FOUND page: %s' % response.url)
            return

        self.log('Hi, this is an item page! %s' % response.url)
        item = ProductItem()
        image_urls=response.css("#J_UlThumb img::attr('src')").extract()
        item['image_urls'] = [url.replace('60x60','430x430') for url in image_urls]
        #http://img02.taobaocdn.com/imgextra/i2/2118504882/TB285zRaVXXXXazXXXXXXXXXXXX_!!2118504882.jpg_50x50.jpg
        item['name'] = response.css("div.tb-detail-hd h1::text").extract()
        item['price'] = response.css("div.tb-property-cont em.tb-rmb-num::text").extract()
        item['url'] = response.url
        item['id'] = response.url.split('id=')[1]
        item['url_stack'] = response.meta.get('url_stack')
        props = [x.split(u":\xa0") for x in response.css("#J_AttrUL li::text").extract()]
        pmap = {}
        for p in props:
            if(len(p)==2):
                pmap[p[0]]=p[1]

        item['material'] = prop_get(pmap, [u'材质', u'面料', u'面料材质', u'鞋面材质'])
        item['collar'] = prop_get(pmap, [u'领子'])
        item['thickness'] = prop_get(pmap, [u'厚薄'])
        item['pattern'] = prop_get(pmap, [u'图案'])
        item['style'] = prop_get(pmap, [u'款式'])
        item['brand'] = prop_get(pmap, [u'品牌'])
        item['sleeve'] = prop_get(pmap, [u'袖长'])
        item['zipper'] = prop_get(pmap, [u'衣门襟'])
        item['skirt'] = prop_get(pmap, [u'裙长'])
        item['shoe_head'] = prop_get(pmap, [u'鞋头款式'])
        item['heel'] = prop_get(pmap, [u'鞋跟'])
        item['handle'] = prop_get(pmap, [u'提拎部件类型'])
        return item


