from selenium import webdriver
import time
from pprint import pprint
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

chrome_options = Options()
chrome_options.add_argument('start-maximized')

driver = webdriver.Chrome()
driver.get('https://www.mvideo.ru/')
time.sleep(3)
items_list = []

while True:
    hits_part = driver.find_element_by_xpath(
        '//div[contains(text(),"Хиты продаж")]/ancestor::div[contains(@data-init,"gtm-push-products")]')
    items = hits_part.find_elements_by_class_name('sel-product-tile-title')
    time.sleep(15)

    for item in items:
        item_info = {}
        item_info['name'] = item.text
        item_info['link'] = item.get_attribute('href')
        price = item.get_attribute('data-product-info')
        price = price.split(',')
        price = price[0].split(': ')
        price = price[1].replace('\"','')
        item_info['price'] = price

#        if (not (item_info in items_list)) and item_info['name'] != '':
#            items_list.append(item_info)
        if (item_info['name'] != '') and (item_info not in items_list):
            items_list.append(item_info)

    actions = ActionChains(driver)
    actions.move_to_element(items[-1])
    actions.perform()

    try:
        button = WebDriverWait(hits_part, 15).until(
        EC.presence_of_element_located((By.XPATH, ".//a[@class='next-btn sel-hits-button-next']"))
        )
    except:
        break
pprint(items_list)
driver.quit()
