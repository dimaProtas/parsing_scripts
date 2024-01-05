import json
from datetime import datetime
import instaloader

USER = 'dima_protasevich92'
PASSWORD = "protasadidas0147588"
SESSION_FILE = 'inst_session.txt'
import os
proxy_url_with_auth = '195.154.184.80:8080'
# proxy_url_with_auth = '45.146.88.162:8000'
os.environ["HTTPS_PROXY"] = proxy_url_with_auth


# Создание экземпляра класса Instaloader
L = instaloader.Instaloader()


if os.path.exists(SESSION_FILE):
    if L.load_session_from_file(USER, SESSION_FILE):
        print(f"Не удалось загрузить сессию из файла '{SESSION_FILE}'. Возможно, файл поврежден.")
    else:
        print(f"Сессия загружена из file: '{SESSION_FILE}' успешно!")
else:
    L.login(user=USER, passwd=PASSWORD)
    L.save_session_to_file(SESSION_FILE)
    print(f"Сессия сохранена в file: '{SESSION_FILE}' !")


profile = instaloader.Profile.from_username(L.context, 'kochirishka23')
# posts = profile.get_posts()
# for p in posts:
#     L.download_post(p, target='post')
print(profile)


# post = instaloader.Post.from_shortcode(L.context, 'CsgoxJnIB8S')
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


# L.download_pic('moto', post.url, post.date, '.jpg')
# L.download_post(post, target='post')
# print('Успех!')
