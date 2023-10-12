
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import time
import openpyxl
from selenium import webdriver

driver = webdriver.Chrome("./chromedriver")
driver.get('http://www.ssg.com/service/bestMain.ssg')

i = 1

while True:

    print("Click : %d" % i)
    i += 1

    such = driver.find_element_by_class_name('best_item_more')
    such.click() #버튼 클릭
    driver.implicitly_wait(3)
    
    if i == 5:
        break

req = driver.page_source
soup = BeautifulSoup(req, 'html.parser')

wb = openpyxl.Workbook()
sheet = wb.active
sheet.append(["순위","회사","상품명","단축명","판매가","할인가","구매횟수/평점","비고"])


items = soup.select("#bestCategoryItem") #이건 그 상품의 박스 하나임

soup = BeautifulSoup(driver.page_source, 'html.parser')
    
items = soup.select('#bestCategoryItem')[0].select('li.cunit_t290') #이건 그 상품의 박스 하나임
for item in items:
        price = item.find('em', attrs={'class': 'ssg_price'}).get_text() #상품명 가져오기 
        rank = item.find('span', attrs={'class': 'tx_best'}).get_text() #상품가격 가져오기
        tit = item.find('em', attrs={'class': 'tx_ko'}).get_text() #행사 정보 가져오기
        p2 = item.find('div', attrs={'class': 'opt_price'}).get_text() #행사 정보 가져오기
        rev = item.find('div', attrs={'class': 'cunit_app'}).get_text() #행사 정보 가져오기
        title = item.find('div', attrs={'class': 'title'}).get_text() #행사 정보 가져오기
        title2 = item.find('em', attrs={'class': 'tx_en'}).get_text() #행사 정보 가져오기
        com = item.find('div', attrs={'class': 'cunit_tp'}).get_text() #행사 정보 가져오기
        # img = item.find('p', attrs={'class': 'img'}).get_text() #행사 이미지 : 이게 안됨
        print(price,tit,rank,p2,title,rev) #프린트로 나타내기
        sheet.append([rank+'위',com,title2,tit,price,p2,rev,title])

driver.close()#완료 후 닫기(안그러면 크롬 계속 열림)
wb.save('ssg best.xlsx') #파일명
print('크롤링 완료') #완료 후 설정









