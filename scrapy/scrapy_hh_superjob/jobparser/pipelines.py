# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import re

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError


class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancies

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        salary = item['salary']
        # collection.insert_one(item)
        # del item['salary']
        self.process_salary(salary, spider.name, item, collection)
        return item

    def process_salary(self, salary, site, item, collection):
        if site == 'hhru':
            if len(salary) == 8:
                item['min_salary'] = int(salary[1].replace(' ', '').replace('\xa0', ''))
                try:
                    item['max_salary'] = int(salary[3].replace(' ', '').replace('\xa0', ''))
                except IndexError:
                    compensation_max = None
                item['currency_symbol_match'] = re.search(r'([₽$€£])', salary[5]).group(1)
            elif len(salary) == 6:
                item['min_salary'] = int(salary[1].replace(' ', '').replace('\xa0', ''))
                try:
                    item['max_salary'] = None
                except IndexError:
                    compensation_max = None
                item['currency_symbol_match'] = re.search(r'([₽$€£])', salary[3]).group(1)
            else:
                item = item
            del item['salary']
            existing_record = collection.find_one({'url': item['url']})
            if not existing_record:
                try:
                    collection.insert_one(item)
                except DuplicateKeyError:
                    print("Такая вакансия уже существует: ", item['url'])
        elif site == 'superjob':
            if len(salary) == 9:
                try:
                    item['min_salary'] = int(salary[0].replace(' ', '').replace('\xa0', ''))
                except ValueError:
                    item['min_salary'] = int(salary[0].replace(' ', '').replace('\xa0', ''))
                try:
                    item['max_salary'] = int(salary[4].replace(' ', '').replace('\xa0', ''))
                except IndexError:
                    item['max_salary'] = int(salary[4].replace(' ', '').replace('\xa0', ''))
                item['currency_symbol_match'] = re.search(r'([₽$€£])', salary[6]).group(1)
            elif len(salary) == 1:
                item['min_salary'] = salary[0]
                item['max_salary'] = None
                item['currency_symbol_match'] = None
            elif len(salary) == 5:
                item['min_salary'] = None
                max_salary_str = salary[2].replace('\xa0', '').replace(' ', '')[:-1]
                item['max_salary'] = int(max_salary_str) if max_salary_str else None
                item['currency_symbol_match'] = salary[2][-1:]
                print(1)
            else:
                item = item
            del item['salary']
            existing_record = collection.find_one({'url': item['url']})
            if not existing_record:
                try:
                    collection.insert_one(item)
                except DuplicateKeyError:
                    print("Такая вакансия уже существует: ", item['url'])

