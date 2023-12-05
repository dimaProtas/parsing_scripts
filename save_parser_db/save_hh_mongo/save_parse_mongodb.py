import json
import string
import re
import unicodedata
from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint


# Функция для записи вакансий в MongoDB
def write_mongo_parse_hh(list_job):
    client = MongoClient('localhost', 27017)
    db = client['hh']

    hh = db.hh

    unique_field = 'link_job'
    vacancy_new = 0

    for job in list_job:
        result = hh.update_one(
            {unique_field: job[unique_field]},
            {'$set': job},
            upsert=True
        )

        if result.upserted_id:
            vacancy_new += 1
            print('Вакансия успешно добавлена в MongoDB!')
        else:
            pprint(f'Вакансия уже существует в MongoDB, пропускаем')

    print(f'{len(list_job)} вакансий найдено!')
    print(f'Вакансий записано {vacancy_new}')


url = 'https://hh.ru/'
url_search = url + 'search/vacancy'
#https://hh.ru/search/vacancy?search_field=name&search_field=company_name&search_field=description&enable_snippets=false&text=Python+backend+%D1%80%D0%B0%D0%B7%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D1%87%D0%B8%D0%BA


def parsing_hh(url_search):
    def clean_text(text):
        # Оставляем только печатаемые символы
        printable_chars = set(string.printable)
        cleaned_text = ''.join(filter(lambda x: x in printable_chars, text))

        return cleaned_text.strip()

    header = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    }

    params = {
        'text': input('Введите параметр запроса HH: \n'),
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
        all_list_vacancy = scope.find('div', {'id': 'a11y-main-content'})
        try:
            items = all_list_vacancy.find_all('div', {'class': 'serp-item'})
        except AttributeError:
            pass
        try:
            next_page = scope.find('a', {'data-qa': 'pager-next'})['href']
            next_link = url + next_page
        except TypeError:
            next_link = None

        for i in items:
            item = i.find('a')
            job_name = unicodedata.normalize("NFKD", item.getText())
            job_link = item['href']
            try:
                company = i.find('a', {'class': 'bloko-link bloko-link_kind-tertiary'})
                company_name = unicodedata.normalize("NFKD", company.getText())
                company_link = url + company['href']
            except AttributeError:
                company_name = None
                company_link = None
            company_addres = unicodedata.normalize("NFKD", i.find('div', {'data-qa': 'vacancy-serp__vacancy-address'}).getText())
            skill = i.find('div', {'data-qa': 'vacancy-serp__vacancy-work-experience'}).getText()
            try:
                compensation = i.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}).getText()
                compensation_list = clean_text(compensation).split(' ')
                if len(compensation_list) > 1:
                    compensation_min = int(compensation_list[0])
                    try:
                        compensation_max = int(compensation_list[2])
                    except IndexError:
                        compensation_max = None
                    currency_symbol_match = re.search(r'([₽$€£])', compensation).group(1)
                else:
                    compensation_min = int(compensation_list[0])
                    compensation_max = None
                    currency_symbol_match = re.search(r'([₽$€£])', compensation).group(1)
            except AttributeError:
                compensation_min = None
                compensation_max = None
                currency_symbol_match = None
            # try:
            #     is_home = i.find('span', {'data-qa': 'vacancy-label-remote-work-schedule'}).getText()
            # except ValueError:
            #     is_home = ''

            item_data = {
                'company': {
                    'company_name': company_name,
                    'company_link': company_link,
                    'company_addres': company_addres,
                },
                'name_job': job_name,
                'compensation': {
                    'compensation_min': compensation_min,
                    'compensation_max': compensation_max,
                    'currency_symbol_match': currency_symbol_match
                },
                'link_job': job_link,
                'skill': skill,
            }

            vacancy_all.append(item_data)


    # pprint(len(vacancy_all))
    write_mongo_parse_hh(vacancy_all)  # сохраняем вакансии в MongoDB


parsing_hh(url_search)
