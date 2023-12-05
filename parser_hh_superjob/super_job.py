import json
import string
import re
import unicodedata

import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint


url_super_job = 'https://www.superjob.ru/'
url_search = url_super_job + 'vacancy/search'

#https://www.superjob.ru/vacancy/search/?keywords=python%20backend&geo%5Bt%5D%5B0%5D=4

def parsing_super_job(url_search):
    def clean_text(text):
        # Оставляем только печатаемые символы
        printable_chars = set(string.printable)
        cleaned_text = ''.join(filter(lambda x: x in printable_chars, text))

        return cleaned_text.strip()

    header = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    }

    params = {
        'keywords': input('Введите искомую вакансию: \n'),
        # 'page': 0,
    }

    vacancy_all = []
    next_link = url_search

    while next_link:
        response = requests.get(next_link, headers=header, params=params)

        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            break

        html = response.text
        scope = bs(html, 'lxml') #html.parser
        # res = scope.find_all(attrs={'class': 'bloko-column'})
        all_list_vacancy = scope.find('div', {'class': '_1dYCz _2MONE'})

        next_link_scope = scope.find('a', {'class': 'f-test-link-Dalshe'})
        if next_link_scope != None:
            next_link = url_super_job + next_link_scope['href']
        else:
            next_link = None


        try:
            items = all_list_vacancy.find_all('div', {'class': '_2bKwW _1L7d1'})
        except AttributeError:
            pass

        for i in items:
            item = i.find('a')
            job_name = item.getText()
            job_link = url_super_job + item['href']
            compensation = i.find('span', {'class': '_2eYAG'}).getText()
            compensation_list = clean_text(compensation).split(' ')
            try:
                currency_symbol_match = re.search(r'([₽$€£])', compensation).group(1)
            except AttributeError:
                currency_symbol_match = None

            if len(compensation_list) > 1:
                min_compensation = int(compensation_list[0])
                max_compensation = int(compensation_list[1])
            else:
                min_compensation = int(compensation_list[0])
                max_compensation = None

            try:
                company = i.find('span', {'class': '_3nMqD'})
                company_name = company.getText()
                company_link = url_super_job + company.next_element['href']
            except AttributeError:
                company_name = None
                company_link = None
            print(1)

            item_data = {
                'company_name': company_name,
                'company_link': company_link,
                'name_job': job_name,
                'min_compensation': min_compensation,
                'max_compensation': max_compensation,
                'currency_symbol_match': currency_symbol_match,
                'link_job': job_link,
            }

            vacancy_all.append(item_data)
    # print(f'Записанно {len(vacancy_all)} вакансий {params["keywords"]}')
    # pprint(vacancy_all)


    # pprint(len(vacancy_all))
    with open(f'{params.get("keywords")}_sj.json', 'w') as f:
        for vacancy in vacancy_all:
            # Преобразование словаря в строку JSON и запись в файл
            json.dump(vacancy, f, ensure_ascii=False)
            f.write('\n')  # Добавление новой строки между записями
    pprint(f'Записано в фаил {len(vacancy_all)} вакансий успешно!')


parsing_super_job(url_search)
