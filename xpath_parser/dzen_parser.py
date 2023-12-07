import requests
from lxml import html
from pprint import pprint


url = 'https://dzen.ru/news?issue_tld=ru'

header = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    }

response = requests.get(url, headers=header)

if response.ok:
    pprint(response.text)
    dom = html.fromstring(response.text)
    items = dom.xpath("//div[contains(@class, 'mg-grid__col mg-grid__col_xs_')]")
    result = []
    for item in items:
        name_news = item.xpath(".//a[@class='mg-card__link']//text()")

        news = {
            "name_news": name_news,
        }
        result.append(news)

    pprint(result)
