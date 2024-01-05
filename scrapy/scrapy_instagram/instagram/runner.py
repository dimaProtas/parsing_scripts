from scrapy.settings import Settings
from scrapy.crawler import CrawlerProcess
from instagram import settings
from instagram.spiders.Insta import InstaSpider

if __name__ == '__main__':
    insta_set = Settings()
    insta_set.setmodule(settings)

    # insta_set.set('HTTP_PROXY', 'http://195.154.184.80:8080')
    # insta_set.set('HTTPS_PROXY', 'https://195.154.184.80:8080')

    process = CrawlerProcess(settings=insta_set)
    process.crawl(InstaSpider)
    process.start()
    
