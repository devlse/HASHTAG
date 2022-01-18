from flask import Flask, render_template, jsonify, request
from datetime import datetime, timedelta
from pytz import timezone
import bcrypt
import jwt
from JWT_info import * #*자리에 secret, algorithm, MIN로 되어있었는데 이러니까 제 컴퓨터에선 오류가 나더라구요 그래서 일단 주석처리합니다
today = datetime.now(timezone('Asia/Seoul'))


app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbmakingchallenge


#DB속 유저 리스트
users = list(db.user.find({},{'_id': False}))

#유저 jwt 체크 데코레이터
def check(func):
    def check_Token():
        cookie = request.cookies.get('Authorization')
        # cookie = request.headers['Authorization'] client -> server 헤더로 쿠키값을 싫어서 보낸다.
        try:
            print('{}'.format(func.__name__))
            #유저 아이디값 불러와서 인자로 넣어주기!
            user_id = jwt.decode(cookie, secret, algorithm)['user_id']
            return func(user_id)
        except jwt.ExpiredSignatureError:
            return jsonify({'msg':'로그인 시간이 만료되었습니다.'})
        except jwt.exceptions.DecodeError:
            return jsonify({'msg': "로그인 정보가 존재하지 않습니다."})
    check_Token.__name__ = func.__name__
    return check_Token


#####


#메인페이지
@app.route('/')
def mainPage():
    return render_template('Mainlogout.html')


@app.route('/main-page')
@check
def mainPage2(user_id):
    return render_template('Mainlogin.html', name=user_id)

#로그인페이지
@app.route('/login-page')
def login_page():
    return render_template('Login.html')

#회원가입페이지
@app.route('/signup-page')
def signup_Page():
    return render_template('Account.html')

#검색결과 보여주는 페이지
@app.route('/searched-result')
def resultPage():
    return render_template('Result.html')

#관심단어 등록 페이지
@app.route('/myword-page')
def mywordPage():
    return render_template('record_list.html')

#임시 메인 페이지
@app.route('/temporary-main-page')
def temporaryMainPage():
    return render_template('testpage.html')

###


#로그인버튼
@app.route('/login', methods=['POST'])
def login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    for target in users:
        if id_receive == target['user_id']:
            check_password = target['user_pw'].encode('utf-8')
            if bcrypt.checkpw(pw_receive.encode('utf-8'), check_password):
                payload={
                    'user_id':id_receive,
                    'exp':datetime.utcnow() + timedelta(minutes=MIN)
                    # 'exp': datetime.utcnow() + timedelta(minutes=10)
                }
                # 토큰인코딩
                access_token = jwt.encode(payload, secret, algorithm)
                # 토큰디코딩
                # check_token = jwt.decode(access_token, secret, algorithm)
                # 유저 아이디 값
                return jsonify({'signIn': '1', 'Authorization': access_token})
    return jsonify({'msg': '아이디/비밀번호가 틀립니다'})

#회원가입버튼
@app.route('/signup', methods=['POST'])
def signup():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    # 아이디값 공백 검사
    if id_receive == "":
        return({'msg':'아이디를 입력해주세요'})
    # DB에서 중복 아이디 검사
    elif db.user.find_one({'user_id':id_receive},{'_id':False}):
        return jsonify({'msg':'아이디가 있습니다'})
    # 패스워드값 공백 검사
    elif pw_receive == "":
        return ({'msg': '비밀번호를 입력해주세요'})
    #비밀번호 해싱
    encode_password = bcrypt.hashpw(pw_receive.encode('utf-8'), bcrypt.gensalt())
    #해싱값 str변환 -> DB저장
    hashed_password = encode_password.decode('utf-8')

    user ={
        'user_id':id_receive,
        'user_pw':hashed_password,
    }
    db.user.insert_one(user)
    return jsonify({'signUp': '1'})

#검색어 저장
@app.route('/searchword', methods=['POST'])
def search_post():
    search_word_receive = request.form['searchWord_give']
    doc = {
        'search': search_word_receive
    }
    db.searchword.insert_one(doc)
    return jsonify({'msg': '결과 보러가기'})

@app.route('/search', methods=['GET'])
def searchaaa():
    word = list(db.searchword.find({}, {'_id': False}))
    return jsonify({'search_word': word})

#검색어와 메모 저장
@app.route('/result-save', methods=['POST'])
def saving_memo():
    myword_receive = request.form['myword_give'] #검색한 단어
    num_receive = request.form['num_give'] #아이디값 저장
    memo_receive = request.form['memo_give']
    keyword_receive = request.form['keyword_give']
    link_receive = request.form['link_give']

    doc = {
        'myword': myword_receive,
        'saving-num': num_receive,
        'memo': memo_receive,
        'keyword': keyword_receive,
        'link': link_receive
    }
    db.onedaylive.insert_one(doc)
    return jsonify({'msg' : '검색어가 저장되었습니다.'}) #검색어 보여주기

#저장된 단어들 보여줌
@app.route('/searchlist', methods=['GET'])
def record():
    searchs = list(db.onedaylive.find({}, {'_id': False}))
    return jsonify({'all_searchs': searchs})

#저장된 결과들 보여줌 = 특정 한 단어에 대한 결과-메모,키워드,링크 만 보여줌
@app.route('/searchitem', methods=['POST']) #search에서 searchlist로 바꿈
def show_item():
    savenum_receive = request.form['savenum_give']
    items = list(db.onedaylive.find({'saving-num': savenum_receive}, {'_id': False}))
    return jsonify({'items': items})

#저장된 내용 지우기
@app.route('/delete-item', methods=['POST'])
def delete_one():
    saved_num = request.form['saved_num']
    remaining = list(db.onedaylive.delete_one({'saving-num': saved_num})) #여기가 문젠데 왜 오류나는지 모르겠다
    return jsonify({'remaining_items': remaining})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)