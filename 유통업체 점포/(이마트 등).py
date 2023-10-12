import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import pandas as pd

options = webdriver.ChromeOptions()
# options.add_argument('--headless')
driver = webdriver.Chrome("./chromedriver", options = options)

url = 'https://store.emart.com/branch/list.do?trcknCode=header_store'
driver.get(url)
driver.implicitly_wait(10)

emart_store = []
for i, store in enumerate(driver.find_elements_by_css_selector('#branchList > li > a'), 1):
    driver.execute_script('arguments[0].click();', store)
    time.sleep(1)

    name = store.text

    try:
        address = driver.find_element_by_css_selector('#conts > div > div.map-wrap > div.branch-info > div.branch-info1 > ul > li:nth-child(2) > dl > dd:nth-child(2)').text
    except NoSuchElementException:
        address = ''

    try:
        shopping_time = driver.find_element_by_css_selector('#conts > div > div.store-intro > div.cont > div.intro-wrap > ul > li:nth-child(1) > p:nth-child(3)').text
    except NoSuchElementException:
        shopping_time = ''

    try:
        closed_days = driver.find_element_by_css_selector('#conts > div > div.store-intro > div.cont > div.intro-wrap > ul > li.closed-day > p').text
    except NoSuchElementException:
        closed_days = ''

    try:
        customer_center = driver.find_element_by_css_selector('#conts > div > div.store-intro > div.cont > div.intro-wrap > ul > li:nth-child(3) > p').text
    except NoSuchElementException:
        customer_center = ''

    try:
        parking = driver.find_element_by_css_selector('#conts > div > div.store-intro > div.cont > div.intro-wrap > ul > li:nth-child(4) > p').text
    except NoSuchElementException:
        parking = ''

    emart_store.append({'점포명': name, '주소': address, '쇼핑시간': shopping_time,
                        '휴점일': closed_days, '고객센터': customer_center, '주차시설': parking})

    print(i, name)

df = pd.DataFrame(emart_store)
df.to_excel('이마트.xlsx', index = False)

driver.quit() # driver process shut down


