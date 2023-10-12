import re
from bs4 import BeautifulSoup
from selenium import webdriver
import openpyxl
import time
from selenium.webdriver.support import expected_conditions as EC
from openpyxl import Workbook

# 백그라운드로 웹브라우저 실행
options = webdriver.ChromeOptions()
# options.add_argument('--headless')
driver = webdriver.Chrome("./chromedriver", options = options)
driver.implicitly_wait(6)

# 이마트24 url 정보 설정
url = 'https://corporate.homeplus.co.kr/store/hypermarket.aspx'
driver.get(url)

# 해당 페이지 HTML 정보 추출
soup = BeautifulSoup(driver.page_source, 'html.parser')

search_box = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_Button1"]').click() 
time.sleep(1)
# search_box = driver.find_element_by_xpath('/html/body/div[2]/div/div/div[3]/div[2]/div[1]/div[1]/div[2]/div[1]/ul/li[1]').click() 
# time.sleep(1)
# search_box = driver.find_element_by_xpath('/html/body/div[2]/div/div/div[3]/div[2]/div[1]/div[1]/div[3]/div/div').click() 
# time.sleep(1)

wb = openpyxl.Workbook()
sheet = wb.active
sheet.append(['점포명', '주소', '위도', '경도'])


items = BeautifulSoup(driver.page_source, 'html.parser')

for item in items:
    # 전체 페이지 수만큼 반복
    title_spans = soup.select("span.name")
    search_box = driver.find_element_by_xpath('#content > div > div > div > ul > li:nth-child(1) > div:nth-child(1) > h3 > span.name > a').click()
    
    place_divs = soup.select("td")
    search_box = driver.find_element_by_xpath('//*[@id="content"]/div/div/div/div[3]/a').click()    
    time.sleep(1)


    #store_detail01 > table > tbody > tr:nth-child(1) > td


    title_spans = soup.select("span.title")
    place_divs = soup.select("div.place")

    

    print(title_spans.text.strip(), place_divs.text.strip())

wb.save("이마트24 신버전.xlsx")
