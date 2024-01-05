import json
import time
from datetime import datetime
import instaloader
import pandas as pd
import requests

# USER = 'dima_protasevich92'
# PASSWORD = "protasadidas0147588"
USER = 'voyage_and_more'
PASSWORD = 'klassadidas0147'
# Ваш прокси-сервер
SESSION_FILE = 'voyage'
import os
# proxy_url_with_auth = '195.154.184.80:8080'
proxy_url_with_auth = '45.146.88.162:8000'
os.environ["HTTPS_PROXY"] = proxy_url_with_auth

# Создание сессии requests с использованием прокси
# proxies = {
#     'http': proxy_url,
#     'https': proxy_url,
# }
#
# session = requests.Session()
# session.proxies = proxies
#
# response = session.get('https://www.instagram.com/')
# if response.status_code == 200:
#     print(response.text)
# else:
#     print(response.status_code)


# Создание экземпляра класса Instaloader
L = instaloader.Instaloader(max_connection_attempts=1, request_timeout=300)


try:
    L.load_session_from_file(USER)
    print(f"Сессия загружена из файла по умолчанию успешно!")
except FileNotFoundError:
    L.login(user=USER, passwd=PASSWORD)
    L.save_session_to_file()
    print(f"Сессия сохранена в file по умолчанию!")


profile = instaloader.Profile.from_username(L.context, 'dima_protasevich92')
posts = profile.get_posts()
for p in posts:
    # L.download_post(p, target='post')
    print(p.url)
    print(p.caption)
    print(p.profile)
    L.download_post(p, target='post')
    print('-----------------------------------')
print('Autorizen:', L.context.is_logged_in)

# print(profile, '\n', posts)
# for index, post in enumerate(posts, 1):
#     print(index, post)
#     L.download_post(post, target='post')
#     print('Ok dowload')
#     time.sleep(2)


# posts = profile.get_posts()

# def serialize_datetime(obj):
#     if isinstance(obj, datetime):
#         return obj.isoformat()
#     raise TypeError("Type not serializable")
#
# with open('int_data.json', 'a') as f:
#     for post in posts:
#         data = {
#             'post.profile': post.profile,
#             'date_utc': serialize_datetime(post.date_utc),
#             'post.url': post.url,
#             'post.date': serialize_datetime(post.date),
#         }
#
#         json.dump(data, f, ensure_ascii=False)
#         # f.write(data)
#         f.write('\n')
#     print('Посты записаны!')



# L.download_post(post, target='post')
# L.download_pic('moto', post.url, post.date, '.jpg')
# print("ID поста:", post.mediaid)
# print("Код поста:", post.shortcode)
# print("Ссылка на пост:", post.url)
# print("Автор поста:", post.owner_username)
# print("Дата создания:", post.date_utc)
# print("Текст поста:", post.caption)
# print("Количество лайков:", post.likes)
# print("Количество комментариев:", post.comments)
# print("Ссылка на изображение:", post.url)
# print('Успех!', post.url)


# L.download_post(post, target='post')
