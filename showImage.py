from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # SQLiteデータベースを使用
db = SQLAlchemy(app)

class InputData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    input_number = db.Column(db.Integer)

@app.route('/', methods=['GET'])
def index():
    # 保存した画像のパス
    image_path = 'static/output_plot.png'
    generated_texts = "-"
    
    # テンプレートに画像のパスを渡して表示
    return render_template('index.html',texts=generated_texts, image_path=image_path)

@app.route('/simple_ver', methods=['GET', 'POST'])
def simple_ver():
    image_path = 'static/output_graph_simple.png'
    generated_texts = ["-","dsds"]
    
    if request.method == 'POST':
        input_number = int(request.form['input_number'])
        new_input = InputData(input_number=input_number)
        db.session.add(new_input)
        db.session.commit()
    else:
        latest_input = InputData.query.order_by(InputData.id.desc()).first()
        input_number = latest_input.input_number if latest_input else None
    
    return render_template('index.html',texts=generated_texts, image_path=image_path,input_number=input_number)

@app.route('/Savitzky-Golay', methods=['GET'])
def Savitzky_Golay():
    Savitzky_Golay_path = 'static/output_graph_savitzky_golay.png'
    #generated_texts = CP.texts
    generated_texts = ["-","dsds"]
    
    return render_template('index.html',texts=generated_texts,image_path=Savitzky_Golay_path)
#if __name__ == '__main__':
 #   db.create.all()
  #  app.run(debug=True)

with app.app_context():
    db.create_all()
    app.run(debug=True)