from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time

driver = webdriver.Chrome('./chromedriver.exe')

driver.get('https://geekbrains.ru/login')

login = driver.find_element_by_id('user_email')
login.send_keys('study.ai_172@mail.ru')

passw = driver.find_element_by_id('user_password')
passw.send_keys('Password172')

passw.send_keys(Keys.ENTER)
time.sleep(0.5)
profile = driver.find_element_by_class_name('avatar')
driver.get(profile.get_attribute('href'))

edit_profile = driver.find_element_by_class_name('text-sm')
driver.get(edit_profile.get_attribute('href'))

gender = driver.find_element_by_name('user[gender]')
# options = gender.find_elements_by_tag_name('option')
#
# for option in options:
#     if option.text == 'Р–РµРЅСЃРєРёР№':
#         option.click()

select = Select(gender)
select.select_by_value('2')

gender.submit()

driver.back()
driver.forward()
driver.refresh()

driver.close()
