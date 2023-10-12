import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoAlertPresentException, NoSuchElementException, TimeoutException, ElementNotInteractableException,NoSuchWindowException, NoSuchFrameException
import time
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import requests
import re
import csv

driver = webdriver.Chrome('./chromedriver') # Webdriver에서 네이버 페이지 접속 
driver.implicitly_wait(3)
#hrd = {'User-Agent':'Mozilla/5.0', 'referer':'http://naver.com'}
#네이버 검색
driver.get('https://news.naver.com/')#, headers=hrd)

search_box = driver.find_element_by_xpath('/html/body/section/header/div[1]/div/div/div[2]/div[3]/a/span').click() # 검색 창   //*[@id="u_hs"]/div/div/input   
search_box = driver.find_element_by_xpath('//*[@id="u_hs"]/div/div/input') # 검색 창   

search_box.send_keys("딜리셔스 페스티벌") #원하는 단어 
#driver.find_element_by_id('search_btn').click() #검색버튼 클릭
driver.find_element_by_xpath('//*[@id="u_hs"]/div/div/button[2]').click() #검색버튼 클릭
time.sleep(3)
#lnb > div.lnb_group > div > ul > li:nth-child(3)
#news_tab = driver.find_element_by_xpath('//*[@id="lnb"]/div[1]/div/ul/li[3]/a') #뉴스탭 클릭
#news_tab.send_keys(Keys.ENTER)
#time.sleep(3)

driver.switch_to.window(driver.window_handles[-1])

time.sleep(2)
option = driver.find_element_by_xpath('//*[@id="snb"]/div[1]/div/div[2]/a') #옵션 클릭
option.send_keys(Keys.ENTER)

date = driver.find_element_by_xpath('//*[@id="snb"]/div[2]/ul/li[2]/div/div[1]/a[9]') #날짜 직접입력 클릭  //*[@id="snb"]/div[2]/ul/li[3]/div/div[1]/a[9]
date.send_keys(Keys.ENTER)  
time.sleep(2)

year = driver.find_element_by_xpath('//*[@id="snb"]/div[2]/ul/li[2]/div/div[3]/div[2]/div[1]/div/div/div/ul/li[34]/a') #연도 직접입력 클릭
#//*[@id="snb"]/div[2]/ul/li[2]/div/div[3]/div[2]/div[1]/div/div/div/ul/li[29]/a #2018
#//*[@id="snb"]/div[2]/ul/li[2]/div/div[3]/div[2]/div[1]/div/div/div/ul/li[30]/a #2019
#//*[@id="snb"]/div[2]/ul/li[2]/div/div[3]/div[2]/div[1]/div/div/div/ul/li[31]/a #2020
#//*[@id="snb"]/div[2]/ul/li[2]/div/div[3]/div[2]/div[1]/div/div/div/ul/li[32]/a #2021

year.send_keys(Keys.ENTER)
time.sleep(1)
month = driver.find_element_by_xpath('//*[@id="snb"]/div[2]/ul/li[2]/div/div[3]/div[2]/div[2]/div/div/div/ul/li[2]/a') #날짜 직접입력 클릭
#//*[@id="snb"]/div[2]/ul/li[2]/div/div[3]/div[2]/div[2]/div/div/div/ul/li[4]/a #4월
#//*[@id="snb"]/div[2]/ul/li[2]/div/div[3]/div[2]/div[2]/div/div/div/ul/li[5]/a #5월
#//*[@id="snb"]/div[2]/ul/li[2]/div/div[3]/div[2]/div[2]/div/div/div/ul/li[6]/a #6월
month.send_keys(Keys.ENTER)
time.sleep(1)
day = driver.find_element_by_xpath('//*[@id="snb"]/div[2]/ul/li[2]/div/div[3]/div[2]/div[3]/div/div/div/ul/li[1]/a') #날짜 직접입력 클릭
#//*[@id="snb"]/div[2]/ul/li[2]/div/div[3]/div[2]/div[3]/div/div/div/ul/li[1]/a #1일
#//*[@id="snb"]/div[2]/ul/li[2]/div/div[3]/div[2]/div[3]/div/div/div/ul/li[2]/a #2일
#//*[@id="snb"]/div[2]/ul/li[2]/div/div[3]/div[2]/div[3]/div/div/div/ul/li[3]/a #3일
#//*[@id="snb"]/div[2]/ul/li[2]/div/div[3]/div[2]/div[3]/div/div/div/ul/li[6]/a #6일
day.send_keys(Keys.ENTER)
time.sleep(1)

date_to = driver.find_element_by_xpath('//*[@id="snb"]/div[2]/ul/li[2]/div/div[3]/div[1]/span[3]/a')
date_to.send_keys(Keys.ENTER)
time.sleep(3)                            

year = driver.find_element_by_xpath('//*[@id="snb"]/div[2]/ul/li[2]/div/div[3]/div[2]/div[1]/div/div/div/ul/li[34]/a') #연도 직접입력 클릭
#//*[@id="snb"]/div[2]/ul/li[2]/div/div[3]/div[2]/div[1]/div/div/div/ul/li[29]/a #2018
#//*[@id="snb"]/div[2]/ul/li[2]/div/div[3]/div[2]/div[1]/div/div/div/ul/li[30]/a #2019
#//*[@id="snb"]/div[2]/ul/li[2]/div/div[3]/div[2]/div[1]/div/div/div/ul/li[31]/a #2020
#//*[@id="snb"]/div[2]/ul/li[2]/div/div[3]/div[2]/div[1]/div/div/div/ul/li[32]/a #2021
year.send_keys(Keys.ENTER)
time.sleep(1)
month = driver.find_element_by_xpath('//*[@id="snb"]/div[2]/ul/li[2]/div/div[3]/div[2]/div[2]/div/div/div/ul/li[5]/a') #날짜 직접입력 클릭
#//*[@id="snb"]/div[2]/ul/li[2]/div/div[3]/div[2]/div[2]/div/div/div/ul/li[4]/a #4월
#//*[@id="snb"]/div[2]/ul/li[2]/div/div[3]/div[2]/div[2]/div/div/div/ul/li[5]/a #5월
#//*[@id="snb"]/div[2]/ul/li[2]/div/div[3]/div[2]/div[2]/div/div/div/ul/li[6]/a #6월
month.send_keys(Keys.ENTER)
time.sleep(1)
day = driver.find_element_by_xpath('//*[@id="snb"]/div[2]/ul/li[2]/div/div[3]/div[2]/div[3]/div/div/div/ul/li[31]/a') #날짜 직접입력 클릭
#//*[@id="snb"]/div[2]/ul/li[2]/div/div[3]/div[2]/div[3]/div/div/div/ul/li[1]/a #1일
#//*[@id="snb"]/div[2]/ul/li[2]/div/div[3]/div[2]/div[3]/div/div/div/ul/li[2]/a #2일
#//*[@id="snb"]/div[2]/ul/li[2]/div/div[3]/div[2]/div[3]/div/div/div/ul/li[3]/a #3일
#//*[@id="snb"]/div[2]/ul/li[2]/div/div[3]/div[2]/div[3]/div/div/div/ul/li[6]/a #6일
day.send_keys(Keys.ENTER)
time.sleep(1)
apply_date = driver.find_element_by_xpath('//*[@id="snb"]/div[2]/ul/li[2]/div/div[3]/div[3]/button') #적용 클릭
apply_date.send_keys(Keys.ENTER)
time.sleep(1)

sdata = []
news_list = []
results = []


file = open('wine.txt', 'a', encoding = 'utf-8')
file.write('date'+'|'+'title'+'\\n')#저장 값의 컬럼명\n",

for i in range(0,10000): #보고싶은 페이지 전체 수 
    req = driver.page_source
    soup = BeautifulSoup(req, 'html.parser')
    
    news_page = soup.select("#main_pack > section.sc_new.sp_nnews._prs_nws > div > div.group_news > ul") #뉴스페이지소스가져오기
        
    for news in news_page:
        for dates,titles, news_dscs in zip(news.find_all('span', attrs={'class': 'info'}), news.find_all('a', attrs={'class': 'news_tit'}), news.find_all('a', attrs={'class': 'api_txt_lines dsc_txt_wrap'})):
            date = dates.get_text() # 날짜 가져오기
            title = titles.get_text() # 제목 가져오기
            news_dsc = news_dscs.get_text() #내용요약 가져오기
            data = [date, title, news_dsc]
            results.append(data)
            file.write(date+ '|' + title +'\\n') #파일에 넣기
            news_list.append(date+ '|' + title + '\\n') 

    
    
    #for news in news_page:
    #    for dates in news.find_all('span', attrs={'class': 'info'}):
    #        date = dates.get_text()
    #    for titles in news.find_all('a', attrs={'class': 'news_tit'}):
    #        title = titles.get_text()
    #    file.write(date+ '|' + title +'\\n')
    #    review_list.append(date+ '|' + title + '\\n')
   # 
    print('파일저장종료:',i+1,'페이지')
    try:
        next_btn = driver.find_element_by_xpath('//*[@id="main_pack"]/div[2]/div/a[2]')
    except NoSuchElementException:
        break
    
    try:
        next_btn.send_keys(Keys.ENTER)
    except ElementNotInteractableException:
        print("ㅡ ElementNotInteractableException ㅡ")
        break

file.close()

driver.quit()
print('크롤링 종료')


# 결과를 데이터프레임으로 저장
import pandas as pd
result_df = pd.DataFrame(results)
result_df.columns = ['date','title','news_dsc']
result_df.to_csv('네이버 뉴스(신판).csv') 

print('크롤링 종료')
