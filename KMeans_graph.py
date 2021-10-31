import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA

class Kmeans_graph:
    def __init__(self, data, center_points, j_clusters):
        self.data = data
        self.center_points = center_points
        self.j_clusters = j_clusters
    def j_cluster_plot(self):
        j_sum = []
        for i in pd.DataFrame(self.j_clusters).index:
            sum = 0
            for k in pd.DataFrame(self.j_clusters).columns:
                sum+=pd.DataFrame(self.j_clusters)[k][i]/len(pd.DataFrame(self.j_clusters).columns)
            j_sum.append(sum)
        plt.bar(pd.DataFrame(j_sum).index,j_sum)
        plt.xlabel('Iteration')
        plt.ylabel('Sum of j cluster values')
        plt.title("The sum of each Iteration's j cluster values")
        plt.show()
    def scatter_plot(self):
        plt.bar(self.data.loc['cluster'].value_counts().index, self.data.loc['cluster'].value_counts())
        plt.xlabel('Cluster No.')
        plt.ylabel('The number of players')
        plt.title('The player number of each Cluster')
        plt.show()
    def pca_plot(self):
        pca = PCA(n_components=2)
        pca_components = pca.fit_transform(self.data.iloc[:4423].transpose())
        pca_df = pd.DataFrame(data = pca_components, columns = ['pca_1','pca_2'])
        pca_df['cluster'] = self.data.transpose()['cluster'].tolist()

        for i in pca_df['cluster'].value_counts().index:
            x_axis_data = pca_df[pca_df['cluster']==i]['pca_1']
            y_axis_data = pca_df[pca_df['cluster']==i]['pca_2']
            plt.scatter(x_axis_data, y_axis_data, label = i)
        plt.legend()
        plt.xlabel('PCA_1')
        plt.ylabel('PCA_2')
        plt.show()