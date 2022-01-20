from unittest import result
from urllib.parse import quote_plus

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service


import pandas as pd
import time

baseUrl = 'https://www.instagram.com/explore/tags/'
plusUrl = input('검색할 키워드를 입력하세요')
# 만약 plusUrl 그대로 들어가면 input이 합정동이면 
# 아스키값이 아닌 그냥 합정동으로 들어가서 그부분을 치환해서 돌려줘야 함 = quote_plus
url = baseUrl + quote_plus(plusUrl)


options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

service_instance = Service('C:/Users/내문서/Desktop/sparta/HASHTAG/backend/crawling_machine/chromedriver.exe')

driver = webdriver.Chrome(service=service_instance, options=options)

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

# 로그인이 안되거나, 인터넷이 안될때 에러 처리
time.sleep(2)

save_later_button = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="react-root"]/div/div/section/main/div/div/div/div/button')))
save_later_button.click()

#여기서 함수 끊어주면 좋을 것 같은디 우선 이어서..!
#링크 옮겨도 로그인 상태 유지됨!
driver.get(url)

first_post = WebDriverWait(driver,15).until(EC.visibility_of_element_located((By.CSS_SELECTOR ,'div.v1Nh3.kIKUG._bz0w')))
first_post.click() #div사이에 공백있으면 .으로 replace -- 이유는 유튭 참고
# 이 first_post가 없을때의 에러 처리 (검색어입력이 잘못되었을때)

data = []
crawl_post_number = 5
for i in range(crawl_post_number):
    time.sleep(3)
    #hashtag_array = WebDriverWait(driver,10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR , 'a.xil3i')))
    hashtag_array = driver.find_elements(By.CSS_SELECTOR , 'a.xil3i')
    for hashtag in hashtag_array:
        data.append(hashtag.text.replace('#',''))

    #다음 포스트로 넘어가기
    next_button = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR , 'body > div.RnEpo._Yhr4 > div.Z2Inc._7c9RR > div > div.l8mY4.feth3 > button')))
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

wordcloud = WordCloud(font_path='C:/Users/내문서/Desktop/sparta/HASHTAG/backend/crawling_machine/Fonts/GmarketSansTTFBold.ttf',
    background_color='white',
    width=800,
    height=800
    )
wc_img = wordcloud.generate_from_frequencies(dict(tags))
print(dict(tags))
#fig = plt.figure()
#plt.imshow(wordcloud, interpolation='bilinear')
#plt.axis('off')
#plt.show()
label_count+=1
wc_img.to_file('C:/Users/내문서/Desktop/sparta/HASHTAG/static/image/test'+str(plusUrl)+'.jpg')
