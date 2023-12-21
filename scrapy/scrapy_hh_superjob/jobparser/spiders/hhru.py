import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://izhevsk.hh.ru/search/vacancy?area=&fromSearchLine=true&st=searchVacancy&text=python',
                  ]

    def parse(self, response: HtmlResponse):
        vacansy_links = response.xpath("//a[@data-qa='serp-item__title']/@href").extract()
        for link in vacansy_links:
            yield response.follow(link, callback=self.vacansy_parse)
        next_page = response.xpath("//a[@data-qa='pager-next']/@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def vacansy_parse(self, response: HtmlResponse):
        name = response.xpath("//h1[@data-qa='vacancy-title']//text()").extract_first()
        salary = response.xpath("//div[@data-qa='vacancy-salary']//text()").extract()
        url = response.url
        yield JobparserItem(name=name, salary=salary, url=url)
