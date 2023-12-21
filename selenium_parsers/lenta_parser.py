from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

chrome_options = Options()
chrome_options.add_argument('start-maximized')
driver = webdriver.Chrome('./chromedriver.exe',options=chrome_options)

driver.get('https://lenta.com/catalog/frukty-i-ovoshchi/')

button = WebDriverWait(driver,10).until(
    EC.presence_of_element_located((By.CLASS_NAME,'store-notification__button--submit'))
)

# button = driver.find_element_by_class_name('store-notification__button--submit')
button.click()

button = WebDriverWait(driver,10).until(
    EC.element_to_be_clickable((By.CLASS_NAME,'store-notification__button--submit'))
)
button.click()

driver.refresh()

button = WebDriverWait(driver,10).until(
    EC.element_to_be_clickable((By.CLASS_NAME,'cookie-usage-notice__button'))
)
button.click()
pages = 0


while True:
    try:
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'catalog-grid-container__pagination-button'))
        )
        button.click()
        pages +=1
    except:
        print(f'Р Р°СЃРєСЂС‹С‚РёРµ {pages} СЃС‚СЂР°РЅРёС† РѕРєРѕРЅС‡РµРЅРѕ РёР»Рё РѕС€РёР±РєР°')
        break

goods = driver.find_elements_by_class_name('sku-card-small-container')
for good in goods:
    print(good.find_element_by_class_name('sku-card-small__title').text)
    print('Р¦РµРЅР° РїРѕ Р°РєС†РёРё: ', good.find_element_by_class_name('sku-prices-block__price').text)