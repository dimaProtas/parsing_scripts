import requests
from PIL import Image
from io import BytesIO
from pprint import pprint

key = 'ZKtj1diIQnEttO0dM46rmuXXQnzor5pDCuZNgWcL'

# Координаты и дата для получения изображения
lon = 100.75
lat = 1.5
date = '2023-11-01'

# Формирование URL
url = f"https://api.nasa.gov/planetary/earth/imagery?lon={lon}&lat={lat}&date={date}&api_key={key}"

response = requests.get(url)

if response.status_code == 200:
    # Получение бинарных данных изображения
    image_data = response.content

    # Открытие изображения с использованием PIL
    image = Image.open(BytesIO(image_data))

    # Сохранение изображения
    image.save('earth_image.jpg')

    print("Image saved successfully.")
else:
    print(f"Failed to fetch image. Status code: {response.status_code}")

