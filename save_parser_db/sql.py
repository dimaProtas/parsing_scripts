from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, INT, VARCHAR, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///users.db', echo=True)
Base = declarative_base()


class UsersModel(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    name = Column(String(100))
    fullname = Column(String)
    password = Column(String)
    age = Column(Integer)

    def __init__(self, name, fullname, password, age):
        self.name = name
        self.fullname = fullname
        self.password = password
        self.age = age


# Если еще нет таблицы в базе данных
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

session = Session()

# dima = UsersModel('Dima', 'Dima Protas', '1234', 31)
# session.add(dima)

# session.add_all([UsersModel("kolia", "Cool Kolian[S.A.]","kolia$$$", 28),
#                  UsersModel("zina", "Zina Korzina", "zk18", 54)])

for obj in session.query(UsersModel).filter(UsersModel.age > 30, UsersModel.age < 50):
    print(f'Имя: {obj.name} \n Полное имя: {obj.fullname} \n Возраст: {obj.age}')

session.commit()
session.close()
