import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint

# https://hh.ru/search/vacancy?from=suggest_post&ored_clusters=true&area=1&hhtmFrom=vacancy_search_list&hhtmFromLabel=vacancy_search_line&search_field=name&search_field=company_name&search_field=description&text=Python+backend+%D1%80%D0%B0%D0%B7%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D1%87%D0%B8%D0%BA&enable_snippets=false

header = {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",}

url = 'https://hh.ru/'

url_g = 'https://www.google.com/'

params = {
    # 'from': suggest_post,
    # 'ored_clusters': True,
    # 'area': 1,
    # 'hhtmFrom': vacancy_search_list,
    # 'hhtmFromLabel': vacancy_search_line,
    # 'search_field': name,
    # 'search_field': company_name,
    'text': 'Python Backend-разработчик'
}


# response = requests.get(url, headers=header, params=params)
response = requests.get(url_g + 'search/vacancy', headers=header, params=params)

if response.status_code == 200:
    # data = response.json()
    # pprint(response.text)
    html = response.text
    scope = bs(html, 'lxml')  #html.parser

    div = scope.find('div')
    pprint(len(list(div.children)))
    child_div = div.findChildren(recursive=False)
    pprint(child_div)
    pprint(div.parent)
    pprint(div.previous)
    pprint(child_div)
    # with open('google.html', 'w') as f:
    #     f.write(a)


#bloko-column