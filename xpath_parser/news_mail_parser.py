import requests
from lxml import html
from pprint import pprint


def news_mail_parser():
    url = 'https://news.mail.ru/'

    header = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        }

    response = requests.get(url, headers=header)

    if response.status_code == 200:
        dom = html.fromstring(response.text)
        items = dom.xpath("//li[contains(@class, 'list')] | //a[@class='newsitem__title link-holder'] | //span[contains(@class, 'js-topnews__item')]")
        result = []
        for item in items:
            link_news = item.xpath(".//@href")[0]

            news_response = requests.get(link_news, headers=header)

            if news_response.status_code == 200:
                dom_news = html.fromstring(news_response.text)
                try:
                    news_name = dom_news.xpath("//h1[@class='hdr__inner']//text()")[0]
                except IndexError:
                    news_name = None
                try:
                    date_news = dom_news.xpath("//span[@class='note__text breadcrumbs__text js-ago']//text()")[0]
                except IndexError:
                    date_news = None
                try:
                    source_news = dom_news.xpath("//a[@class='link color_gray breadcrumbs__link']//text() | //span[@class='link link_underline link_pointer js-source-link']//text()")[0]
                except IndexError:
                    source_news = None

                news = {
                    "news_name": news_name,
                    "date_news": date_news,
                    "source_news": source_news,
                    "link_news": link_news,
                }

                # pprint(news)

                result.append(news)

        print(f'Получено новостей {len(result)} с news.mail.ru')
        return result


