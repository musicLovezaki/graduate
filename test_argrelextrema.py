

import numpy as np
from scipy.signal import argrelextrema

data = np.array([1, 3, 7, 1, 2, 6, 4, 8, 3, 5])

# 極大値のインデックスを取得（前後2つのデータポイントと比較）
peaks = argrelextrema(data, np.greater, order=2)[0]

print("極大値のインデックス:", peaks)