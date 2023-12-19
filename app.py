# 필수 라이브러리
'''
0. Flask : 웹서버를 시작할 수 있는 기능. app이라는 이름으로 플라스크를 시작한다
1. render_template : html파일을 가져와서 보여준다
'''
from flask import Flask, render_template, request, redirect, url_for, jsonify
app = Flask(__name__)
# DB 기본 코드
import os
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')

db = SQLAlchemy(app)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    belong = db.Column(db.String, nullable=False)
    armynumber = db.Column(db.String, nullable=False)
    disease = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)

    def __repr__(patient):
        return f'{patient.belong} {patient.armynumber} {patient.username} {patient.disease} 검사결과 {patient.phone}점'

with app.app_context():
    db.create_all()

# 설문지를 위한 기본 데이터
questions = [
    {"id": 1, "question": "Question 1: Choose C, D, or E"},
    {"id": 2, "question": "Question 2: Choose C, D, or E"},
    {"id": 3, "question": "Question 3: Choose C, D, or E"},
    {"id": 4, "question": "Question 4: Choose D or E"},
    {"id": 5, "question": "Question 5: Choose D or E"},
    {"id": 6, "question": "Question 6: Choose D or E"}
]

# 초기 점수
score = 0


@app.route("/")
def armysolution():
    return render_template('armysolution.html')

@app.route("/depression/")
def depression():
    return render_template('depression.html')

@app.route('/depression/submit/', methods=['POST'])
def depression_submit():
    # 각 문항에 대한 답변을 받아옴
    answers = [int(request.form[f'question_{i}']) for i in range(1, 10)]
    
    # 답변의 총합 계산
    total_score = sum(answers)
    
    # 결과 페이지로 이동
    if 20 <= total_score <= 27:
        return redirect(url_for('depression_result1'))
    elif 10 <= total_score <= 19:
        return redirect(url_for('depression_result2'))
    elif 5 <= total_score <= 9:
        return redirect(url_for('depression_result3'))
    elif 0 <= total_score <= 4:
        return redirect(url_for('depression_result4'))

@app.route('/depression_result1/',methods=['GET'])
def depression_result1():
    return render_template('depression_result1.html')

@app.route('/depression_result2/',methods=['GET'])
def depression_result2():
    return render_template('depression_result2.html')

@app.route('/depression_result3/',methods=['GET'])
def depression_result3():
    return render_template('depression_result3.html')

@app.route('/depression_result4/',methods=['GET'])
def depression_result4():
    return render_template('depression_result4.html')

@app.route("/anxiety/")
def anxiety():
    return render_template('anxiety.html')

@app.route('/anxiety/submit/', methods=['POST'])
def anxiety_submit():
    # 각 문항에 대한 답변을 받아옴
    answers = [int(request.form[f'question_{i}']) for i in range(1, 22)]
    
    # 답변의 총합 계산
    total_score = sum(answers)
    
    # 결과 페이지로 이동
    if 32 <= total_score <= 63:
        return redirect(url_for('anxiety_result1'))
    elif 27 <= total_score <= 31:
        return redirect(url_for('anxiety_result2'))
    elif 22 <= total_score <= 26:
        return redirect(url_for('anxiety_result3'))
    elif 0 <= total_score <= 21:
        return redirect(url_for('anxiety_result4'))

@app.route('/anxiety_result1/',methods=['GET'])
def anxiety_result1():
    return render_template('anxiety_result1.html')

@app.route('/anxiety_result2/',methods=['GET'])
def anxiety_result2():
    return render_template('anxiety_result2.html')

@app.route('/anxiety_result3/',methods=['GET'])
def anxiety_result3():
    return render_template('anxiety_result3.html')

@app.route('/anxiety_result4/',methods=['GET'])
def anxiety_result4():
    return render_template('anxiety_result4.html')

@app.route("/ptsd/")
def ptsd():
    return render_template('ptsd.html')

@app.route('/ptsd/submit/', methods=['POST'])
def ptsd_submit():
    # 각 문항에 대한 답변을 받아옴
    answers = [int(request.form[f'question_{i}']) for i in range(1, 21)]
    
    # 답변의 총합 계산
    total_score = sum(answers)
    
    # 결과 페이지로 이동
    if total_score >= 32:
        return redirect(url_for('ptsd_result1'))
    else :
        return redirect(url_for('ptsd_result2'))

@app.route('/ptsd_result1/',methods=['GET'])
def ptsd_result1():
    return render_template('ptsd_result1.html')

@app.route('/ptsd_result2/',methods=['GET'])
def ptsd_result2():
    return render_template('ptsd_result2.html')

@app.route("/adhd/")
def adhd():
    return render_template('adhd.html')

@app.route('/adhd/submit/', methods=['POST'])
def adhd_submit():
    global score
    score = 0

    for i in range(1, 7):
        answer = request.form.get(f"question_{i}")
        # 각 질문당 점수 계산
        if i in [1, 2, 3] and answer in ['C', 'D', 'E']:
            score += 1
        elif i in [4, 5, 6] and answer in ['D', 'E']:
            score += 1

    # 결과 페이지로 이동
    if score >= 4:
        return redirect(url_for('adhd_result1'))
    else:
        return redirect(url_for('adhd_result2'))

@app.route('/adhd_result1',methods=['GET'])
def adhd_result1():
    return render_template('adhd_result1.html')

@app.route('/adhd_result2', methods=['GET'])
def adhd_result2():
    return render_template('adhd_result2.html')

@app.route("/armysolution/create/", methods=['POST'])
def armysolution_create():
    # form에서 보낸 데이터 받아오기
    if request.method == 'POST':
        username_receive = request.form.get("username")
        belong_receive = request.form.get("belong")
        armynumber_receive = request.form.get("armynumber")
        disease_receive = request.form.get("disease")
        phone_receive = request.form.get("phone")
    
    # 데이터를 DB에 저장하기
    patient = Patient(username=username_receive, armynumber=armynumber_receive, belong=belong_receive, disease=disease_receive, phone=phone_receive)
    db.session.add(patient)
    db.session.commit()

    return render_template('success.html')

    
if __name__ == "__main__":
    app.run(debug=True)
