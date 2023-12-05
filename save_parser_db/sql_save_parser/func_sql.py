from models import save_data_sj, search_vacancy_sj, delete_all_vacancy
from parser_sj import parsing_super_job


url_super_job = 'https://www.superjob.ru/'
url_search = url_super_job + 'vacancy/search'

# Вызоф ф-и добавления вакансий по названию факансии
save_data_sj(parsing_super_job, url_search)

# Вызов функции поиска вакансий по зп
# search_vacancy_sj()


# Удаление всех вакансий из бд
# delete_all_vacancy()