import selenium
from selenium import webdriver
from selenium.webdriver.common import keys
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoAlertPresentException, NoSuchElementException, TimeoutException, ElementNotInteractableException,NoSuchWindowException, NoSuchFrameException
import time
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import requests
import re
import csv
import os
import zipfile
import random
import collections
import itertools


driver = webdriver.Chrome('./chromedriver') # Webdriver에서 네이버 페이지 접속 
driver.implicitly_wait(3)
#hrd = {'User-Agent':'Mozilla/5.0', 'referer':'http://naver.com'}
#네이버 검색
driver.get('https://www.naver.com/')#, headers=hrd)

search_box = driver.find_element_by_xpath('//*[@id="query"]') # 검색 창 
search_box.send_keys("내돈내산 cu") #원하는 단어 
driver.find_element_by_xpath('//*[@id="search_btn"]').click() #검색버튼 클릭
time.sleep(1)

driver.find_element_by_xpath('//*[@id="lnb"]/div[1]/div/ul/li[2]/a').click() #블로그 클릭
time.sleep(1)

driver.switch_to.window(driver.window_handles[-1])

time.sleep(1)
option = driver.find_element_by_xpath('//*[@id="snb"]/div[1]/div/div[3]/a') #옵션 클릭  //*[@id="snb"]/div[1]/div/div[3]/a   
option.send_keys(Keys.ENTER)

date = driver.find_element_by_xpath('//*[@id="snb"]/div[2]/ul/li[3]/div/div[1]/a[9]') #날짜 직접입력 클릭
date.send_keys(Keys.ENTER)  
time.sleep(1)



################################ 전 설정 ##############################

year = driver.find_element_by_xpath('//*[@id="snb"]/div[2]/ul/li[3]/div/div[2]/div[2]/div[1]/div/div/div/ul/li[32]/a') #연도 직접입력 클릭 # 연도는 xpath를 설정해야함
year.send_keys(Keys.ENTER)
time.sleep(1)

month = driver.find_element_by_xpath('//*[@id="snb"]/div[2]/ul/li[3]/div/div[2]/div[2]/div[2]/div/div/div/ul/li[11]/a') #날짜 직접입력 클릭  [8]만 바꿔주면 됨
month.send_keys(Keys.ENTER)
time.sleep(1)

day = driver.find_element_by_xpath('//*[@id="snb"]/div[2]/ul/li[3]/div/div[2]/div[2]/div[3]/div/div/div/ul/li[1]/a') #날짜 직접입력 클릭   [22]만 바꿔주면 됨
day.send_keys(Keys.ENTER)
time.sleep(1)

################################ 전 설정 ##############################




################################ 적용 설정 ##############################
date_to = driver.find_element_by_xpath('//*[@id="snb"]/div[2]/ul/li[3]/div/div[2]/div[1]/span[3]/a')
date_to.send_keys(Keys.ENTER)
time.sleep(1)                            
################################ 적용 설정 ##############################




################################ 후 설정 ##############################

year = driver.find_element_by_xpath('//*[@id="snb"]/div[2]/ul/li[3]/div/div[2]/div[2]/div[1]/div/div/div/ul/li[32]/a') #연도 직접입력 클릭
year.send_keys(Keys.ENTER)
time.sleep(1)

month = driver.find_element_by_xpath('//*[@id="snb"]/div[2]/ul/li[3]/div/div[2]/div[2]/div[2]/div/div/div/ul/li[11]/a') #날짜 직접입력 클릭
month.send_keys(Keys.ENTER)
time.sleep(1)

day = driver.find_element_by_xpath('//*[@id="snb"]/div[2]/ul/li[3]/div/div[2]/div[2]/div[3]/div/div/div/ul/li[22]/a') #날짜 직접입력 클릭
day.send_keys(Keys.ENTER)
time.sleep(1)

################################ 후 설정 ##############################





apply_date = driver.find_element_by_xpath('//*[@id="snb"]/div[2]/ul/li[3]/div/div[2]/div[3]/button') #적용 클릭
apply_date.send_keys(Keys.ENTER)
time.sleep(1)

sdata = []
news_list = []
results = []


file = open('wine.txt', 'a', encoding = 'utf-8')
file.write('date'+'|'+'title'+'\\n')#저장 값의 컬럼명\n",

last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    # Scroll down
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # page loading를 위한 대기 시간
    time.sleep(random.uniform(2,3)) # Feed를 불러올 수 있도록 램덤 대기
    # 기존 height하고 변화가 발생하지 않을시 break
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

time.sleep(1)

req = driver.page_source
soup = BeautifulSoup(req, 'html.parser')
        
news_page = soup.select("#main_pack > section > div > div._list > panel-list > div > more-contents > div > ul") #뉴스페이지소스가져오기 

time.sleep(1)

for news in news_page:
            for dates, titles, news_dscs, news_tag in zip(news.find_all('span', attrs={'class': 'sub_time sub_txt'}), news.find_all('a', attrs={'class': 'api_txt_lines total_tit _cross_trigger'}), news.find_all('div', attrs={'class': 'api_txt_lines dsc_txt'}), news.find_all('div', attrs={'class': 'total_tag_area'})):
                date = dates.get_text() # 날짜 가져오기
                title = titles.get_text() # 제목 가져오기
                news_dsc = news_dscs.get_text() #내용요약 가져오기
                news_tag = news_tag.get_text() #내용요약 가져오기
                data = [date, title, news_dsc, news_tag]
                results.append(data)
                file.write(date+ '|' + title +'\\n') #파일에 넣기
                news_list.append(date+ '|' + title + '\\n') 

    

driver.quit()
print('파일저장종료:','블로그 페이지')

file.close()

# 결과를 데이터프레임으로 저장
import pandas as pd
result_df = pd.DataFrame(results)
result_df.columns = ['date','title','news_dsc', 'news_tag']
result_df.to_csv('네이버블로그.csv') 

df = pd.read_csv('네이버블로그.csv')
kw_dict = collections.Counter(itertools.chain.from_iterable(k.split(" ") for k in df['news_tag']))
print(kw_dict)






from os import remove
from types import CodeType
from konlpy.tag import Hannanum
from collections import Counter
from matplotlib.colors import Colormap
from wordcloud import WordCloud
from wordcloud import STOPWORDS
from matplotlib import pyplot as plt
from numpy import number
from PIL import Image
from wordcloud import WordCloud
import numpy as np
# 모듈 호출
import pandas as pd
from PIL import Image
import wordcloud
from wordcloud.wordcloud import FONT_PATH


# 텍스트 파일 열기
text = open('네이버블로그.csv','r',encoding='UTF8').read() # numbers에서 csv파일로 저장하면 됨, 내용이나, 불필요한 글자는 지우는것도 좋음
stopwords = set(STOPWORDS)


# 한글 형태소 분석하기
engin = Hannanum()
nouns = engin.nouns(text)
nouns = [n for n in nouns if len(n) > 1] # 1자리 단어보다 큰것을 카운팅
stopwords = set(STOPWORDS) #스탑워드 별로 필요 없음 


# 단어 숫자 세기 
count = Counter(nouns)
tags = count.most_common(100) #표시할 단어 수 

remove = '이마트24','점포','전국','편의점','상품','이마트','신세계','GS25','운영','업계','ㅁ최초','베트남','브랜드','구입','판매','구매','제공','세븐일레븐','cu','BGF리테','BGF리테일','bgf리테일','gs리테일','롯데','파이낸셜 뉴스','다날','2명','흉기','한국','메릴랜드주','불안','0시','뉴스투데이','미국','뉴스터치','시장','편의점서','성숙기','GS리테일','가맹점주','매출','서비스','롯데하이마트','세븐일레븐','홈케','출시,세븐일레븐','출시','자립','경영','지원','파이낸셜뉴스','미니스톱','본사','심관섭)','한국미니스톱','회장','(서울=뉴스1)','대표이사','사진','강성규','왼쪽','7.','심관섭','가맹점','김정미','CU','홈술상','기','말레이시아','1호점','1일','것','등','코로나19','코로나바이러스','수','[아시아경제','임춘한','/BGF리테일','22일','20일','모바','달','국내','중구','서울','오전','직원','고객','무','필요','경영주','업무','진행','활성화','영업','발주','매출활성화','행사','집중','강화','방향','생각','경우','점포별','캐릭터','실리콘','마케팅','함지현','1824','몽골','출입','기내식','제주항공','이벤트','할','드','GS리테','29일','#gs25','#GS25','#내돈내산','#gs25편의점','#GS25편의점','#편의점','# gs25','# GS25',',,,,#이마트24','#이마트24','#이마트24와','#편의점와',',,,,#이마트24와','#이마트','#이마트편의점',',,,,#이마트','#이마트24편의점','#이마트트레이더스',',,,,#내돈내산','#네이버페',',,,,#네이버페','#네이버','#이마트24편의점창업비용','내돈내산','맥주추천','편스토랑','내돈내산','#'
nouns = [n for n in nouns if n not in remove]

count = Counter(nouns)
tags = count.most_common(100) # 처음 카운팅을 하고 다시 제거할 단어를 선정하여 재카운팅함       


# 워드 클라우드 이미지 생성하기
mask = np.array(Image.open('ddc.jpeg'))
wordcloud = WordCloud(font_path='YNJ.otf',  #글꼴 (배달민족, 야놀자 abs.ttf)
                      stopwords=STOPWORDS,
                      mask=mask,
                      background_color='white', #white
                      max_words=1000, #최대 단어 표시
                      relative_scaling = 0.1, # 글자들의 상대적 크기
                      width=1500, 
                      height=1000).generate_from_frequencies(dict(tags))
                      

# 화면에 출력하기
fig = plt.figure(figsize=(10,10)) # 최종 출력몰 크기, width, heigt크기가 커야 최종 출력몰의 크기가 깨지지 않음
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off') # 그래프 주변 가로.세로 크기 숫자표시


# SVG 객체로 이미지 저장하기
plt.savefig('skycloud plt.png')
plt.show()

