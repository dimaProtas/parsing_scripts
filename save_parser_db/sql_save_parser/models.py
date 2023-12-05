from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, INT, VARCHAR, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///super_job.db', echo=True)
Base = declarative_base()


class SuperJobModel(Base):
    __tablename__ = 'super_job'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    company_name = Column(String)
    company_link = Column(String)
    name_job = Column(String)
    link_job = Column(String)
    min_compensation = Column(Integer)
    max_compensation = Column(Integer)
    currency_symbol_match = Column(String)

    def __init__(self, company_name, company_link, name_job, link_job, min_compensation, max_compensation,
                 currency_symbol_match):
        self.company_name = company_name
        self.company_link = company_link
        self.name_job = name_job
        self.link_job = link_job
        self.min_compensation = min_compensation
        self.max_compensation = max_compensation
        self.currency_symbol_match = currency_symbol_match


def create_session():
    Session = sessionmaker(bind=engine)
    return Session()


def create_table():
    Base.metadata.create_all(engine)


# Функция сохранения записей в БД SQL
def save_data_sj(parse_func, url_search):
    create_table()
    session = create_session()
    new_vacancy = 0

    for job in parse_func(url_search):
        existing_record = session.query(SuperJobModel).filter_by(
            company_name=job['company_name'],
            name_job=job['name_job'],
            min_compensation=job['min_compensation'],
            max_compensation=job['max_compensation'],
            currency_symbol_match=job['currency_symbol_match']
        ).first()

        if existing_record is None:
            session.add(SuperJobModel(job['company_name'],
                                      job['company_link'],
                                      job['name_job'],
                                      job['link_job'],
                                      job['min_compensation'],
                                      job['max_compensation'],
                                      job['currency_symbol_match'],
                                      ))
            new_vacancy += 1
    session.commit()
    session.close()
    print(f'Сохранено {new_vacancy} новых вакансий')


# Поиск вакансий
def search_vacancy_sj():
    min_compesation = input('Введите минимальную зп: \n')
    max_compesation = input('Введите максимальную зп: \n')

    create_table()
    session = create_session()

    for obj in session.query(SuperJobModel).filter(SuperJobModel.min_compensation > min_compesation,
                                                   SuperJobModel.max_compensation < max_compesation):
        print(f'Компания: {obj.company_name} \nВакансия: {obj.name_job} \n от {obj.min_compensation} \n '
              f'до {obj.max_compensation} {obj.currency_symbol_match} \n ----------------')

    session.close()


def delete_all_vacancy():
    create_table()
    session = create_session()

    for obj in session.query(SuperJobModel).all():
        session.delete(obj)

    session.commit()
    session.close()