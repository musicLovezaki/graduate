from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    # 保存した画像のパス
    image_path = 'static/output_plot.png'
    
    # テンプレートに画像のパスを渡して表示
    return render_template('index.html', image_path=image_path)

@app.route('/simple_ver')
def simple_ver():
    simple_image_path = 'static/output_graph_simple.png'
    
    return render_template('index.html', image_path=simple_image_path)

if __name__ == '__main__':
    app.run(debug=True)
