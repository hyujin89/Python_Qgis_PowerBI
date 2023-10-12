from enum import Flag
import re
import time #sleep 타임 걸어주기 (안그럼 페이지 이동후 html을 못읽음)
from bs4 import BeautifulSoup #html 코드 가져오기 
from selenium import webdriver #셀레니움으로 반복 (페이지)
import openpyxl #엑셀로 저장하기 
from selenium.webdriver.support import expected_conditions as EC

# 크롬 옵션 설정, 브라우저를 띄우지 않고 백그라운드로 처리
options = webdriver.ChromeOptions() #웹드라이버 크롬
# options.add_argument('--headless') # 이건 이해 안되는데 끌어옴
driver = webdriver.Chrome("./chromedriver", options = options) #옵션으로 크롬 드라이버 실행
driver.implicitly_wait(6)
# 주어진 url을 이용하여 웹 정보 크롤링

url = 'http://gs25.gsretail.com/gscvs/ko/store-services/locations' # 글어올 사이트
# headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"}

driver.get(url) # url 담기 (다음에 이해안되면 나도코딩 보기)

soup = BeautifulSoup(driver.page_source, 'html.parser') #소스 html에 담기
page_js = "boardViewController.getDataList('{}');"

# 전체 페이지 수 계산
page_count = int(re.findall(r'\d+', soup.select('a.prev2')[-1]['href'])[0])

wb = openpyxl.Workbook() # 저장할 엑셀 시트 열기
sheet = wb.active #시트 활성화
sheet.append(["점포명", "주소", "제공서비스"]) # 시트 맨위에 고정으로 박아두기
# # 페이지 수만큼 반복
for page in range(1, 3286): #Gs 마지막 페이지 수 P.2969 / 마지막 페이지보다 항상 +2정도 더 큰 수를 입력
    # 현재 페이지 정보 추출
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    # time.sleep(1)
    
    items = soup.select('#storeInfoList > tr') #이건 그 상품의 박스 하나임 
    
    for item in items:
        tit = item.find('a', attrs={'class': 'st_name'}).get_text() #상품명 가져오기 
        # time.sleep(1)
        price = item.find('a', attrs={'class': 'st_address'}).get_text() #상품가격 가져오기
        # time.sleep(1)
        # flg = item.find('div', attrs={'class': 'stsch_icon'}).get_text() #행사 정보 가져오기
        # img = item.find('p', attrs={'class': 'img'}).get_text() #행사 이미지 : 이게 안됨
        # print(tit, price, flg, img) #프린트로 나타내기
        # print(tit,price)
        sheet.append([tit,price]) #시트에다가 차례로 박기
        # time.sleep(1)
        driver.implicitly_wait(1)
        # time.sleep(1)
        
    next_button = driver.find_element_by_css_selector('#pagingTagBox > a.next') #넥스트 버튼인데 xpath에서 selec 아니면 ful가져오기
    next_button.click()
    time.sleep(2)
   
    print(f'{page}/{page_count} Completed!')


driver.quit()
wb.save('GS255.xlsx') 
print('크롤링 완료') 


