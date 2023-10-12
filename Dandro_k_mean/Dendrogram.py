#이건 가장 비슷한 점포들을 묶는 거임 클러스터링 하는거라고 보면 됨
#Total, smoke, FF매출, 객수, 구매, 폐기 등 이런 변수들을 열에다가 쭉 넣고 각 점포당 묶어바 했을때 비슷한것끼리 묶이는 것임

import numpy as np  # 
import pandas as pd # 
import matplotlib.pyplot as plt # 
from sklearn.preprocessing import StandardScaler # 
from sklearn.cluster import AgglomerativeClustering


utilities_df = pd.read_csv('dendrogram0.csv', encoding='utf8') #파일 열기 
utilities_df.head()
utilities_df.shape
utilities_df.keys()


######################################## 한글깨짐 처리
import matplotlib.pyplot as plt
from matplotlib import rc
import seaborn as sns

rc('font', family='AppleGothic')
plt.rcParams['axes.unicode_minus'] = False #이걸로 해야 한글이 안깨임
############################################


columns = ['total Sale','smoke','human','FF','purchase','disposal'] #열 : 영어로 표시 어떤것들을 할것인지 분석 total은 종속변수임
columns #열을 추가하고 싶으면 여기다가 쭉 써줘야해, 이것말고도 더 있겟지? 그러니까 추가하고 싶음 파일도 넣고 여기도 써주고

#숫자에 쉼표를 넣으면 안됨, 일반으로 표시해야함

labels = np.array(utilities_df['Company']) #컴페니는 점포명임 
labels

utilities_df = utilities_df.drop(['Company'], axis=1)
utilities_df

stdsc = StandardScaler()
utilities_df = pd.DataFrame(stdsc.fit_transform(utilities_df))

utilities_df.index = labels
utilities_df.columns = columns
utilities_df


from scipy.spatial.distance import pdist, squareform
row_dist = pd.DataFrame(squareform(pdist(utilities_df, metric='euclidean')),columns=labels,index=labels)
row_dist


from scipy.cluster.hierarchy import linkage
row_clusters = linkage(utilities_df.values, method='complete', metric='euclidean')  #complete, singe, average(이것을 설정해서 가까운, 중간, 먼것으로 판단 :블로그 참고)
pd.DataFrame(row_clusters, columns=['row label 1', 'row label 2','거리', '클러스터 샘플 갯수.'], index=['cluster %d' % (i + 1)
                    for i in range(row_clusters.shape[0])])

from scipy.cluster.hierarchy import dendrogram
dendr = dendrogram(row_clusters,labels=labels)
ac = AgglomerativeClustering(n_clusters=10, affinity='euclidean', linkage='ward') #클러스터 갯수를 설정하는 것인데 잘 안됨
labels = ac.fit_predict(utilities_df)

plt.title('Emart24 Store', fontsize=14) #그래프 맨 위에 제목이라고 보면됨
plt.xlabel('점포명', fontsize=12) #독립변수가 되는데 상관계수가 높은걸로 바꿔줘하니, 이건 (변동값) x축에 이름을 바꿔주는 것임
plt.ylabel('클러스터링', fontsize=12) #종속변수가 될것이고 (고정값)
plt.tight_layout()
plt.show()


print('클러스터 레이블: %s' % labels) #클러스터가 0~10까지 등 표시됨 

