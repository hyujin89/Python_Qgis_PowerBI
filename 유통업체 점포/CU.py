from ast import Break
import time
import re
from tkinter import BROWSE
from webbrowser import BaseBrowser
import openpyxl
import csv 

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup #html 코드 가져오기
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()
# options.add_argument('--headless')
driver = webdriver.Chrome("./chromedriver", options = options)
 
url= ('https://cu.bgfretail.com/store/list.do?category=store')  
driver.implicitly_wait(5)

driver.get(url) # url 담기

soup = BeautifulSoup(driver.page_source, 'html.parser') #소스 html에 담기 

search_box = driver.find_element_by_xpath('//*[@id="result_search"]/div/div[2]/ul/li[11]/div').click() # 이거 1 ~ 11까지 있음  1이 가장 많은거
search_box = driver.find_element_by_xpath('//*[@id="paging"]/a').click()

wb = openpyxl.Workbook() # 저장할 엑셀 시트 열기
sheet = wb.active #시트 활성화
sheet.append(["점포명", "주소", "제공서비스"]) # 시트 맨위에 고정으로 박아두기

for page in range(1, 4000):
    # 시도 셀렉션 바 추출 및 값 설정
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    try:
        search_box = driver.find_element_by_xpath('//*[@id="paging"]/a[2]').click()
        time.sleep(0.7)
        
        items = soup.select('#result_search > div.result_store > div.detail_store > table > tbody > tr') #이건 그 상품의 박스 하나임

        for item in items:
                    tit = item.find('span', attrs={'class': 'name'}).get_text()  
                    flg = item.find('a', attrs={'href': '#'}).get_text() 
                    
    
                    print(f'{page} Completed!')
                    sheet.append([tit, flg])
    except:
        #마지막 페이지에 자료를 못끌어와서 만듦
        items = soup.select('#result_search > div.result_store > div.detail_store > table > tbody > tr') 
        
        for item in items:                
                    tit = item.find('span', attrs={'class': 'name'}).get_text()  
                    flg = item.find('a', attrs={'href': '#'}).get_text() 
                    
    
                    print(f'{page} Completed!')
                    sheet.append([tit, flg])
        break
            
wb.save('CU11.xlsx') 
driver.quit() 

print('System Completed!!!')   
