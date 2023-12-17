from flask import Flask, render_template, request, session


app = Flask(__name__)
app.secret_key = 'zzzzz'


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
        input_number = int(request.form['input_number'])  # フォームからの数字を取得
        session['input_number'] = input_number  # セッションにデータを保存
    else:
        input_number = session.get('input_number', None)  # セッションからデータを取得
    
    return render_template('index.html',texts=generated_texts, image_path=image_path,input_number=input_number)

@app.route('/Savitzky-Golay', methods=['GET'])
def Savitzky_Golay():
    Savitzky_Golay_path = 'static/output_graph_savitzky_golay.png'
    #generated_texts = CP.texts
    generated_texts = ["-","dsds"]
    
    return render_template('index.html',texts=generated_texts,image_path=Savitzky_Golay_path)

if __name__ == '__main__':
    app.run(debug=True)
