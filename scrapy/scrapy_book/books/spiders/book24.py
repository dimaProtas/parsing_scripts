import json
import time
import scrapy
from scrapy.http import HtmlResponse
from books.items import BooksItem

class Book24Spider(scrapy.Spider):
    name = "book24"
    allowed_domains = ["book24.ru"]
    start_urls = ["https://book24.ru/search/?q=Психология"]

    # def start_requests(self):
    #     url = 'https://book24.ru/api/v1/catalog/product/reviews/livelib/?isbn=978-5-699-98630-9'
    #     headers = {
    #         'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    #         'X-Oauth-Client-Id': '6a56dbab-804b-4a39-b767-4bbfdc28d7e9',
    #     }
    #     yield scrapy.Request(url, headers=headers, callback=self.process_reviews)


    def parse(self, response: HtmlResponse):
        books_links = response.xpath("//div[contains(@class, 'product-list')]//a[@class='product-card__image-link']/@href").extract()
        for link in books_links:
            yield response.follow(link, callback=self.book_parse)
        next_link = response.xpath("//a[@class='pagination__item _link _button _next smartLink']/@href").extract_first()
        if next_link:
            yield response.follow(next_link, self.parse)

    def book_parse(self, response: HtmlResponse):
        name_books = response.xpath("//h1//text()").extract_first()
        price = response.xpath("//span[@class='app-price product-sidebar-price__price-old']//text()").extract_first()
        price_discount = response.xpath("//span[@class='app-price product-sidebar-price__price']//text()").extract_first()
        link = response.url
        time.sleep(1)
        authors = response.xpath("//div[contains(@class, 'product-detail-page__characteristic-short')]//div[@class='product-characteristic__item'][1]//a//text()").extract()
        rating = response.xpath("//div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/button[1]/span[2]//text()").extract_first()
        print(1)
        yield BooksItem(name_books=name_books, price=price, price_discount=price_discount,
                        link=link, authors=authors, rating=rating)

    # def process_reviews(self, response):
    #     # Здесь вы можете обрабатывать данные из отзывов
    #     data = json.loads(response.text)
    #     rating = data['data'][0]['bookRating']
    #     authors = data['data'][0]['authorName']
    #     yield BooksItem(rating=rating, authors=authors)
