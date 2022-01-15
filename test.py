from flask import Flask, request, jsonify, render_template
# JWT 확장 라이브러리 임포트하기
from flask_jwt_extended import *

app = Flask(__name__)

# 토큰 생성에 사용될 Secret Key를 flask 환경 변수에 등록
app.config.update(
			DEBUG = True,
			JWT_SECRET_KEY = "I'M IML"
		)

# JWT 확장 모듈을 flask 어플리케이션에 등록
jwt = JWTManager(app)
admin_id = "1234"
admin_pw = "qwer"

@app.route("/")
def test_test():
	return "<h1>Hello, I'm IML!</h1>"


@app.route("/login", methods=['POST'])
def login_proc():
	# 클라이언트로부터 요청된 값
	input_data = request.get_json()
	user_id = input_data["id"]
	user_pw = input_data["pw"]

	# 아이디, 비밀번호가 일치하는 경우
	if (user_id == admin_id and
			user_pw == admin_pw):
		return jsonify(
			result="success",
			# 검증된 경우, access 토큰 반환
			access_token=create_access_token(identity=user_id,
											 expires_delta=False)
		)

	# 아이디, 비밀번호가 일치하지 않는 경우
	else:
		return jsonify(
			result="Invalid Params!"
		)

@app.route('/user_only', methods=["GET"])
@jwt_required()
def user_only():
	cur_user = get_jwt_identity()
	if cur_user is None:
		return "User Only!"
	else:
		return "Hi!," + cur_user

@app.route('/login2', methods=['POST'])
def login2():
	if not request.is_json:
		return jsonify({"msg": "Missing JSON in request"}), 400

	username = request.json.get('username')
	password = request.json.get('password')
	if not username:
		return jsonify({"msg": "Missing username parameter"}), 400
	if not password:
		return jsonify({"msg": "Missing password parameter"}), 400

	if username != 'test' or password != 'test':
		return jsonify({"msg": "Bad username or password"}), 401

	# Identity can be any data that is json serializable
	access_token = create_access_token(identity=username)
	return jsonify(access_token=access_token), 200

# Protect a view with jwt_required, which requires a valid access token
# in the request to access.
@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
	# Access the identity of the current user with get_jwt_identity
	current_user = get_jwt_identity()
	return jsonify(logged_in_as=current_user), 200

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)