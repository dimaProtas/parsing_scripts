import requests
from pprint import pprint


key = "ZKtj1diIQnEttO0dM46rmuXXQnzor5pDCuZNgWcL"

#https://api.nasa.gov/EPIC/api/natural/images?api_key=DEMO_KEY

response = requests.get(f"https://api.nasa.gov/EPIC/api/natural/images?api_key={key}")

if response.status_code == 200:
    data = response.json()
    if data:
        image_name = data[0]['image']
        date = data[0]['date']

        base_url = "https://api.nasa.gov/EPIC/archive/natural/"
        api_key = f"?api_key={key}"

        # Пример формата даты: 2019-05-30
        formatted_date = date.split()[0].replace('-', '/')

        # Сформируйте полный URL
        full_image_url = f"{base_url}{formatted_date}/png/{image_name}.png{api_key}"

        # Теперь вы можете передать full_image_url в шаблон или в другое место для отображения.
        print(full_image_url)
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")


# if response.status_code == 200:
#     data = response.json()
#     # pprint(data)
#     image_name = data[0]['image']
#     # print(data[0]['attitude_quaternions'])
#     # print(f'{data["date"]}')
#     # print(data['caption'])
#
#     base_url = "https://api.nasa.gov/EPIC/archive/natural/2019/05/30/png/"
#     api_key = f"/?api_key=DEMO_KEY"
#
#     # Сформируйте полный URL
#     full_image_url = base_url + image_name + '.png' + api_key
#
#     # Теперь вы можете передать full_image_url в шаблон или в другое место для отображения.
#     print(full_image_url)
