# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

keyword = input("검색어 입력 : ")
#############################################
# 추가1

# daumnews.csv 파일을 쓰기(w) 모드로 열어줍니다.
f = open("All news.csv", "w") #워드클라우드 실행 시 txt, 뉴스 형태 .csv

# 데이터의 헤더 부분을 써줍니다.
f.write("일자,제목,요약,url\n")
#############################################

for n in range(1, 10): #페이지 수 선정
    raw = requests.get("https://search.daum.net/search?w=news&q="+keyword+"&p="+str(n))
    html = BeautifulSoup(raw.text, 'html.parser')

    articles = html.select("div.wrap_cont")

    for ar in articles:
        date = ar.select_one("span.cont_info").text
        title = ar.select_one("a.tit_main.fn_tit_u").text
        summary = ar.select_one("p.desc").text
        url = ar.a["href"]

        print(date)
        print(title)
        print(summary)
        print(url)
        # 기사별로 구분을 위해 구분선 삽입
        print("="*50)

        #############################################
        # 추가2

        # ,로 데이터가 구분되지 않도록 수집한 제목/기사요약에서 ,를 삭제해줍니다.
        date = date.replace(",", "")
        title = title.replace(",", "")
        summary = summary.replace(",", "")
        url = url.replace(",", "")
        

        # 수집한 제목/저자를 파일에 써줍니다.
        f.write(date + "," + title + "," + summary + "," + url + "\n")
        #############################################

#############################################
# 추가3

# naverebook.csv파일을 닫아줍니다.
f.close()
#############################################