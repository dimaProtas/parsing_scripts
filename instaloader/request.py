import requests


# Ваш прокси-сервер
proxy_url = '45.146.88.162:8000'
# proxy_url = '195.154.184.80:8080'


# Создание сессии requests с использованием прокси
proxies = {
    'http': proxy_url,
    'https': proxy_url,
}

session = requests.Session()
session.proxies = proxies

response = session.get('https://instagram.com/')
if response.status_code == 200:
    print(response.text)
else:
    print(response.status_code)

