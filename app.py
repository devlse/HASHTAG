from flask import Flask, render_template, jsonify, request, redirect
from datetime import datetime, timedelta
from pytz import timezone
import bcrypt
import jwt
from JWT_info import * #*자리에 secret, algorithm, MIN로 되어있었는데 이러니까 제 컴퓨터에선 오류가 나더라구요 그래서 일단 주석처리합니다
today = datetime.now(timezone('Asia/Seoul'))

app = Flask(__name__)

#크롤링시 필요한 import
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from unittest import result
from urllib.parse import quote_plus
import pandas as pd
import time

###

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbmakingchallenge

#파일 이름 저장용으로 현재 시간 받아오기 및 전역변수 설정
from datetime import datetime
now = datetime.now()
current = now.strftime("%Y%m%H%S%M%d")
file_route = ''

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
            return redirect('/login-page')
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

#검색결과 보여주는 페이지 - 로그인 했을 때
@app.route('/searched-result')
def resultPage():
    return render_template('Result.html')

#검색결과 보여주는 페이지 - 로그아웃 상태
@app.route('/searched-result-logout')
def resultPage_out():
    return render_template('Result_logout.html')

#관심단어 등록 페이지
@app.route('/myword-page')
def mywordPage():
    return render_template('record_list.html')

###


#로그인버튼
@app.route('/login', methods=['POST'])
def login():
    users = list(db.user.find({}, {'_id': False}))
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

#검색어 저장 - 여기에 그냥 크롤링 기능 합침
@app.route('/searchword', methods=['POST'])
def search_post():
    search_word_receive = request.form['searchWord_give']
    if search_word_receive != "":
        doc = {
            'search': search_word_receive
        }
        db.searchword.insert_one(doc)
        crawling(search_word_receive) #실질적인 크롤링
    return jsonify({'msg': '결과 보러가기'})
#crawling - 실질적인 크롤링
def crawling(search_word_receive):
    baseUrl = 'https://www.instagram.com/explore/tags/'
    plusUrl = search_word_receive  # input = 검색어 입력받는 되는 부분.
    # 만약 plusUrl 그대로 들어가면 input이 합정동이면
    # 아스키값이 아닌 그냥 합정동으로 들어가서 그부분을 치환해서 돌려줘야 함 = quote_plus
    url = baseUrl + quote_plus(plusUrl)

    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    service_instance = Service('C:/Users/song/Desktop/pro2/HASHTAG/backend/crawling_machine/chromedriver.exe')  # 상대경로절대경로

    driver = webdriver.Chrome(service=service_instance, options=options)

    driver.get("https://www.instagram.com/accounts/login/")

    instagram_id = "spartasimhwa@gmail.com"
    instagram_pwd = "sparta3" #"tmvkfmxktlaghk"  # 스파르타심화

    id_space = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, 'username')))
    id_space.send_keys(instagram_id)
    time.sleep(2)

    pwd_space = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, 'password')))
    pwd_space.send_keys(instagram_pwd)
    time.sleep(2)

    login_button = driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[3]/button')
    login_button.click()

    # 로그인이 안되거나, 인터넷이 안될때 에러 처리
    time.sleep(2)

    save_later_button = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="react-root"]/section/main/div/div/div/div/button')))
                    #//*[@id="react-root"]/div/div/section/main/div/div/div/div/button 에서 수정됨*****
    save_later_button.click()

    # 여기서 함수 끊어주면 좋을 것 같은디 우선 이어서..!
    # 링크 옮겨도 로그인 상태 유지됨!
    driver.get(url)

    first_post = WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.v1Nh3.kIKUG._bz0w')))
    first_post.click()  # div사이에 공백있으면 .으로 replace -- 이유는 유튭 참고
    # 이 first_post가 없을때의 에러 처리 (검색어입력이 잘못되었을때)

    data = []
    crawl_post_number = 5
    for i in range(crawl_post_number):
        time.sleep(3)
        # hashtag_array = WebDriverWait(driver,10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR , 'a.xil3i')))
        hashtag_array = driver.find_elements(By.CSS_SELECTOR, 'a.xil3i')
        for hashtag in hashtag_array:
            data.append(hashtag.text.replace('#', ''))

        # 다음 포스트로 넘어가기
        next_button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'body > div.RnEpo._Yhr4 > div.Z2Inc._7c9RR > div > div.l8mY4.feth3 > button')))
        next_button.click()

    def convertToCsv(data):
        flag = False
        try:
            data_frame = pd.DataFrame(data)
            data_frame.to_csv('crawled_data.csv', index=False, encoding='utf-8-sig')
            flag = True
            return flag
        except:
            print("csv convert error")
            return flag

    # beautiful soup을 활용해서 데이터를 긁어올 수 있지만
    # 지금같은 경우는 다른 잡다한 정보는 필요없고 오로지 해시태그 정보만 필요해서 Bs4를
    # 활용하지 않을 것.

    driver.quit()

    from wordcloud import WordCloud
    import matplotlib.pyplot as plt
    from collections import Counter

    counts = Counter(data)
    tags = counts.most_common(40)
    label_count = 0

    wordcloud = WordCloud(
        font_path='C:/Users/song/Desktop/pro2/HASHTAG/backend/crawling_machine/Fonts/GmarketSansTTFBold.ttf',  # 상대경로절대경로
        background_color='white',
        width=800,
        height=800
    )
    wc_img = wordcloud.generate_from_frequencies(dict(tags))
    print(dict(tags))
    # fig = plt.figure()
    # plt.imshow(wordcloud, interpolation='bilinear')
    # plt.axis('off')
    # plt.show()
    label_count += 1
    file_route_in = 'C:/Users/song/Desktop/pro2/HASHTAG/static/image/test' + str(
        plusUrl) + current + '.png'  # 상대경로절대경로
    global file_route  # 이미지 주소 저장 위한 전역변수
    file_route = file_route_in  # 전역변수
    wc_img.to_file(file_route_in)

@app.route('/search', methods=['GET'])
def searchaaa():
    word = list(db.searchword.find({}, {'_id': False}))
    global file_route #이미지 경로 받아오기 위함
    return jsonify({'search_word': word, 'image': file_route})


#검색어와 메모 저장
@app.route('/result-save', methods=['POST'])
@check
def saving_memo(id):
    myword_receive = request.form['myword_give'] #검색한 단어
    num_receive = request.form['num_give'] #아이디값 저장
    memo_receive = request.form['memo_give']
    keyword_receive = request.form['keyword_give']
    link_receive = request.form['link_give']
    id = id
    doc = {
        'myword': myword_receive,
        'saving-num': num_receive,
        'memo': memo_receive,
        'keyword': keyword_receive,
        'link': link_receive,
        'image': file_route, #이미지 경로 추가
        'user_id': id
    }
    db.onedaylive.insert_one(doc)
    return jsonify({'msg' : '검색어가 저장되었습니다.'}) #검색어 보여주기

#저장된 단어들 보여줌
@app.route('/searchlist', methods=['GET'])
@check
def record(id):
    searchs = list(db.onedaylive.find({'user_id':id}, {'_id': False}))
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
    remaining = list(db.onedaylive.delete_one({'saving-num': saved_num})) #실행은 되는데 왜 오류나는지 모르겠다
    return jsonify({'remaining_items': remaining})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)