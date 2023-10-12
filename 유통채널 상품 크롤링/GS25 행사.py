import re
import time #sleep 타임 걸어주기 (안그럼 페이지 이동후 html을 못읽음)
from bs4 import BeautifulSoup #html 코드 가져오기 
from selenium import webdriver #셀레니움으로 반복 (페이지)
import openpyxl #엑셀로 저장하기 

# 크롬 옵션 설정, 브라우저를 띄우지 않고 백그라운드로 처리
options = webdriver.ChromeOptions() #웹드라이버 크롬
# options.add_argument('--headless') # 이건 이해 안되는데 끌어옴
driver = webdriver.Chrome("./chromedriver", options = options) #옵션으로 크롬 드라이버 실행

# 주어진 url을 이용하여 웹 정보 크롤링
url = 'http://gs25.gsretail.com/gscvs/ko/products/event-goods#;' # 글어올 사이트
driver.get(url) # url 담기 (다음에 이해안되면 나도코딩 보기)

# 전체 탭 클릭
search_button = driver.find_element_by_css_selector('a#TOTAL') #전체 버튼 클릭 후 1+1, 2+1 등 전체보기 클릭
search_button.click() #버튼 클릭
time.sleep(2) # 슬립 2~3초정도 주기 그래야지 안그러면 안넘어감 / 나중에 딴거 만들때도 슬립을 1~5초는 꼭 주기

# 현재 웹 페이지 정보 추출
soup = BeautifulSoup(driver.page_source, 'html.parser') #소스 html에 담기

# 전체 페이지 수 추출 #
total_pages = int(re.findall(r'\d+', soup.select_one('a.next2')['onclick'])[0]) #이거 어려움 페이지가 반으로 나눠져 있어서 next로 넘겨줘야함 원랜 url에 페이번호가 있어 그것만 넘겨주면 됨


wb = openpyxl.Workbook() # 저장할 엑셀 시트 열기
sheet = wb.active #시트 활성화
sheet.append(["상품명", "가격", "행사내용"]) # 시트 맨위에 고정으로 박아두기
# # 페이지 수만큼 반복
for p in range(total_pages):
    # 현재 페이지 정보 추출
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    time.sleep(2)
    # 한 페이지 내에 있는 상품 정보 리스트(최대 8개) 추출 최대 8개 밖에 없음
    items = soup.select('ul.prod_list')[0].select('div.prod_box') #이건 그 상품의 박스 하나임
    # 상품 리스트의 제목, 가격, 추가 정보 추출 및 엑셀에 저장
    for item in items:
        tit = item.find('p', attrs={'class': 'tit'}).get_text() #상품명 가져오기 
        price = item.find('p', attrs={'class': 'price'}).get_text() #상품가격 가져오기
        flg = item.find('div', attrs={'class': 'flag_box'}).get_text() #행사 정보 가져오기
        img = item.find('p', attrs={'class': 'img'}).get_text() #행사 이미지 : 이게 안됨
        print(tit, price, flg, img) #프린트로 나타내기

        sheet.append([tit, price, flg, img]) #시트에다가 차례로 박기

    # 다음(Next) 버튼을 클릭하여 다음 페이지로 이동     
    next_button = driver.find_element_by_css_selector('#contents > div.cnt > div.cnt_section.mt50 > div > div > div:nth-child(9) > div > a.next') #넥스트 버튼인데 xpath에서 selec 아니면 ful가져오기
    next_button.click()
    time.sleep(2) #넥스트 버튼으로 이동(슬립 2~3초)

# 크롬 드라이버 종료 및 결과(엑셀) 저장
driver.close()#완료 후 닫기(안그러면 크롬 계속 열림)
wb.save('gs25행사.xlsx') #파일명
print('크롤링 완료') #완료 후 설정


