# -*- coding: utf-8 -*-

import pandas as pd # 엑셀 불러오기
from sklearn.cluster import KMeans # kMeans model
import matplotlib.pyplot as plt # 그래프 만들기


sales = pd.read_csv("product_sales.csv") # 파일불러오기 , 독립변수를 추가해줄거면 열을 추가해서 하나씩 더 넣어줘야함
print(sales.info()) # 파일 내용 불러오기
'''
RangeIndex: 150 entries, 0 to 149
Data columns (total 4 columns):
tot_price      150 non-null float64 -> 총구매금액 
visit_count    150 non-null float64 -> 매장방문수 
buy_count      150 non-null float64 -> 구매횟수 
avg_price      150 non-null float64 -> 평균구매금액 
'''

sales.shape # (150, 4) # 세일 데이터 프레임 
type(sales) # DataFrame


# 단계1 : 3개 군집으로 군집화
model = KMeans(n_clusters=4, algorithm='auto') #full auto, 군집화 갯수 (그래서 몇개를 해줄건지를 설정하는 것임)
model.fit(sales)


# 단계2: 원형데이터에 군집 예측치 추가
# kMeans 예측치
pred = model.predict(sales)
pred 

sales['cluster'] = pred
sales.head()


# 단계3 : tot_price 변수와 가장 상관계수가 높은 변수로 산점도(색상 : 클러스터 결과)
sales.corr()
corr=sales.corr(method='pearson')
print(corr)
''' 피어슨
             tot_price  visit_count  buy_count  avg_price   cluster
tot_price     1.000000     0.817954  -0.013051   0.871754  0.349480
'''

plt.scatter(x=sales['avg_price'], y=sales['tot_price'], c=sales['cluster'])  #상관계수가 높은것으로 바꿔줘야함 x를(avg, visit 등등 ), ""

# 단계4 : 산점도에 군집의 중심점 시각화
centers = model.cluster_centers_
centers


# 총구매금액 vs 평균구매금액 (상관계수가 가장 높은것을 설정해줘야함 )
plt.scatter(x=centers[:,3], y=centers[:,0], c='red', label='Inline label', alpha=1, s=20, cmap='viridis', marker='*') #s는 중심점
plt.title('Store', fontsize=14) #그래프 맨 위에 제목이라고 보면됨
plt.xlabel('avg_price', fontsize=12) #독립변수가 되는데 상관계수가 높은걸로 바꿔줘하니, 이건 (변동값) x축에 이름을 바꿔주는 것임
plt.ylabel('tot_price', fontsize=12) #종속변수가 될것이고 (고정값)
plt.show()

#피어슨의 상관계수는 tot price와 관계가 가장 높은 것을 설정하는 것 그리고 결과값이 나오면 X를 무엇을 넣어줄지 설정해야함
