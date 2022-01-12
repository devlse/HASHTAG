from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbmakingchallenge

#유저 리스트
# users = list(db.user.find({},{'_id':False}))

#메인페이지
@app.route('/')
def mainPage():
    return render_template('Mainlogout.html')

#로그인페이지
@app.route('/signInPage')
def signInPage():
    return render_template('Login.html')

#회원가입페이지
@app.route('/signUpPage')
def signUpPage():
    return render_template('Account.html')

#로그인버튼
@app.route('/signInPage/in', methods=['POST'])
def signin():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    if db.user.find_one({'id':id_receive},{'_id':False}):
        if db.user.find_one({'pw': pw_receive}, {'_id': False}):
            return jsonify({'signIn': '1'})
    return jsonify({'msg': '아이디/비밀번호가 틀립니다'})

#회원가입버튼
@app.route('/signUpPage/up', methods=['POST'])
def signup():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    question_receive = request.form['question_give']
    answer_receive = request.form['answer_give']
    if id_receive == "":
        return({'msg':'아이디를 입력해주세요'})
    elif db.user.find_one({'id':id_receive},{'_id':False}):
        return jsonify({'msg':'아이디가 있습니다'})
    elif pw_receive == "":
        return ({'msg': '비밀번호를 입력해주세요'})

    user ={
        'id':id_receive,
        'pw':pw_receive,
        'question':question_receive,
        'answer':answer_receive
    }
    # db.user.insert_one(user)
    return jsonify({'signUp': '1'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)