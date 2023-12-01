import requests
from pprint import pprint

key = '7597a8f63ca8b80d2aba19d9e8cab8bb'

header = {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",}

# https://api.openweathermap.org/data/2.5/weather?q={city name}&appid={API key}

link = "https://api.openweathermap.org/data/2.5/weather"

params = {
    "q": "Moscow",
    "appid": key
}

response = requests.get(link, headers=header, params=params)

if response.status_code == 200:
    data = response.json()
    # pprint(data)
    print(f'В городе {data["name"]} температура {data["main"]["temp"] - 273.15} градусов')
