
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import time
import openpyxl
from selenium import webdriver

driver = webdriver.Chrome("./chromedriver")
driver.get('https://front.homeplus.co.kr/best?gnbNo=3')

req = driver.page_source
soup = BeautifulSoup(req, 'html.parser')

wb = openpyxl.Workbook()
sheet = wb.active
sheet.append(["상품명","가격","평점/리뷰"])


# items = soup.select("#root > div > div.css-1u9ias7-defaultStyle") #이건 그 상품의 박스 하나임

soup = BeautifulSoup(driver.page_source, 'html.parser')

items = soup.select('body > section > div.content-wrap > div.content-body.shop-search-wrap > div.content-wrap.mgb110 > div > div > div.tabbox') 
# items = soup.select('#root > div > div.css-1u9ias7-defaultStyle > div.bestProdMore > div > div > div')[0].select('div.unitItemBox mid cardType.css-1guxdwx-itemDisplayStyle') #이건 그 상품의 박스 하나임
for item in items:
        price = item.find('strong', attrs={'class': 'priceValue'}).get_text() #상품명 가져오기  
#         # tit = item.find('div', attrs={'class': 'srchProductUnitPriceArea'}).get_text() #행사 정보 가져오기
        # p2 = item.find('div', attrs={'class': 'srchProductInfoColumn'}).get_text() #행사 정보 가져오기
        
        # try:
        #     rev1 = item.find('span', attrs={'class': 'srchRatingScore'}).get_text() #행사 정보 가져오기
            
        # except:
            # rev1 = "리뷰 없음"
        
print(items) #프린트로 나타내기
        # sheet.append([price,tit,rev1])

# driver.close()#완료 후 닫기(안그러면 크롬 계속 열림)
# wb.save('롯데마트.xlsx') #파일명
# print('크롤링 완료') #완료 후 설정









