from app import *

#JWT 시크릿 키
secret = 'MakingChallenge'

#JWT 해싱 알고리즘
algorithm = 'HS256'

#토큰 만료기간
MIN = 10

# encode_jwt = jwt.encode(payload, secret, algorithm)
# decode_jwt = jwt.decode(encode_jwt, secret, algorithm)