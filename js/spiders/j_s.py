# -*- coding: utf-8 -*-
from wsgiref import headers
import scrapy
from pip._vendor import requests
from js.items import JsItem
from scrapy.utils.response import get_base_url
from urllib.parse import urljoin
from datetime import datetime

class JSSpider(scrapy.Spider):
    name = 'j_s'
    box = []
    for num in range(100,200):
        pages = 'http://www.jianshu.com/c/V2CqjW?order_by=commented_at&page={0}'.format(num)
        box.append(pages)
    start_urls = box


    def parse(self, response):

        jianshudiv=response.xpath("//ul[@class='note-list']/li")
        for jsdiv in jianshudiv:
            item = JsItem()
            item['title']=jsdiv.xpath(".//div[@class='content']/a[@class='title']/text()").extract()
            item['author']=jsdiv.xpath(".//div[@class='meta']/a[@class='nickname']/text()").extract()
            content=jsdiv.xpath(".//div[@class='content']/p[@class='abstract']/text()").extract()
            item['content']="".join(content).strip()
            comment=jsdiv.xpath('.//div[@class="content"]/div[@class="meta"]/a[2]/text()').extract()
            item['comment'] = ''.join(comment).strip()
            likes = jsdiv.xpath('.//div/span[2]/text()').extract()
            item['likes'] = ''.join(likes)
            authorlink=jsdiv.xpath('.//div[@class="content"]/div[@class="meta"]/a/@href').extract()[0]
            item['authorlink']=''.join(['http://www.jianshu.com', authorlink])
            url = jsdiv.xpath('.//div[@class="content"]/a/@href').extract()[0]
            item['url']= 'http://www.jianshu.com' + url
            url1 = url.split("?")[0]
            item['article_id'] = url1.split('/')[-1]
            piclink=jsdiv.xpath('.//a[1]/img/@src').extract()
            item['piclink'] =''.join(piclink).strip()
            yield scrapy.Request(url=item['url'],callback=self.parse_detail,method="GET",meta={"item":item},dont_filter=True)

    def parse_detail(self,response):
            item=response.meta["item"]
            item['time'] = str(datetime.now())
            artical=response.xpath('//article[@class="_2rhmJa"]').xpath('string(.)').extract()
            item['artical'] = ''.join(artical).replace("\n","").replace("\xa0","")
            yield item



