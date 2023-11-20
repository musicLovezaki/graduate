from PIL import Image

# 保存した画像を開く
image_path = 'output_plot.png'
img = Image.open(image_path)

# 画像を表示
img.show()