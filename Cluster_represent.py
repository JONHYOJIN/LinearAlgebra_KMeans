import pandas as pd
import numpy as np

class cluster_represent:
    def __init__(self, data, center_points):
        self.data = data
        self.center_points = center_points
    def get_neighbor5(self):
        neighbors = []
        for i in range(len(self.data.loc['cluster'].value_counts())):
            nnns = self.data.transpose()[self.data.transpose()['cluster']==i].transpose()
            dists = []
            for col in nnns.columns:
                sum=0
                for k, row in enumerate(nnns.index):
                    sum+=(nnns[col][row] - self.center_points[i][k])**2
                dists.append(sum)
            df = pd.DataFrame(dists, index = nnns.columns)
            df = df.sort_values(by=df.columns[0])
            lst = df.index[0:5].tolist()
            neighbors.append(lst)
        return neighbors
    def print_neighbor5(self):
        neighbors = self.get_neighbor5()
        for i, lst in enumerate(neighbors):
            print("{}th Cluster's Neighbors: {}\n".format(i+1, lst))
        
