from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time

chrome_options = webdriver.FirefoxOptions()
chrome_options.add_argument('--start-maximized')

# Укажите абсолютный путь к chromedriver в Options
# chrome_options.binary_location = "/opt/chrome-linux64/chrome"
chrome_options.binary_location = "/home/dima_protasevich/Documents/PycharmProjects/parsing_data/selenium_parsers/geckodriver"

# Создайте драйвер с использованием Options
driver = webdriver.Firefox()


driver.get('https://www.mvideo.ru/')


product = driver.find_elements(By.CLASS_NAME, 'popular-categories__list to-line-mobile-view ng-star-inserted')

# menu = driver.find_element(By.CLASS_NAME, 'catalog-button')
# menu.click()
#
# menu = driver.find_element(By.CLASS_NAME, 'notification__button')
# menu.click()

# comp_game = WebDriverWait(driver, 10).until(
#     EC.presence_of_element_located((By.CLASS_NAME, 'left-menu'))
# )

new = driver.find_element(By.XPATH, "//header/div[3]/div[1]/mvid-slide-panel[1]/div[1]/div[1]/mvid-floating-controls[1]/div[1]/div[1]/div[1]/div[3]/a[1]")
driver.get(new.get_attribute('href'))

time.sleep(1)
product_list = driver.find_elements(By.CLASS_NAME, 'plp__card-grid')
print(product_list)

for prod in product_list:
    print(prod.find_element(By.XPATH, "//a[@class='product-title__text']").text)

driver.close()
# login = driver.find_element(By.ID, 'user_email')
# login.send_keys('dima_protasevich92@mail.ru')
#
# passw = driver.find_element(By.ID, 'user_password')
# passw.send_keys('protasadidas0147588')
#
# passw.send_keys(Keys.ENTER)
#
# time.sleep(1)
# profile = driver.find_element(By.CLASS_NAME, 'mn-dropdown__list')
# driver.get(profile.get_attribute('href'))

# edit_profile = driver.find_element(By.CLASS_NAME, 'text-sm btn btn-primary relative inline-block wrap')
# driver.get(edit_profile.get_attribute('href'))


