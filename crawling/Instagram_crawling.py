import pandas as pd
from selenium.webdriver import Chrome
from bs4 import BeautifulSoup as bs
import time
from selenium.webdriver.common.keys import Keys

keyword = str(input('키워드 : '))
#keyword = '메리고키친'

driver = Chrome('./chromedriver')
driver.get("https://www.instagram.com/explore/tags/" + keyword + "/")
time.sleep(20)

#해쉬태그 게시물 갯수
totalCount = driver.find_element_by_class_name('g47SY').text
print('totalCount :', totalCount)

content = []
f=open('./'+keyword+'검색결과.txt','w', encoding='utf-8')

# 최초 도입부분
#첫번째 포스트 클릭
driver.find_element_by_class_name('_9AhH0').click()
time.sleep(3)
soup = bs(driver.page_source,'html.parser')
obj = soup.find('div', class_='C4VMK')
txt=obj.find('span').text
txt=txt.replace('  ','')
f.write(txt+'\n\n')
print(txt)

#두번쨰 포스터 넘기기
driver.find_element_by_xpath('/html/body/div[4]/div[1]/div/div/a').click()
time.sleep(3)
soup = bs(driver.page_source,'html.parser')
obj = soup.find('div', class_='C4VMK')
txt=obj.find('span').text
txt=txt.replace('  ','')
f.write(txt+'\n\n')
print(txt)


#나머지 포스트 값 가져오기
for i in range(0, 10):   #종료값을 증가시키면 더 많은 자료를 얻을 수 있습니다.
    try:
        driver.find_element_by_xpath('/html/body/div[4]/div[1]/div/div/a[2]').click() #두번쨰 포스터 넘기기
        time.sleep(3)
        soup = bs(driver.page_source,'html.parser')
        obj = soup.find('div', class_='C4VMK')
        txt=obj.find('span').text
        txt=txt.replace('  ','')
        f.write(txt+'\n\n')
        #print(txt)
    except :
            print('에러')
            pass

f.close()
driver.close()
print('작업이 종료되었습니다.')