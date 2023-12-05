from pymongo import MongoClient

# Подключение с паролем, но не работает
# host_ip = 'localhost'
# username = 'root'
# password = 'password'
# database_name = 'mydatabase'
#
# # Connection URI with authentication
# uri = f"mongodb://{username}:{password}@{host_ip}:27017/{database_name}"


client = MongoClient('localhost', 27017)
db = client['users_db']


users = db.users

# users.insert_one({"author": "Peter",
#                    "age": 78,
#                    "text": "is cool! Wildberry",
#                    "tags": ['cool', 'hot', 'ice'],
#                    "date": '14.06.1983'})
#
# users.insert_many([{"author": "Dima",
#                    "age": 31,
#                    "text": "i am boss!",
#                    "tags": ['cool', 'hot', 'ice'],
#                    "date": '12.02.1992'},
#                   {"author": "Paha",
#                    "age": 27,
#                    "text": "He lox",
#                    "tags": ['cool', 'hot', 'ice'],
#                    "date": '05.06.1996'},
#                   {"author": "Ira",
#                    "age": 37,
#                    "text": "Cool girl",
#                    "tags": ['cool', 'hot', 'ice'],
#                    "date": '14.06.1983'},]
#                   )

# for user in users.find({'author': 'Paha'}, {'_id': False, 'author': True, 'age': True, 'text': True}):
#     print(user)

# for user in users.find({}).sort('age', -1).limit(3):
#     print(user)

# for user in users.find({'age': {'$ne': 31}}):
#     print(user)

# for user in users.find({'$or': [{'author': 'Ira'}, {'age': 31}]}):
#     print(user)

data = {"author": "Alex",
                   "age": 100,
                   "text": "Lox moto!",
                   "tags": ['cool', 'hot', 'ice'],
                   "date": '13.02.1996'}

# users.update_many({'author': 'Dima'}, {'$set': data})  # Обновление
# users.replace_one({'author': 'Peter'}, data) # Замена

# users.delete_one({'author': 'Alex'}) # Удалить одну запись
users.delete_many({})  # Удалить все записи

for user in users.find({}):
    print(user)
