from scrapy.settings import Settings
from scrapy.crawler import CrawlerProcess

from jobparser import settings
from jobparser.spiders.hhru import HhruSpider
from jobparser.spiders.superjob import SuperjobSpider


if __name__ == '__main__':
    hhru_settings = Settings()
    hhru_settings.setmodule(settings)

    process = CrawlerProcess(settings=hhru_settings)
    process.crawl(HhruSpider)
    process.crawl(SuperjobSpider)

    process.start()
