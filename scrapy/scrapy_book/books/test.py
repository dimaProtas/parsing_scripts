import json

import requests


headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'X-Oauth-Client-Id': '6a56dbab-804b-4a39-b767-4bbfdc28d7e9',
    # 'isbn': 978-5-699-98630-9
}

response = requests.get('https://book24.ru/api/v1/catalog/product/reviews/livelib/?isbn=978-5-699-98630-9', headers=headers)

if response.status_code == 200:
    data = json.loads(response.text)
    print(data)
else:
    print(response.status_code)