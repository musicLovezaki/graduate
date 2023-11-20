import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

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
fig.savefig('output_plot.png')
# グラフの表示

# plt.show()

# ターミナルから行番号を入力
try:
    row1_index = int(input("Enter the line number of the first line: ")) - 1
    row2_index = int(input("Enter the line number of the next line: ")) - 1

    # 指定した行のデータを取得
    row1_data = df.iloc[row1_index]['price']
    row2_data = df.iloc[row2_index]['price']
    
    trend_summary = describe_difference(row1_data,row2_data)
    print("Trend of specified data:"+ trend_summary +"can be seen in this graph")

except ValueError:
    print("Invalid input. Please enter an integer line number.")
    

