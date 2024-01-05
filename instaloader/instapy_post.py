from instapy import InstaPy
import os
proxy_url_with_auth = '45.146.88.162:8000'
os.environ["HTTPS_PROXY"] = proxy_url_with_auth

bot = InstaPy(username='voyage_and_more', password='klassadidas0147')

bot.login()


caption = 'Новостной пост'
image_path = '/home/dima_protasevich/Изображения/bear.jpg'
bot.upload_photo(image_path, caption=caption)

bot.end()
