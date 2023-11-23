import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.signal import argrelextrema

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

ticks = 10

fig, ax = plt.subplots()
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

# X軸のメモリを10個飛ばしで表示
x_ticks = df['date_year'][::10]
plt.xticks(x_ticks)

# ピーク（山）と谷のインデックスを取得
peaks = argrelextrema(smoothed_data.values, comparator=lambda x, y: x > y, order=window_size)[0]
valleys = argrelextrema(smoothed_data.values, comparator=lambda x, y: x < y, order=window_size)[0]

# 始点と終点を含む谷と山の値をリストにまとめる
start_point = smoothed_data.iloc[0]
end_point = smoothed_data.iloc[-1]
peaks_values = [smoothed_data.iloc[i] for i in peaks]
valleys_values = [smoothed_data.iloc[i] for i in valleys]

# 結果を表示
print("始点:", start_point)
print("終点:", end_point)
print("山の値:", peaks_values)
print("谷の値:", valleys_values)

# グラフをファイルに保存
output_file_simple_path = 'static/output_graph_simple.png'  # 保存するファイルのパス
plt.savefig(output_file_simple_path)


# グラフの表示
# plt.show()

# # ターミナルから行番号を入力
# try:
#     row1_index = int(input("Enter the line number of the first line: ")) - 1
#     row2_index = int(input("Enter the line number of the next line: ")) - 1

#     # 指定した行のデータを取得
#     row1_data = df.iloc[row1_index]['price']
#     row2_data = df.iloc[row2_index]['price']
    
#     trend_summary = describe_difference(row1_data,row2_data)
#     print("Trend of specified data:"+ trend_summary +"can be seen in this graph")

# except ValueError:
#     print("Invalid input. Please enter an integer line number.")
    

