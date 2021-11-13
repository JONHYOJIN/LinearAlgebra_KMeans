import pandas as pd
import numpy as np
import random

class KmeansRun:
    def __init__(self, data, clusters, max_iter=20):
        self.data = data            # KMeans를 수행하는 데이터
        self.clusters = clusters    # 구분할 cluster의 수
        self.max_iter = max_iter    # 최대 반복 횟수 (20으로 고정)
    def run_kmeans(self):           # KMeans 실행 함수
        print("Start KMeans Clustering...")
        jclust_values = []              # iteration별 각 군집의 j-clust값의 합
        cpoints = self.get_rdpoints()   # 각 군집의 중심점 좌표 리스트
        print("Random Process Complete!\n")
        for iter in range(self.max_iter):
            p_cpoints = cpoints         # 이전 중심점 좌표 리스트 저장
            print("{}th iteration start".format(iter+1))
            self.classify_cluster(cpoints)  # cpoint 기반으로 ['cluster']에 cluster 분류값 입력
            cpoints = self.set_center()     # cluster값 기반으로 중심점 재설정
            jclust = self.get_jclust(cpoints)   # 재설정된 중심점 기반으로 jclust값 계산
            jclust_values.append(jclust)        # 각 군집의 j-clust값의 합을 jclust_values 리스트에 저장
            print("{}th iteration's jclust value: {}".format(iter+1, jclust))
            if cpoints == p_cpoints:        # 중심점의 이동이 없으면 클러스터링 종료
                print("\nIteration Complete!\n")
                break
        # 각 군집의 중심점과 가장 가까운 5개의 document를 데이터 프레임으로 반환
        n5_data, n5_index = self.get_nearest5(cpoints)  
        nearest_5 = pd.DataFrame(n5_data, columns = ['1st','2nd','3rd','4th','5th'], index=n5_index)
        # 반환할 데이터 프레임에 각 군집의 중심점 좌표를 row로 추가(할당된 document가 없는 군집은 제외)
        for i in self.data['cluster'].value_counts().index:
            cpoints[int(i)].append(int(i))
            name = "cluster "+str(int(i))
            df = pd.Series(cpoints[int(i)], index=self.data.columns)
            self.data.loc[name] = df
        # 군집화 완료된 데이터 프레임, j-clust값, 가까운 5개의 document에 대한 데이터 프레임 반환
        return self.data, jclust_values, nearest_5
    def get_rdpoints(self): # 초기 랜덤 중심점 설정
        rand_points = []
        rands = []
        for i in range(self.clusters):
            while(1):
                rand = random.randint(0,len(self.data.index))   # 0 ~ document의 갯수 범위의 랜덤값 지정 (K개 만큼)
                if rand not in rands:
                    break
            rand_points.append(self.data.loc[self.data.index[rand]][:-1].tolist())
        return rand_points
    def get_jclust(self, cpoints):  # 각 cluster의 jclust값의 합 return
        sum_jclusts = 0
        for i in range(self.clusters):
            sum = 0
            documents = self.data.loc[self.data['cluster']==i].index.tolist()
            for document in documents:
                dist = np.linalg.norm(self.data.loc[document][:-1]-np.array(cpoints[i]))
                sum += dist
            try:
                jclust = sum/len(documents) # 각 군집의 j-clust 값 (중심점과의 거리의 평균)
            except:
                jclust = sum                # i번째 군집에 할당된 document가 없는 경우 jclust=0
            sum_jclusts += jclust       # 각 군집의 j-clust 값들의 합
        return sum_jclusts
    def classify_cluster(self, cpoints):    # 가장 가까운 군집 중심점 기준으로 cluster 할당
        for idx in self.data.index:
            self.data.loc[idx][-1] = self.find_nearest(self.data.loc[idx][:-1], cpoints)
    def set_center(self):   # numpy 평균을 이용해 중심점 다시 지정
        cpoints = []
        for i in range(self.clusters):
            cpoints.append(np.mean(self.data[self.data['cluster']==i],axis=0).tolist()[:-1])
        return cpoints
    def find_nearest(self, point, cpoints):   # 각 점별로 군집 할당
        dists = []
        for i in range(self.clusters):      # 군집의 중심점이 가장 가까운 군집으로 할당
            dist = np.linalg.norm(point-np.array(cpoints[i]))
            dists.append(dist)
        return pd.DataFrame(dists).sort_values(by=0).index[0]
    def get_nearest5(self,cpoints):
        result = []     # 가장 가까운 5개의 document의 index numbers
        index = []      # 군집 갯수만큼 index 리스트 제작 (데이터 프레임으로 변환 시 사용)
        for i in range(self.clusters):
            index.append('cluster '+str(i))
            dists = []
            for idx in self.data.index:
                dist = np.linalg.norm(self.data.loc[idx][:-1]-np.array(cpoints[i]))
                dists.append(dist)
            result.append(self.data.loc[self.data.index[[pd.DataFrame(dists).sort_values(by=0).index[0:5]]]].index.tolist())
        return result, index
            


        
