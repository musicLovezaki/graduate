import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.signal import argrelextrema,find_peaks, savgol_filter
from datetime import datetime
from dateutil.relativedelta import relativedelta


#order 7 windowsize 9

#windowsizeはorderサイズより大きな奇数とする
print("Nikkei Stock Average Time Series Data")
print("windowsize > polynominal chara")
input_windowsize = input("Input windowsize: ")
input_polynominal_chara = input("Input polynomial number of characters:")
try:
    input_windowsize = int(input_windowsize)
    input_polynominal_chara = int(input_polynominal_chara)
except ValueError:
    print("無効な入力です。数字を入力してください。")


# CSVファイルからデータを読み込み
df = pd.read_csv('Nikkei Stock Average Time Series Data.csv')

# グラフの描画

plt.plot(df['date_year'], df['price'], label='Stock Average')

plt.title('Nikkei Stock Average Time Series Data')
plt.xlabel('month-year')
plt.ylabel('price')
plt.legend()
plt.xticks(np.arange(0, len(df['date_year']), step=4))

ticks = 3

fig, ax = plt.subplots()
plt.xticks(rotation=270)
df.plot(ax=ax)
output_file_path = 'static/images/stockAverage.png'
fig.savefig(output_file_path)



window_size = input_windowsize 

# Calculate moving averages to smooth data
smoothed_data = df['price'].rolling(window=window_size).mean()


#Get indices of peaks (mountains) and valleys
peaks = argrelextrema(smoothed_data.values, comparator=lambda x, y: x > y, \
    order=window_size)[0]
valleys = argrelextrema(smoothed_data.values, comparator=lambda x, y: x < y, \
    order=window_size)[0]

# 始点と終点を含む谷と山の値をリストにまとめる
start_point = (df['date_year'].iloc[0], smoothed_data.iloc[0])
end_point = (df['date_year'].iloc[-1], smoothed_data.iloc[-1])
peaks_values = [(df['date_year'].iloc[i], smoothed_data.iloc[i]) for i in peaks]
valleys_values = [(df['date_year'].iloc[i], smoothed_data.iloc[i]) for i in valleys]

# データをNumPyの配列に変換
x_values = df['date_year'].values
y_values = df['price'].values


#Apply Savitzky-Golay filter to smooth data
window_size = input_windowsize 
order = input_polynominal_chara  
smoothed_data = savgol_filter(y_values, window_size, order)

# グラフの描画
plt.plot(x_values, smoothed_data, color = "red",label=f'Smoothed (Savitzky-Golay)')
plt.title('Smoothed Data with Savitzky-Golay Filter')
plt.xlabel('date_year')
plt.ylabel('price')
plt.legend()


plt.xticks(rotation=45, ha='right')
x_ticks = df['date_year'][::6]
plt.xticks(x_ticks)

# Peak detection using find-peaks method
peaks, _ = find_peaks(smoothed_data, height=0)  
prominence_threshold = 0.1
valleys_prominence, _ = find_peaks(-smoothed_data, prominence=prominence_threshold)  # ここでは prominence パラメータを使って、ピークと認識するための相対的な高さの閾値を設定しています。ただし、これはデータの特性によりますので、具体的なデータに合わせて調整

start_point = (x_values[0], smoothed_data[0])
end_point = (x_values[-1], smoothed_data[-1])
peaks_data = [(x_values[i], smoothed_data[i]) for i in peaks]
valleys_data = [(x_values[i], smoothed_data[i]) for i in valleys_prominence]

# ピークと谷の高さ比較
peak_heights = [smoothed_data[i] for i in peaks]
valley_depths = [smoothed_data[i] for i in valleys_prominence]
peak_valley_height_ratios = [peak_heights[i] / valley_depths[i] for i in range(min(len(peak_heights), len(valley_depths)))]

# 対応する x 座標の値
x_peaks = x_values[peaks]
x_valleys = x_values[valleys_prominence]

# 新しいリストを作成
new_list = []

i, j = 0, 0
while i < len(peaks) and j < len(valleys_prominence):
    # x 座標を日付に変換
    peak_date = datetime.strptime(x_peaks[i], '%Y/%m/%d')
    valley_date = datetime.strptime(x_valleys[j], '%Y/%m/%d')

    if peak_date < valley_date:
        new_list.append((x_peaks[i], max(peak_heights[i], valley_depths[j])))
        i += 1
    else:
        new_list.append((x_valleys[j], min(peak_heights[i], valley_depths[j])))
        j += 1

# 残りの値を挿入
while i < len(peaks):
    new_list.append((x_peaks[i], peak_heights[i]))
    i += 1

while j < len(valleys):
    new_list.append((x_valleys[j], valley_depths[j]))
    j += 1


sum = 0
trend_y = []
adverb = []
total_months_differences = []
max_value = max(new_list, key=lambda x: x[1])[1]
min_value = min(new_list, key=lambda x: x[1])[1]
length_y = max_value - min_value
temp_y = 0
texts = []

# 上昇と下降の比率を出力、副詞を使い分けて結果を出力
for i in range(len(new_list) - 1):
    current_x, current_y = new_list[i]
    next_x, next_y = new_list[i + 1]
    

    # 年月を日付オブジェクトに変換
    current_date = datetime.strptime(current_x, '%Y/%m/%d')
    next_date = datetime.strptime(next_x, '%Y/%m/%d')
    
    # 経過月数を計算
    delta = relativedelta(next_date, current_date)
    months_passed = delta.months
    years_passed = delta.years
    total_months_defference = years_passed * 12 + months_passed
    total_months_differences.append(total_months_defference)
    
    #今と次のyの値から求められる比率
    ratio_y = abs((next_y - current_y) / current_y)    
    #全体分の今のy
    temp_ratio_y = current_y / length_y
    
    if next_y > current_y:
        if ratio_y < 0.7:
            trend_y.append("rise")
        else:
            trend_y.append("soar")
    elif next_y < current_y:
        if ratio_y < 0.7:
            trend_y.append("go down")
        else:
            trend_y.append("plummet")
    else:
        trend_y.append("remain flat")

    if ratio_y > 0.5:
        adverb.append("dramatically")
    elif ratio_y > 0.3:
        adverb.append("substantially") 
    elif ratio_y > 0.1:
        adverb.append("significantly") 
    elif ratio_y > 0.03:
        adverb.append("slightly") 
    elif ratio_y > 0.001:
        adverb.append("negligibly")
    else:
        adverb.append("almost unchanged")
    
    if adverb[i] == "almost unchanged":
        continue
    text = f"{current_x} to {next_x} y-coordinate {adverb[i]} {trend_y[i]} and {total_months_differences[i] } months have elapsed."
    texts.append(text)
    


for i in range(len(texts)):
    print(texts[i])
    

output_file_path = 'static/images/stockAverage_savitzky_golay.png'  # 保存するファイルのパス
plt.savefig(output_file_path, dpi=300, bbox_inches='tight')
