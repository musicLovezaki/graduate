import pandas as pd

# CSVファイルのパス
csv_file_path = 'GasolinePriceTrends-Excel.csv'

# CSVファイルを読み込む
df = pd.read_csv(csv_file_path)

# 'price'カラムが存在することを確認
if 'price' in df.columns:
    # 'price'カラムをリストに変換
    prices = df['price'].tolist()
    
max_increase = 0
max_decrease = 0

# 価格の変動を調査
for i in range(1, len(prices)):
    change = prices[i] - prices[i - 1]

    # 最大上昇幅を更新
    if change > max_increase:
        max_increase = change

    # 最大下降幅を更新
    elif change < max_decrease:
        max_decrease = change

# 結果を表示
print("最大上昇幅:", max_increase)
print("最大下降幅:", abs(max_decrease))