from flask import Flask, render_template
import createPlot as CP

app = Flask(__name__)

@app.route('/')
def index():
    # 保存した画像のパス
    image_path = 'static/output_plot.png'
    generated_texts = "-"
    
    # テンプレートに画像のパスを渡して表示
    return render_template('index.html',texts=generated_texts, image_path=image_path)

@app.route('/simple_ver')
def simple_ver():
    simple_image_path = 'static/output_graph_simple.png'
    generated_texts = "-"
    
    return render_template('index.html',texts=generated_texts, image_path=simple_image_path)

@app.route('/Savitzky-Golay')
def Savitzky_Golay():
    Savitzky_Golay_path = 'static/output_graph_savitzky_golay.png'
    generated_texts = CP.texts
    
    return render_template('index.html',texts=generated_texts,image_path=Savitzky_Golay_path)

if __name__ == '__main__':
    app.run(debug=True)
