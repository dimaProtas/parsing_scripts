import requests
from lxml import html
from pprint import pprint


def lenta_parser():
    url = 'https://lenta.ru/'

    header = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        }

    response = requests.get(url, headers=header)

    if response.status_code == 200:
        dom = html.fromstring(response.text)
        items = dom.xpath("//a[contains(@class, 'card-mini')] | //a[contains(@class, 'card-big')] ")
        result = []
        for item in items:
            name_news = item.xpath(".//h3//text()")
            date_news = ','.join(item.xpath(".//div[@class='card-mini__info']//text() | .//div[@class='card-big__info']//text()"))
            link_news = url + item.xpath("./@href")[0]

            news = {
                "news_name": name_news[0],
                "source_news": "lenta.ru",
                "date_news": date_news,
                "link_news": link_news
            }

            result.append(news)

        print(f'Получено новостей {len(result)} с lenta.ru')
        return result


# lenta_parser()
