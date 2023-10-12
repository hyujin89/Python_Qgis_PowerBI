
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import time
import openpyxl
from selenium import webdriver

options = webdriver.ChromeOptions() #웹드라이버 크롬
options.add_argument('--headless') # 이건 이해 안되는데 끌어옴
driver = webdriver.Chrome("./chromedriver", options = options) #옵션으로 크롬 드라이버 실행

# 주어진 url을 이용하여 웹 정보 크롤링
url = 'https://www.kurly.com/shop/goods/goods_list.php?category=029#main' # 글어올 사이트


headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"}


driver.get(url)

req = driver.page_source
soup = BeautifulSoup(req, 'html.parser')

wb = openpyxl.Workbook()
sheet = wb.active
sheet.append(["순위","상품명","가격","할인","설명","배송"])

items = soup.select("#goodsList > div.list_goods > div > ul") #이건 그 상품의 박스 하나임
soup = BeautifulSoup(driver.page_source, 'html.parser')
items = soup.select('#goodsList > div.list_goods > div > ul')[0].select('div.item') #이건 그 상품의 박스 하나임


for n in range(1, 2):  # 끌어올 페이지 수 설정
    time.sleep(1)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    for item in items:
            price = item.find('span', attrs={'class': 'price'}).get_text() #상품명 가져오기 
            tit = item.find('span', attrs={'class': 'name'}).get_text() #행사 정보 가져오기
            p2 = item.find('span', attrs={'class': 'desc'}).get_text() #행사 정보 가져오기
                
            try:
                rev1 = item.find('span', attrs={'class': 'ico limit tag_type2'}).get_text() #행사 정보 가져오기
                    
            except:
                rev1 = "컬리 낫 온리"

            try:
                rev2 = item.find('span', attrs={'class': 'original'}).get_text() #행사 정보 가져오기
                    
            except:
                rev2 = "할인없음"
                
                
            print(price,rev2,tit,p2,rev1) #프린트로 나타내기
            sheet.append([str(1)+"위",tit,price,rev2,p2,rev1])
    

    next_button = driver.find_element_by_xpath('//*[@id="goodsList"]/div[3]/div/a[3]').click()
    
    time.sleep(2)
    
    

driver.close()#완료 후 닫기(안그러면 크롬 계속 열림)
wb.save('마켓컬리.xlsx') #파일명
print('크롤링 완료') #완료 후 설정









