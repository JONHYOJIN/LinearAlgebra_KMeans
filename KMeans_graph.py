import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA

class KmeansGraph:
    def __init__(self, classified_data, jclusts):
        self.data_c = classified_data
        self.data = classified_data.drop(['cluster'], axis=1)
        self.jclusts = jclusts
    def make_graph(self):
        result_df, center_df = self.seperate_data(self.data_c)
        pca_data = self.do_pca()
        result_df_pca, center_df_pca = self.seperate_data(pca_data)
        result_df_pca['cluster'] = result_df['cluster']
        center_df_pca['cluster'] = center_df['cluster']

        self.jclust_visualize() # Iteration별로 j-clust값을 보여주는 Bar Plot
        plt.show()
        print("\n")
        self.data_visualize(result_df_pca, center_df_pca) # 군집화된 데이터를 차원축소 후 시각화
        plt.show()

    def seperate_data(self, data):  # 데이터를 document 데이터와 중심점 데이터로 구분
        result_df = data.loc[:data.index[len(data.loc[:'cluster 0'])-2]]
        center_df = data['cluster 0':]
        return result_df, center_df
    def do_pca(self):   # 시각화를 위한 차원축소 함수 (변수 4423개 -> 2개)
        pca = PCA(n_components=2)
        pca_components = pca.fit_transform(self.data)
        pca_df = pd.DataFrame(pca_components, columns=['PCA 1','PCA 2'], index=self.data.index)
        return pca_df
    def jclust_visualize(self): # j-clust 시각화 함수
        jclusts_df = pd.DataFrame(self.jclusts, columns=['J-clusts value'])
        plt.bar(jclusts_df.index, jclusts_df['J-clusts value'])
        plt.xlabel('Iters')
        plt.ylabel('J-clusts value')
        plt.title('Sum of J-clusts values')
    def data_visualize(self, result_df_pca, center_df_pca):  # 차원축소된 데이터 시각화
        clust_num = []  # 각 군집 이름 저장
        for i in range(len(result_df_pca['cluster'].value_counts())):   # 군집별로 document 데이터 시각화
            clust_num.append('cluster '+str(i))
            plt.scatter(result_df_pca[result_df_pca['cluster']==i]['PCA 1'], result_df_pca[result_df_pca['cluster']==i]['PCA 2'])
        plt.legend(clust_num)
        for i in range(len(center_df_pca['cluster'].value_counts())):   # 중심점 시각화(빨간색 별모양)
            plt.scatter(center_df_pca[center_df_pca['cluster']==i]['PCA 1'], center_df_pca[center_df_pca['cluster']==i]['PCA 2'],marker='*',color='r',s=150)
        plt.xlabel('PCA 1')
        plt.ylabel('PCA 2')
        plt.title('KMeans Clustering')
