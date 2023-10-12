import time
import re
import openpyxl
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
# import chromedriver_autoinstaller

# 크롬 드라이버 자동 설치
# chromedriver_autoinstaller.install()

# 세븐일레븐 웹 페이지 오픈
options = webdriver.ChromeOptions()
# options.add_argument('--headless')
driver = webdriver.Chrome("./chromedriver", options = options)
# driver = webdriver.Chrome(options = options)
driver.get('https://www.7-eleven.co.kr/')  #http://gs25.gsretail.com/gscvs/ko/store-services/locations
driver.implicitly_wait(15)





# 점포찾기 클릭
driver.find_element_by_xpath('//*[@id="header"]/div/div/div[1]/a[1]').click()
time.sleep(5)

# 시도 목록 추출
storeLaySido = driver.find_element_by_id('storeLaySido')
sido_list = [x.get_attribute('value') for x in storeLaySido.find_elements_by_tag_name('option')][1:]
time.sleep(2)

# 엑셀 설정
wb = openpyxl.Workbook()
sheet = wb.active
sheet.append(['점포명', '주소', '위도', '경도'])

for sido in sido_list:
    # 시도 셀렉션 바 추출 및 값 설정
    select_storeLaySido = Select(driver.find_element_by_id('storeLaySido'))
    select_storeLaySido.select_by_visible_text(sido)
    time.sleep(1.5)
    

    # 시군구 목록 추출
    storeLayGu = driver.find_element_by_id('storeLayGu')
    gu_list = [x.get_attribute('value') for x in storeLayGu.find_elements_by_tag_name('option')][1:]
    time.sleep(1.5)

    for gu in gu_list:
        # 시군구 셀렉션 바 추출 및 값 설정
        select_storeLayGu = Select(driver.find_element_by_id('storeLayGu'))
        select_storeLayGu.select_by_visible_text(gu)
        time.sleep(1.5)

        # 확인 버튼 클릭
        
        
        try:  
            storeButton1 = driver.find_element_by_id('storeButton1')
            storeButton1.click()
            time.sleep(3)
            driver.switch_to.alert.accept()  #이건 그 오류 메시지 나오면 취소누르는거 알겠지?
            storeButton1 = driver.find_element_by_id('storeButton1')
            storeButton1.click()
            time.sleep(3)

        except:

            print("에러없음")


        
        # 해당 페이지 HTML 정보 추출
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # 점포명,주소,위도/경도
        for li in soup.select('div.list_stroe li'):
            store_name = ''
            address = ''
            lat = 0.0
            lon = 0.0

            # 위경도 태그 추출
            a_tag = li.select_one('a')
            if (not a_tag): # 검색 결과가 없는 경우
                continue

            # 점포명, 주소 태그 추출
            span_tag = a_tag.select('span')
            if (len(span_tag) >= 2):
                store_name = span_tag[0].text.strip()
                address = span_tag[1].text.replace('\xa0', ' ').strip()

            # href 주소에서 위경도 추출
            lat_lon = re.findall(r'\((.*?)\)', a_tag['href'])
            if (lat_lon):
                lat, lon = map(float, lat_lon[-1].split(',')[1:])

            # 결과 저장
            sheet.append([store_name, address, lat, lon])
        
        print(f'{sido}-{gu} Completed!')

wb.save('세븐일레븐11.xlsx')
driver.quit() # driver process shut down

print('System Completed!!!')



