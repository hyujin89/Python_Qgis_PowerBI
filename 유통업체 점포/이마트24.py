import re
from bs4 import BeautifulSoup
from selenium import webdriver
import openpyxl
from selenium.webdriver.support import expected_conditions as EC

# 백그라운드로 웹브라우저 실행
options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome("./chromedriver", options = options)
driver.implicitly_wait(6)

# 이마트24 url 정보 설정
url = 'https://www.emart24.co.kr/introduce2/findBranch.asp'
driver.get(url)

# 해당 페이지 HTML 정보 추출
soup = BeautifulSoup(driver.page_source, 'html.parser')

# 페이지 전환 자바스크립트 설정
page_js = "javascript:goPage('{}');"   #boardViewController.getDataList(2)

# 전체 페이지 수 계산
page_count = int(re.findall(r'\d+', soup.select('a.bgNone')[-1]['href'])[0])

wb = openpyxl.Workbook()
sheet = wb.active
sheet.append(['점포명', '주소', '위도', '경도'])

# 전체 페이지 수만큼 반복
for page in range(1, page_count + 1):
    # 자바스크립트 실행
    driver.execute_script(page_js.format(page))

    # 해당 페이지 HTML 정보 추출
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # 매장 테이블 행정보 추출
    tr_list = soup.select('table > tbody > tr')
    for tr in tr_list:
        # 열정보 추출
        td_list = tr.select('td')

        # 매장명 추출
        shop_name = td_list[0].text.strip()

        # 매장주소 추출
        shop_addr = td_list[-1].select_one('p').text.split('|')[0].strip()

        # 매장좌표 추출
        p = td_list[-1].select_one('p.pull-right > a')['href']
        shop_coord = re.findall(r'\d+[.]\d+', p)

        # 위치좌표가 없는 매장
        if (len(shop_coord) != 2):
            shop_coord = ['0.0', '0.0']

        # 결과 저장
        sheet.append([shop_name, shop_addr, shop_coord[1], shop_coord[0]])

       

    print(f'{page}/{page_count} Completed!')

wb.save('이마트24.xlsx')
driver.close()
