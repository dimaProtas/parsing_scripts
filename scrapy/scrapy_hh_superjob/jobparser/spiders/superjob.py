import scrapy
from scrapy.http import HtmlResponse

from jobparser.items import JobparserItem


class SuperjobSpider(scrapy.Spider):
    name = "superjob"
    allowed_domains = ["superjob.ru"]
    start_urls = ["https://russia.superjob.ru/vacancy/search/?keywords=Python",]

    def parse(self, response: HtmlResponse):
        vacancy_all = response.xpath("//div[contains(@class, '_3VMkc')]//a[contains(@class, '_2_Rn8')]/@href").extract()
        for vacancy in vacancy_all:
            yield response.follow(vacancy, callback=self.vacancy_parse)
        next_page = response.xpath("//a[contains(@class, 'f-test-link-Dalshe')]/@href").extract_first()
        if next_page:
            yield response.follow(next_page, self.parse)
    def vacancy_parse(self, response: HtmlResponse):
        name = response.xpath("//h1//text()").extract_first()
        salary = response.xpath("//span[@class='_4Gt5t _3Kq5N']//text()").extract()
        url = response.url
        yield JobparserItem(name=name, salary=salary, url=url)
