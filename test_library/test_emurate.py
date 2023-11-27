#enumerate()関数を利用することで、for文内のループ処理にインデックス番号を付与
my_array = [ '1番目', '2番目', '3番目']
for i, d in enumerate(my_array):
    print('インデックス: ' + str(i) + ' 内容: ' + d )