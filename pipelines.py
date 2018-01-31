# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.exceptions import DropItem
import json

class ScrapytestPipeline(object):
    def process_item(self, item, spider):
        return item

class MyPipeline(object):
    def __init__(self):
        # 打开文件
        self.file = open('data.json', 'w', encoding = 'utf-8')
    # 该方法用于处理数据
    def process_item (self, item, spider):
        # 读取item中的数据
        line = json.dumps(dict(item), ensure_ascii=False) + '\n'
        # 写入文件
        self.file.write(line)
        # 返回item
        return item
    # 该方法在spider被开启时被调用
    def open_spider(self, spider):
        pass
    def close_spider(self, spider):
        pass

class ImgPipleLine(ImagesPipeline):
    # 通过抓取的图片url获取一个Request用于下载
    def get_media_requests(self, item, info):
        # 返回Request 根据托盘url下载
        yield scrapy.Request('http:'+item['image_url'])
    # 当下载请求完成后执行该方法
    def item_completed(self, results, item, info):
        # 获取下载地址
        image_path = [x['path'] for ok, x in results if ok]
        # 判断是否成功
        if not image_path:
            raise DropItem('Item contains no images')
        # 将地址存入Item
        item['image_url'] = image_path
        return item
