import pandas as pd
import numpy as np

class KMeans_DF:
    def __init__(self):
        self.path_xlsx = './KMeans Data/termDocMatrix.xlsx'
        self.path_txt  = './KMeans Data/word-docTitle.txt'
    def get_DF(self):
        rows, columns = self.get_rowcol()
        data = pd.read_excel(self.path_xlsx,header=None,index_col=0,names = columns)
        data.index = rows
        data.loc['cluster']=0
        return data
    def get_rowcol(self):
        worddoc = []
        with open(self.path_txt,'r') as f:
            for line in f:
                line = line.replace('    "','')
                line = line.replace('"\n','')
                line = line.replace('"','')
                worddoc.append(line)
        del worddoc[0]
        del worddoc[-1]
        for i in range(3):
            del worddoc[4423]
        rows = worddoc[0:4423]
        columns = worddoc[4423:]
        
        return rows, columns
