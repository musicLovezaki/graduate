import pandas as pd

sr = pd.Series(range(10))

windows = 3
# 自身も含めた後ろ3つの要素の和を取る
sum_sr = sr.rolling(windows).sum()
print(sum_sr)

#min_periodsの指定により、windowで指定した値の個数よりも少ない場合のNan値を減らすことができる
sum_sr2 = sr.rolling(windows, min_periods=1).sum()
print('------')
print(sum_sr2)

#対象インデックスを中心として窓関数を適用する
sum_sr3 =  sr.rolling(3,center=True).sum()
print('------')
print(sum_sr3)