import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.signal import argrelextrema,find_peaks, savgol_filter
from datetime import datetime
from dateutil.relativedelta import relativedelta

def describe_difference(num_before: int, num_after: int) -> str:
    
    DESCRIPTIONS = ("increase", "remain the same", "decrease")
    description: str = ""
    if num_after > num_before:
        description = DESCRIPTIONS[0]
    elif num_after == num_before:
        description = DESCRIPTIONS[1]
    else:
        description = DESCRIPTIONS[2]
        
    return description

VERB_GROUPS: tuple = (
    ("increase", "remain the same", "decrease"),
    ("rise","stay the same","fail"),
)

def describe_difference2(
    num_before: int, num_after: int, verb_group_id: int
) -> tuple[str,int]:
    
    description: str = ""
    if num_after > num_before:
        description = VERB_GROUPS[verb_group_id % len(VERB_GROUPS)][0]
    elif num_after == num_before:
        description = VERB_GROUPS[verb_group_id % len(VERB_GROUPS)][1]
    else:
        description = VERB_GROUPS[verb_group_id % len(VERB_GROUPS)][2]
    
    verb_group_id += 1
    return description, verb_group_id


# CSVファイルからデータを読み込み
df = pd.read_csv('GasolinePriceTrends-Excel.csv')

# グラフの描画

plt.plot(df['date_year'], df['price'])

plt.xticks(np.arange(0, len(df['date_year']), step=4))
plt.xlabel('month-year')
plt.ylabel('price')
plt.title('Gasoline_price_Trends')

ticks = 3

fig, ax = plt.subplots()
plt.xticks(rotation=270)
df.plot(ax=ax)
output_file_path = 'static/output_plot.png'
fig.savefig(output_file_path)


# データをスムージングするために移動平均を計算
window_size = 3 # 移動平均のウィンドウサイズ（調整が必要な場合は変更してください）
smoothed_data = df['price'].rolling(window=window_size).mean()

# グラフの描画

plt.plot(df['date_year'], smoothed_data, label=f'Smoothed (window size={window_size})')
plt.title('Smoothed Data with Trend Line')
plt.xlabel('date_year')
plt.ylabel('price')
plt.legend()

plt.xticks(rotation=270)
# X軸のメモリを10個飛ばしで表示
x_ticks = df['date_year'][::3]
plt.xticks(x_ticks)

# ピーク（山）と谷のインデックスを取得
peaks = argrelextrema(smoothed_data.values, comparator=lambda x, y: x > y, order=window_size)[0]
valleys = argrelextrema(smoothed_data.values, comparator=lambda x, y: x < y, order=window_size)[0]

# 始点と終点を含む谷と山の値をリストにまとめる
start_point = (df['date_year'].iloc[0], smoothed_data.iloc[0])
end_point = (df['date_year'].iloc[-1], smoothed_data.iloc[-1])
peaks_values = [(df['date_year'].iloc[i], smoothed_data.iloc[i]) for i in peaks]
valleys_values = [(df['date_year'].iloc[i], smoothed_data.iloc[i]) for i in valleys]

# 結果を表示
# print("argrelextremaを用いたpeak検出法")
# print("始点:", start_point)
# print("終点:", end_point)
# print("山の値:", peaks_values)
# print("谷の値:", valleys_values)
# print("-----------------------------")

# グラフをファイルに保存
output_file_simple_path = 'static/output_graph_simple.png'  # 保存するファイルのパス
plt.savefig(output_file_simple_path)

# データをNumPyの配列に変換
x_values = df['date_year'].values
y_values = df['price'].values

# データをスムージングするためにSavitzky-Golayフィルタを適用
window_size = 9  # ウィンドウサイズ（調整が必要な場合は変更してください）
order = 7  # 多項式の次数（調整が必要な場合は変更してください）
smoothed_data = savgol_filter(y_values, window_size, order)

# グラフの描画

plt.plot(x_values, smoothed_data, label=f'Smoothed (Savitzky-Golay)')
plt.title('Smoothed Data with Savitzky-Golay Filter')
plt.xlabel('date_year')
plt.ylabel('price')
plt.legend()

plt.xticks(rotation=270)
x_ticks = df['date_year'][::3]
plt.xticks(x_ticks)

# Savitzky-Golay法を使用してピークを検出
peaks, _ = find_peaks(smoothed_data, height=0)  # heightはピークとみなす閾値（調整が必要な場合は変更してください）
prominence_threshold = 0.1
valleys_prominence, _ = find_peaks(-smoothed_data, prominence=prominence_threshold)  # ここでは prominence パラメータを使って、ピークと認識するための相対的な高さの閾値を設定しています。ただし、これはデータの特性によりますので、具体的なデータに合わせて調整

start_point = (x_values[0], smoothed_data[0])
end_point = (x_values[-1], smoothed_data[-1])
peaks_data = [(x_values[i], smoothed_data[i]) for i in peaks]
valleys_data = [(x_values[i], smoothed_data[i]) for i in valleys]

print("Savitzky-Golay法を用いたpeak検出法")
print("始点:", start_point)
print("終点:", end_point)
print("山の値と位置:", peaks_data)
print("谷の値と位置:", valleys_data)

# ピークと谷の高さ比較
peak_heights = [smoothed_data[i] for i in peaks]
valley_depths = [smoothed_data[i] for i in valleys]
peak_valley_height_ratios = [peak_heights[i] / valley_depths[i] for i in range(min(len(peak_heights), len(valley_depths)))]

# 対応する x 座標の値
x_peaks = x_values[peaks]
x_valleys = x_values[valleys]

# 新しいリストを作成
new_list = [(x_values[0], y_values[0])]


i, j = 0, 0
while i < len(peaks) and j < len(valleys):
    # x 座標を日付に変換
    peak_date = datetime.strptime(x_peaks[i], '%y-%b')
    valley_date = datetime.strptime(x_valleys[j], '%y-%b')

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


# 結果を表示
print("新しいリスト:", new_list)
    
# 上昇と下降の比率を出力、副詞を使い分けて結果を出力
for i in range(len(new_list) - 1):
    current_x, current_y = new_list[i]
    next_x, next_y = new_list[i + 1]

    # 年月を日付オブジェクトに変換
    current_date = datetime.strptime(current_x, '%y-%b')
    next_date = datetime.strptime(next_x, '%y-%b')
    
    # 経過月数を計算
    months_passed = relativedelta(next_date, current_date).months
    
    ratio_y = abs((next_y - current_y) / current_y)    

    if next_y > current_y:
        trend_y = "上昇"
    elif next_y < current_y:
        trend_y = "下降"
    else:
        trend_y = "変化なし"

    if ratio_y > 0.25:
        adverb = "極めて" 
    elif ratio_y > 0.1:
        adverb = "急激に" 
    elif ratio_y > 0.075:
        adverb = "非常に" 
    elif ratio_y > 0.05:
        adverb = "ひどく" 
    elif ratio_y > 0.03:
        adverb = "少し"
    elif ratio_y > 0.001:
        adverb = "わずかに"
    else:
        adverb = "とても" 

    #print(f"{current_x}から{next_x}までに{adverb}{trend_y}した。{ratio_y:.4f}")
    print(f"{current_x}から{next_x}までにy座標が{next_y - current_y} {trend_y}し、{months_passed}ヶ月経過しました。")

output_file_path = 'static/output_graph_savitzky_golay.png'  # 保存するファイルのパス
plt.savefig(output_file_path)