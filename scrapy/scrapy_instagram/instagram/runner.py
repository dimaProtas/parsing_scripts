from scrapy.settings import Settings
from scrapy.crawler import CrawlerProcess
from instagram import settings
from instagram.spiders.Insta import InstaSpider


if __name__ == '__main__':
    insta_set = Settings()
    insta_set.setmodule(settings)
    process = CrawlerProcess(settings = insta_set)
    process.crawl(InstaSpider)
    process.start()
    
