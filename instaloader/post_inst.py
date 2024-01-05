from instabot import Bot
import os
import shutil
# proxy_url_with_auth = '45.146.88.162:8000'
# os.environ["HTTPS_PROXY"] = proxy_url_with_auth

def clean_up(i):
    dir = "config"
    remove_me = "imgs\{}.REMOVE_ME".format(i)
    # checking whether config folder exists or not
    if os.path.exists(dir):
        try:
            # removing it so we can upload new image
            shutil.rmtree(dir)
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))
    if os.path.exists(remove_me):
        src = os.path.realpath("imgs\{}".format(i))
        os.rename(remove_me, src)


def upload_post(i):
    bot = Bot()

    bot.login(username='voyage_and_more', password='klassadidas0147', proxy='45.146.88.162:8000')

    caption = 'Новостной пост'
    # image_path = '/home/dima_protasevich/Изображения/bear.jpg'
    bot.upload_photo(i, caption=caption)
    bot.logout()


if __name__ == '__main__':
    # введите название вашего изображения ниже
    image_name = '/home/dima_protasevich/Изображения/bot_bear.jpg'
    clean_up(image_name)
    upload_post(image_name)

