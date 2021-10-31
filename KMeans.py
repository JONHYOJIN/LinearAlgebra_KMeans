import pandas as pd
import numpy as np
import random

class Kmeans:
    def __init__(self, data, clusters):
        self.data = data            # KMeans를 수행하는 데이터
        self.clusters = clusters    # 구분할 cluster의 수
        self.max_iter = 20           # 최대 반복 횟수 (20으로 고정)
    def do_kmeans(self):
        rd_players = self.get_random_point()
        center_points = []
        j_clusters = []
        for player in rd_players:
            center_points.append(self.data[player].tolist())
        for iter in range(self.max_iter):
            pre_center_points = center_points
            cluster = self.get_cluster(center_points)
            center_points = self.get_centers(cluster)
            j_clusters.append(self.get_j_clusters(center_points))
            if pre_center_points == center_points:
                break
        result_data = self.data
        return result_data, center_points, j_clusters
    def get_random_point(self):
        rand_nums = []
        rand_players = []
        for i in range(self.clusters):
            rand = random.randint(0,499)
            while rand in rand_nums:
                rand = random.randint(0,499)
            rand_nums.append(rand)
            rand_players.append(self.data.columns[rand])
        return rand_players
    def get_cluster(self, center_points):
        cluster = []
        for col in self.data.columns:
            distance = []
            for j in range(len(center_points)):
                sum=0
                for i in range(len(self.data[col])-1):
                    dist = (self.data[col][i] - center_points[j][i]) ** 2
                    sum+=dist
                distance.append(sum)
            df = pd.DataFrame([distance])
            df = df.iloc[:,np.argsort(df.loc[0])]
            cluster.append(df.columns[0])
        self.data.loc['cluster']=cluster
        return cluster
    def get_centers(self, cluster):
        center_points=[]
        for i in range(len(pd.DataFrame(cluster).value_counts().index)):
            mean_point = []
            players = self.data.loc[:,self.data.loc['cluster']==i].columns.tolist()
            for index in self.data[players].index:
                mean_point.append(np.mean(self.data[players].loc[index]))
            center_points.append(mean_point)
        return center_points
    def get_j_clusters(self, center_points):
        j_clusters = []
        for i, point in enumerate(center_points):
            sum = 0
            players = self.data.loc[:,self.data.loc['cluster']==i].columns.tolist()
            for player in players:
                for j in range(len(self.data[player])):
                    sum+=(self.data[player][j]-center_points[i][j])**2
                sum = sum / len(self.data[player])
            sum = sum / len(players)
            j_clusters.append(sum)
        return j_clusters

            


        
