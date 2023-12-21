import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from avitoparser.items import AvitoparserItem


class LabirintSpider(scrapy.Spider):
    name = "labirint"
    allowed_domains = ["labirint.ru"]
    # start_urls = ["https://www.labirint.ru/search/python/?stype=0&page=1"]

    def __init__(self, query):
        super(LabirintSpider, self).__init__()
        self.start_urls = [f"https://www.labirint.ru/search/{query}/?stype=0&page=1"]


    def parse(self, response: HtmlResponse):
        link_books = response.xpath("//a[@class='product-card__img']/@href").extract()
        for link in link_books:
            yield response.follow(link, callback=self.book_parse)
        next_link = response.xpath("//div[@class='pagination-next']/a[@class='pagination-next__text']/@href").extract_first()
        if next_link:
            yield response.follow(next_link, callback=self.parse)

    def book_parse(self, response: HtmlResponse):
        loader = ItemLoader(item=AvitoparserItem(), response=response)
        loader.add_xpath('photos', "//div[@id='product-image']/img/@data-src")
        loader.add_xpath('name', "//h1//text()")

        yield loader.load_item()
        print(1)

        # photos = response.xpath("//div[@id='product-image']/img/@data-src").extract()
        # name = response.xpath("//h1//text()").extract_first()
        # yield AvitoparserItem(name=name, photos=photos)
