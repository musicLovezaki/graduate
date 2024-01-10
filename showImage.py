from flask import Flask, render_template
from createPlot import texts, window_size
import subprocess

app = Flask(__name__)

#FLASK_APP=showImage.py FLASK_ENV=development flask run でhtml出力できる

class MyClass:
    def __init__(self) -> None:
        result = subprocess.run(['ls', '-l'], stdout=subprocess.PIPE, text=True)
        
        print(result.stdout)



@app.route('/', methods=['GET'])
def index():
    # 保存した画像のパス
    image_path = 'static/output_plot.png'
    generated_texts = "-"
    
    # テンプレートに画像のパスを渡して表示
    return render_template('index.html',texts=generated_texts, image_path=image_path)


@app.route('/Savitzky-Golay', methods=['GET'])
def Savitzky_Golay():
    original = 'static/output_plot.png'
    Savitzky_Golay_path = 'static/output_graph_savitzky_golay.png'
    generated_texts = []
    
    generated_texts = texts
    show_window_image = window_size
    
    return render_template('index.html',texts=generated_texts,image_savitgolay=Savitzky_Golay_path,image_original = original,window_size = show_window_image)


with app.app_context():
    app.run(debug=True)