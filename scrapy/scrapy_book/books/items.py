# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BooksItem(scrapy.Item):
    # define the fields for your item here like:
    name_books = scrapy.Field()
    authors = scrapy.Field()
    price = scrapy.Field()
    price_discount = scrapy.Field()
    link = scrapy.Field()
    rating = scrapy.Field()
    _id = scrapy.Field()



