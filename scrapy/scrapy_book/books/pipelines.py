# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError


class BooksPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.books

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]

        price = item['price']
        price_discount = item['price_discount']
        rating = item['rating']
        self.book_list_parse(spider.name, price,  price_discount, rating, item, collection)


    def book_list_parse(self, site, price,  price_discount, rating, item, collection):
        if site == 'labirint':
            item['price'] = int(price) if price else None
            item['price_discount'] = int(price_discount) if price_discount else None
            item['rating'] = float(rating) if rating else None

            existing_record = collection.find_one({'link': item['link']})
            if not existing_record:
                try:
                    collection.insert_one(item)
                except DuplicateKeyError:
                    print("Такая вакансия уже существует: ", item['url'])
        elif site == 'book24':
            existing_record = collection.find_one({'link': item['link']})
            if not existing_record:
                try:
                    collection.insert_one(item)
                except DuplicateKeyError:
                    print("Такая вакансия уже существует: ", item['url'])
        return item
