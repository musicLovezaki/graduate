from flask import Flask, render_template, request
import createPlot as CP

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    # 保存した画像のパス
    image_path = 'static/output_plot.png'
    generated_texts = "-"
    
    # テンプレートに画像のパスを渡して表示
    return render_template('index.html',texts=generated_texts, image_path=image_path)

@app.route('/simple_ver', methods=['GET'])
def simple_ver():
    image_path = 'static/output_graph_simple.png'
    generated_texts = ["-","dsds"]

    if request.method == 'POST':
        input_value = request.form['input_name']
        print("Received input:", input_value)
        
    return render_template('index.html',texts=generated_texts, image_path=image_path)

@app.route('/Savitzky-Golay', methods=['GET'])
def Savitzky_Golay():
    Savitzky_Golay_path = 'static/output_graph_savitzky_golay.png'
    generated_texts = CP.texts
    
    return render_template('index.html',texts=generated_texts,image_path=Savitzky_Golay_path)

if __name__ == '__main__':
    app.run(debug=True)
