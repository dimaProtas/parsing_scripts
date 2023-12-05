from pymongo import MongoClient
from pprint import pprint


client = MongoClient('localhost', 27017)
db = client['hh']

hh = db.hh


# Поиск всех вакансий, поле _id не показывать
def serch_all_vacancy():
    list_search = []
    for i in hh.find({}, {'_id': False}):
        list_search.append(i)
        # pprint(i)
    print(f'Всего вакансий: {len(list_search)}')


# Поиск вакансий по максимальной и минимальной зп
def vacancy_compensation():
    min_compensation = int(input('Введите минимальную зп: \n'))
    max_compensation = int(input('Введите максимальную зп: \n'))

    vac = []
    for i in hh.find({'compensation.compensation_min': {'$gt': min_compensation},
                      'compensation.compensation_max': {'$lt': max_compensation}}):
        vac.append(i)
        pprint(i)
    print(f'По запросу получено {len(vac)} записи.')


# serch_all_vacancy()

# hh.delete_many({})

# vacancy_compensation()
