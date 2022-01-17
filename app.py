import bcrypt
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbmakingchallenge


#유저 리스트
users = list(db.user.find({},{'_id':False}))

#메인페이지
@app.route('/')
def mainPage():
    return render_template('Mainlogout.html')

@app.route('/main')
def mainPage2():
    return render_template('Mainlogin.html')

#로그인페이지
@app.route('/login')
def signInPage():
    return render_template('Login.html')

#회원가입페이지
@app.route('/signup')
def signUpPage():
    return render_template('Account.html')

#관심단어 등록 페이지
@app.route('/myword')
def mywordPage():
    return render_template('record_list.html')

#로그인버튼
@app.route('/login/in', methods=['POST'])
def signin():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    for target in users:
        if id_receive == target['id']:
            check_password = target['pw'].encode('utf-8')
            if bcrypt.checkpw(pw_receive.encode('utf-8'), check_password):
                print('return')
                return jsonify({'signIn': '1'})
    return jsonify({'msg': '아이디/비밀번호가 틀립니다'})

#회원가입버튼
@app.route('/signup/up', methods=['POST'])
def signup():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    # 아이디값 공백 검사
    if id_receive == "":
        return({'msg':'아이디를 입력해주세요'})
    # DB에서 중복 아이디 검사
    elif db.user.find_one({'id':id_receive},{'_id':False}):
        return jsonify({'msg':'아이디가 있습니다'})
    # 패스워드값 공백 검사
    elif pw_receive == "":
        return ({'msg': '비밀번호를 입력해주세요'})
    #비밀번호 해싱
    encode_password = bcrypt.hashpw(pw_receive.encode('utf-8'), bcrypt.gensalt())
    #해싱값 str변환 -> DB저장
    hashed_password = encode_password.decode('utf-8')

    user ={
        'id':id_receive,
        'pw':hashed_password,
    }
    db.user.insert_one(user)
    return jsonify({'signUp': '1'})

#검색어 저장
@app.route('/', methods=['POST'])
def search_post():
    search_word_receive = request.form['searchWord_give']
    doc = {
        'search': search_word_receive
    }
    db.searchword.insert_one(doc)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)