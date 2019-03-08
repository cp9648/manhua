# -*- coding: utf-8 -*-
import scrapy

from scrapy.http import Request
from manhua.items import ManhuaItem
from scrapy_redis.spiders import RedisSpider
from furl import furl


class ManhuataiSpider(RedisSpider):
    name = 'manhuatai'
    allowed_domains = ['www.manhuatai.com']
    # start_urls = ['lpush myspider:start_urls https://www.manhuatai.com/all.html']
    redis_key = 'myspider:start_urls'

    def parse(self, response):
        # import ipdb; ipdb.set_trace()
        for sdiv in response.xpath('//a[@class="sdiv"]'):
            href = sdiv.xpath('@href').extract_first()
            _url = furl(response.url).remove(path=True).join(href).url
            yield scrapy.http.Request(url=_url, callback=self.parse_detailed)
            # break
        print(response.url)
        pages = response.xpath('//div[@class="pages"]/a')[-1]
        page_url = pages.xpath('@href').extract_first()
        if bool(page_url):
            _url = furl(response.url).remove(path=True).join(page_url).url
            yield scrapy.http.Request(url=_url, callback=self.parse)

    def parse_detailed(self, response):
        item = ManhuaItem()
        jshtml = response.xpath('//div[@class="jshtml"]')
        # 书名
        item['name'] = jshtml.xpath('./ul/li[1]/text()').extract_first().split('：')[-1]
        print(item['name'])
        # 图片
        # import ipdb; ipdb.set_trace()
        item['img'] = response.xpath('//div[@id="offlinebtn-container"]/img/@data-url').extract_first()
        # 状态
        item['state'] = jshtml.xpath('./ul/li[2]/text()').extract_first().split('：')[-1]
        # 作者
        item['author'] = jshtml.xpath('./ul/li[3]/text()').extract_first().split('：')[-1]
        # 类型
        item['_type'] = jshtml.xpath('./ul/li[4]/text()').extract_first().split('：')[-1]
        # 简介
        item['title']= jshtml.xpath('./div/div[@class="wz clearfix t1"]/div/text()').extract_first()
        # 更新
        item['update'] = jshtml.xpath('./ul/li[5]/text()').extract_first()
        # 章节
        data_chapter = {}
        for chapter in response.xpath('//ul[@id="topic1"]//li')[::-1]:
            chapter_name = chapter.xpath('./a/@title').extract_first()
            href = chapter.xpath('./a/@href').extract_first()
            chapter_url = furl(response.url).remove(path=True).join(href).url
            # list_url = self.parse_chapter(chapter_url)
            data_chapter[chapter_name] = chapter_url
            # yield scrapy.http.Request(url=chapter_url, callback=self.parse_chapter)
            # break
        # import ipdb; ipdb.set_trace()
        str_chapter = str(data_chapter).replace("'", '"')
        item['chapter'] = str_chapter
        yield item
