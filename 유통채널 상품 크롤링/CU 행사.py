import re
import time #sleep 타임 걸어주기 (안그럼 페이지 이동후 html을 못읽음)
from bs4 import BeautifulSoup #html 코드 가져오기 
from selenium import webdriver #셀레니움으로 반복 (페이지)
import openpyxl #엑셀로 저장하기 
from selenium.common.exceptions import NoSuchElementException


# 크롬 옵션 설정, 브라우저를 띄우지 않고 백그라운드로 처리
options = webdriver.ChromeOptions() #웹드라이버 크롬
options.add_argument('--headless') # 이건 이해 안되는데 끌어옴
driver = webdriver.Chrome("./chromedriver", options = options) #옵션으로 크롬 드라이버 실행

# 주어진 url을 이용하여 웹 정보 크롤링
url = 'http://cu.bgfretail.com/event/plus.do?category=event&depth2=1&sf=N' # 글어올 사이트
driver.get(url) # url 담기 (다음에 이해안되면 나도코딩 보기)


i = 1

while True:

    print("Click : %d" % i)
    i += 1

    driver.execute_script('javascript:nextPage(1)')
    driver.implicitly_wait(3)

    finished = True

    try:
        driver.find_element_by_id('nothing')
    except NoSuchElementException:
        finished = False

    if finished:
        break


req = driver.page_source
soup = BeautifulSoup(req, 'html.parser')

wb = openpyxl.Workbook()
sheet = wb.active
sheet.append(["점포명", "주소", "전화번호", "비고"])


items = soup.select("#contents > div.relCon > div.prodListWrap > ul > li") #이건 그 상품의 박스 하나임
   
for item in items:
    tit = item.find('p', attrs={'class': 'prodName'}).get_text() #상품명 가져오기 
    price = item.find('p', attrs={'class': 'prodPrice'}).get_text() #상품가격 가져오기
    
    ###########################################################
    flg = item.find('ul:nth-child > li:nth-child', attrs={'class':'ul > li'}) #행사 정보 가져오기
    ############################################################## 여기를 못가져옴
    print(tit, price, flg) #프린트로 나타내기

    sheet.append([tit, price, flg])

items2 = soup.select("#contents > div.relCon > div.prodListWrap > ul > li > ul") #이건 그 상품의 박스 하나임

for item in items2:
    ##############################################################
    event = item.find('li').get_text() #행사 정보 가져오기
    ############################################################## 여기를 못가져옴
    print(event) #프린트로 나타내기
#    sheet2.append([flg])
    sheet.append([event])

wb.save("cu.xlsx")
    
