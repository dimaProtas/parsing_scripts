import scrapy
from scrapy.http import HtmlResponse

from books.items import BooksItem


class LabirintSpider(scrapy.Spider):
    name = "labirint"
    allowed_domains = ["labirint.ru"]
    start_urls = ["https://www.labirint.ru/search/python/?stype=0&page=1"]

    def parse(self, response: HtmlResponse):
        link_books = response.xpath("//a[@class='product-card__img']/@href").extract()
        for link in link_books:
            yield response.follow(link, callback=self.book_parse)
        next_link = response.xpath("//div[@class='pagination-next']/a[@class='pagination-next__text']/@href").extract_first()
        print(1)
        if next_link:
            yield response.follow(next_link, callback=self.parse)

    def book_parse(self, response: HtmlResponse):
        name_books = response.xpath("//h1//text()").extract_first()
        authors = response.xpath("//a[@data-event-label='author']//text()").extract()
        price = response.xpath("//span[@class='buying-priceold-val-number']//text()").extract_first()
        price_discount = response.xpath("//span[@class='buying-pricenew-val-number']//text()").extract_first()
        link = response.url
        rating = response.xpath("//div[@id='rate']//text()").extract_first()
        yield BooksItem(name_books=name_books, authors=authors, price_discount=price_discount,
                        price=price, link=link, rating=rating)
