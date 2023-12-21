from scrapy.settings import Settings
from scrapy.crawler import CrawlerProcess

from books import settings
from books.spiders.labirint import LabirintSpider
from books.spiders.book24 import Book24Spider


if __name__ == '__main__':
    books_settings = Settings()
    books_settings.setmodule(settings)

    process = CrawlerProcess(settings=books_settings)
    # process.crawl(LabirintSpider)
    process.crawl(Book24Spider)

    process.start()