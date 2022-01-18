// 1. 클라이언트에 쿠키 저장
document.cookie = 'access_token=[value]'
docCookies.setItem('access_token', [value]);

// // 2. 쿠키 서버로 보내기
// Access-Control-Allow-Origin: https://example.com
// Access-Control-Allow-Methods: GET, POST, PUT, DELETE
// Access-Control-Allow-Headers: Authorization

// 3. 쿠키 삭제하기
docCookies.removeItem('access_token');