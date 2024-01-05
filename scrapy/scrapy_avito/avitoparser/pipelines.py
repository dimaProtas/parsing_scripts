# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
from urllib.parse import urlparse

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from scrapy.pipelines.media import MediaPipeline
from pymongo import MongoClient
import scrapy


class AvitoparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.avito

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        item['path'] = item['photos'][0]['path']
        item['link'] = item['photos'][0]['url']
        collection.insert_one(item)
        return item


class AvitoPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            n = 1
            for img in item['photos']:
                try:
                    yield scrapy.Request(img, meta={'name': item['name'], 'file':   f'file_{str(n)}'})
                    n += 1
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        item['photos'] = [itm for ok, itm in results if ok]
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        return f"{request.meta['name']}/{request.meta['file']}.jpg"
        # return f"{item['name'][:10]}/" + os.path.basename(urlparse(request.url).path) # Вариант сохранения №2


print('Даг Хеллман: Стандартная библиотека Python 3. Справочник с примерами/file_1.jpg')