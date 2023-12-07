from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, INT, VARCHAR, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from lenta_news import lenta_parser
from news_mail_parser import news_mail_parser


engine = create_engine('sqlite:///news.db', echo=True)
Base = declarative_base()


class NewsModel(Base):
    __tablename__ = 'news'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    news_name = Column(String)
    date_news = Column(String)
    link_news = Column(String)
    source_news = Column(String)

    def __init__(self, news_name, date_news, link_news, source_news):
        self.news_name = news_name
        self.date_news = date_news
        self.link_news = link_news
        self.source_news = source_news


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

session = Session()

new_news = 0
news_list = news_mail_parser() + lenta_parser()
print(news_list)
for news in news_list:
    existing_record = session.query(NewsModel).filter_by(
        news_name=news['news_name'],
        date_news=news['date_news'],
        link_news=news['link_news'],
        source_news=news['source_news'],
    ).first()

    if existing_record is None:
        session.add(NewsModel(news['news_name'],
                              news['date_news'],
                              news['link_news'],
                              news['source_news'],
                              ))
        new_news += 1
    print(f'Сохранено {new_news} новости.')
session.commit()
session.close()
