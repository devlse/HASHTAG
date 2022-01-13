from urllib.request import urlopen
from urllib.parse import quote_plus

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

baseUrl = 'https://www.instagram.com/explore/tags/'
plusUrl = input('검색할 키워드를 입력하세요')
# url = baseUrl + plusUrl 
# 만약 plusUrl 그대로 들어가면 input이 합정동이면 
# 아스키값이 아닌 그냥 합정동으로 들어가서 그부분을 치환해서 돌려줘야 함 = quote_plus
url = baseUrl + quote_plus(plusUrl)

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)


driver.get("https://www.instagram.com/accounts/login/" )

instagram_id = "moongirl1148@gmail.com"
instagram_pwd = "tmvkfmxktlaghk" #스파르타심화

id_space = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.NAME, 'username')))
id_space.send_keys(instagram_id)
time.sleep(2)

pwd_space = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.NAME, 'password')))
pwd_space.send_keys(instagram_pwd)
time.sleep(2)

login_button = driver.find_element(By.XPATH,'//*[@id="loginForm"]/div/div[3]/button')
login_button.click()

# 로그인안될때 에러 리턴, 인터넷이 안되거나 할때
time.sleep(2)

save_later_button = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="react-root"]/div/div/section/main/div/div/div/div/button')))
save_later_button.click()

# 처리 안해줘도 링크 잘 옮겨감.
# alert_later_button = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[6]/div/div/div/div[3]/button[2]')))
# alert_later_button.click()

#여기서 함수 끊어주면 좋을 것 같은디 우선 이어서..!
#링크 옮겨도 로그인 상태 유지됨!
driver.get(url)
# search_space = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="react-root"]/div/div/section/nav/div[2]/div/div/div[2]/input')))
# search_space.send_keys(plusUrl)

first_post = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR ,'div.v1Nh3.kIKUG._bz0w')))
first_post.click() #div사이에 공백있으면 .으로 replace -- 이유는 유튭 참고
# 이 first_post가 없을때의 에러 처리 (검색어입력이 잘못되었을때)

# 아래부분은 에러가 떠서 알아봐야할 것 같음

#beautifulsoup이나 urlopen같은 경우에는 read한 다음에 분석했는데
# #selenium은 
# html = driver.page_source
# soup = BeautifulSoup(html)

# #soup, 즉 저 html에서 select를 사용해서 뽑아오기
# insta = soup.select()

while(True):
    pass
# driver.get(url)

# #selenium이 느리기 때문에 driver이 뜨기 전에 page source가 불러와질 수 도 있음
# #그럴 경우를 대비해서 시간 차를 좀 주기
# time.sleep(3)



