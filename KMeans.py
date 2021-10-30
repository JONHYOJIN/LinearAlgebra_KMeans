import pandas as pd
import numpy as np
from KMeans_getDF import KMeans_DF

kmeans_df = KMeans_DF()
data = kmeans_df.get_DF()

print(data.head())

