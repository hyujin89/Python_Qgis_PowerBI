from os import remove
from types import CodeType
from konlpy.tag import Hannanum
from collections import Counter
from wordcloud import WordCloud
from wordcloud import STOPWORDS
from matplotlib import pyplot as plt
from numpy import number
from PIL import Image
from wordcloud import WordCloud
import numpy as np
# 모듈 호출
import pandas as pd
# import seaborn as sns
# conda install seaborn=0.11.0 


# 텍스트 파일 열기
text = open('title news.csv','r',encoding='UTF8').read() # numbers에서 csv파일로 저장하면 됨, 내용이나, 불필요한 글자는 지우는것도 좋음
stopwords = set(STOPWORDS)


# 한글 형태소 분석하기
engin = Hannanum()
nouns = engin.nouns(text)
nouns = [n for n in nouns if len(n) > 1] # 1자리 단어보다 큰것을 카운팅
stopwords = set(STOPWORDS) #스탑워드 별로 필요 없음 


# 단어 숫자 세기 
count = Counter(nouns)
tags = count.most_common(100) #표시할 단어 수 

remove = '이마트24','점포','전국','편의점','상품','이마트','신세계','GS25','운영','업계','ㅁ최초','베트남','브랜드','구입','판매','구매','제공','세븐일레븐','cu','BGF리테','BGF리테일','bgf리테일','gs리테일','롯데','파이낸셜 뉴스','다날','2명','흉기','한국','메릴랜드주','불안','0시','뉴스투데이','미국','뉴스터치','시장','편의점서','성숙기','GS리테일','가맹점주','매출','서비스','롯데하이마트','세븐일레븐','홈케','출시,세븐일레븐','출시','자립','경영','지원','파이낸셜뉴스','미니스톱','본사','심관섭)','한국미니스톱','회장','(서울=뉴스1)','대표이사','사진','강성규','왼쪽','7.','심관섭','가맹점','김정미','CU','홈술상','기','말레이시아','1호점','1일','것','등','코로나19','코로나바이러스','수','[아시아경제','임춘한','/BGF리테일','22일','20일','모바','달','국내','중구','서울','오전','직원','고객','무','필요','경영주','업무','진행','활성화','영업','발주','매출활성화','행사','집중','강화','방향','생각','경우','점포별','캐릭터','실리콘','마케팅','함지현','1824','몽골','출입','기내식','제주항공','이벤트','할','드','GS리테','29일','#gs25','#GS25','#내돈내산','#gs25편의점','#GS25편의점','#편의점','# gs25','# GS25',',,,,#이마트24','#이마트24','#이마트24와','#편의점와',',,,,#이마트24와','#이마트','#이마트편의점',',,,,#이마트','#이마트24편의점','#이마트트레이더스',',,,,#내돈내산','#네이버페',',,,,#네이버페','#네이버','#이마트24편의점창업비용','내돈내산','맥주추천','편스토랑'
nouns = [n for n in nouns if n not in remove]

count = Counter(nouns)
tags = count.most_common(100) # 처음 카운팅을 하고 다시 제거할 단어를 선정하여 재카운팅함       


# 워드 클라우드 이미지 생성하기
wordcloud = WordCloud(font_path='YNJ.otf',  #글꼴 (배달민족, 야놀자 abs.ttf)
                      stopwords=STOPWORDS,
                      background_color='white', #white
                      max_words=1000, #최대 단어 표시
                      relative_scaling = 0.2, # 글자들의 상대적 크기
                      width=1500, 
                      height=1000).generate_from_frequencies(dict(tags))
                      

# 화면에 출력하기
fig = plt.figure(figsize=(10,10)) # 최종 출력몰 크기, width, heigt크기가 커야 최종 출력몰의 크기가 깨지지 않음
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off') # 그래프 주변 가로.세로 크기 숫자표시


# SVG 객체로 이미지 저장하기
plt.savefig('skycloud plt.png')
plt.show()



# plt.plot(text['tags'], text['count'])
# plt.show()


# plt.bar(['count','a','c'], height=[1,2,3,5,6], color='red')
# plt.show()


# # plt.plot(range(1, 10), count, marker='o')
