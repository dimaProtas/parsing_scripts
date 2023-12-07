import requests
from lxml import html
from pprint import pprint


url = 'https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2380057.m570.l1313&_nkw=sony&_sacat=0'

header = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    }


requests = requests.get(url, headers=header)

if requests.status_code == 200:
    dom = html.fromstring(requests.text)
    items = dom.xpath("//ul[@class='srp-results srp-list clearfix']/li[@class='s-item s-item__pl-on-bottom']")
    result = []
    for item in items:
        name = item.xpath(".//a//span[@role='heading']//text()")
        price = item.xpath(".//span[@class='s-item__price']//text()")
        from_city = item.xpath(".//span[@class='s-item__location s-item__itemLocation']//text()")

        sony = {
            "name": name[0],
            "price": ','.join(price),
            "from_city": from_city[0],
        }

        result.append(sony)

    pprint(result)
    
