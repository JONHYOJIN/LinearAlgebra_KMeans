import pandas as pd
import numpy as np

class GetDF:
    def __init__(self):
        self.path_xlsx = './KMeans Data/termDocMatrix.xlsx'
        self.path_txt  = './KMeans Data/word-docTitle.txt'
    def get_df(self):
        rows, columns = self.get_rowcol()
        data = pd.read_excel(self.path_xlsx,header=None,index_col=0,names = columns)
        data.index = rows
        data.loc['cluster']=0   # target값을 cluster칼럼을 추가하면서 추가
        data = np.transpose(data)   # row와 column 자리 변경 (document별로 군집화를 진행하므로 더 편하게 하기 위해서)
        return data
    def get_rowcol(self):
        # txt파일을 읽어와서 불피요한 띄어쓰기, 줄바꿈 등은 없애고 row와 column으로 구분
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
