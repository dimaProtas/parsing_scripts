import scrapy
from scrapy.http import HtmlResponse
from avitoparser.items import AvitoparserItem
from scrapy.loader import ItemLoader
import time
#https://youla.ru/moskva/auto/s-probegom?q=volkswagen
class AvitoruSpider(scrapy.Spider):
    name = 'avitoru'
    allowed_domains = ['avito.ru']
    handle_httpstatus_list = [403]
    # start_urls = ["https://www.avito.ru/moskva/avtomobili/volkswagen-ASgBAgICAUTgtg24mSg?radius=0&searchRadius=0"]

    def __init__(self, query, region):
        super(AvitoruSpider, self).__init__()
        # Пример отправки cookies
        self.start_urls = [f'https://www.avito.ru/{region}?localPriority=0&q={query}/']

    def parse(self, response: HtmlResponse):
        ads_links = response.xpath("//div[@class='items-items-kAJAg']//div[@class='iva-item-title-py3i_']/a[@itemprop='url']")
        for link in ads_links:
            yield response.follow(link, callback=self.parse_ads)
            time.sleep(2)
        print(1)


    def parse_ads(self,response:HtmlResponse):
        loader = ItemLoader(item=AvitoparserItem(), response=response)
        loader.add_xpath('photos', "//div[contains(@class,'gallery-img-frame')]/@data-url")
        loader.add_xpath('name', "//h1/span/text()")

        yield loader.load_item()


        photos = response.xpath("//div[contains(@class,'gallery-img-frame')]/@data-url").extract()
        name = response.xpath("//h1/span/text()").extract_first()
        yield AvitoparserItem(name=name, photos=photos)
