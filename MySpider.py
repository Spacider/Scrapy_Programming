#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
__author__ = 'Gary'

# 引入库文件
import scrapy
from lxml import etree
from scrapytest.CourseItem import CourseItem

# 定义爬虫
class MySpider(scrapy.Spider):
    # 爬虫的名字，这个在后续会用到
    name = "myspider"
    # 允许访问的域
    allowed_domains = ["immoc.com"]
    # 爬取的初地址
    start_urls = ["http://www.imooc.com/course/list"]
    # 爬取方法
    def parse(self, response):
        # 实例一个容器保存一个爬取信息
        item = CourseItem()
        # 这部分是爬取部分，使用xpath 选择
        # 获取每个课程的div
        for box in response.xpath('//div[@class="course-card-container"]/a[@target="_blank"]'):
            # 获取每个div中的课程路径
            item['url'] = 'http://www.imooc.com' + box.xpath('.//@href').extract()[0]
            # 获取div中的课程标题
            item['title'] = box.xpath('.//div[@class="course-card-content"]/h3/text()').extract()[0]
            # 获取div中的标题图片地址
            item['image_url'] = box.xpath('.//div[@class="course-card-top"]/img/@src').extract()[0]
            # 获取div中的学生人数
            item['student'] = box.xpath('.//span/text()').extract()[1]
            # 获取div中的课程简介
            item['introduction'] = box.xpath('.//p/text()').extract()
            # 返回信息
            yield item
            # url跟进开始
            # 获取下一页的url信息
        url = response.xpath("//div[contains(.,'下一页')]//@href").extract()[-2]
        if url:
            # 将信息组合成下一页的url
            page = 'http://www.imooc.com' + url
            # 返回url
            # 停用过滤功能
            yield scrapy.Request(page, callback=self.parse, dont_filter=True)
            # url跟进结束


