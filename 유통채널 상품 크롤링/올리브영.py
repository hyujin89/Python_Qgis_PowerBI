# 올리브영 행사 정보 크롤링

import re
import time 
from bs4 import BeautifulSoup 
from selenium import webdriver 
import openpyxl 


options = webdriver.ChromeOptions() #웹드라이버 크롬
driver = webdriver.Chrome("./chromedriver", options = options) #옵션으로 크롬 드라이버 실행


url = 'https://www.oliveyoung.co.kr/store/main/getBestList.do?dispCatNo=900000100100001&fltDispCatNo=10000020002&pageIdx=1&rowsPerPage=8' # 글어올 사이트
driver.get(url) 
time.sleep(1)


### URL주소만 수정해주면 됨 ###

# 전체 랭킹 : https://www.oliveyoung.co.kr/store/main/getBestList.do?dispCatNo=900000100100001&fltDispCatNo=&pageIdx=1&rowsPerPage=8
# 식품 랭킹 : https://www.oliveyoung.co.kr/store/main/getBestList.do?dispCatNo=900000100100001&fltDispCatNo=10000020002&pageIdx=1&rowsPerPage=8
# 남성 랭킹 : https://www.oliveyoung.co.kr/store/main/getBestList.do?dispCatNo=900000100100001&fltDispCatNo=10000010007&pageIdx=1&rowsPerPage=8
# 건강 랭킹 : https://www.oliveyoung.co.kr/store/main/getBestList.do?dispCatNo=900000100100001&fltDispCatNo=10000020001&pageIdx=1&rowsPerPage=8



soup = BeautifulSoup(driver.page_source, 'html.parser') 

wb = openpyxl.Workbook() 
sheet = wb.active #시트 활성화
sheet.append(["순위", "브랜드", "상품명", "가격", "행사내용"]) 

soup = BeautifulSoup(driver.page_source, 'html.parser')

items = soup.select('div.prd_info') 

for item in items:
    tit = item.find('p', attrs={'class': 'prd_price'}).get_text() 
    price = item.find('div', attrs={'class': 'prd_name'}).get_text() 
    flg = item.find('span', attrs={'class': 'thumb_flag best'}).get_text()
    img = item.find('span', attrs={'class': 'tx_brand'}).get_text()
   

    try:
        sale = item.find('p', attrs={'class': 'prd_flag'}).get_text() 
            
    except:
        sale = "행사 없음"
    

    print(tit,price,flg,img,sale) 
    sheet.append([flg+"위",img,price,tit,sale]) 


driver.close()
wb.save('올리브영.xlsx') 
print('크롤링 완료') 


