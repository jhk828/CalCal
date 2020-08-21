# from urllib.request import urlopen
# from urllib.parse import urlencode,unquote,quote_plus
# import urllib
# import pandas as pd
# from bs4 import BeautifulSoup
#
# # 식품영양성분 서비스 데이터 파싱
#
# # url = endpoint/operation?ServiceKey='서비스키'&numOfRows='가져올행수'
# URL = 'http://apis.data.go.kr/1470000/FoodNtrIrdntInfoService/getFoodNtrItdntList?ServiceKey=YtKyAF9FxF7M4DG2iK3wwuYPN9QOZZ5Gq0UteffbkUIU2wPq8az1Ue6plV6kZQsNB1E4rNv4YcaL60LiXla9vQ%3D%3D&numOfRows=100'
#
# data = urlopen(URL).read()
# soup = BeautifulSoup(data, "html.parser")
# total_count = int(soup.find('totalcount').text) # 총데이터 수 불러오기
#
# # 데이터를 담을 데이터프레임 생성
# df = pd.DataFrame(columns= ['name', 'serving_wt','kcal','carbo','protein','fat','sugars',
#                             'sodium','chol','saturated_fatty_acid','trans_fatty_acid','year','company'])
#
# # 100row 씩 전체 페이지에서 파싱해서 데이터프레임에 담는 코드
# for page in range(1,total_count//100 +2):
#     url = f'{URL}&pageNo={page}'
#     data = urlopen(url).read()
#     soup = BeautifulSoup(data, "html.parser")
#     items = soup.findAll("item")
#     for i, item in enumerate(items):
#              df.loc[i+((page-1)*100)] = [item.desc_kor.text, item.serving_wt.text, item.nutr_cont1.text,
#                         item.nutr_cont2.text, item.nutr_cont3.text, item.nutr_cont4.text, item.nutr_cont5.text,
#                         item.nutr_cont6.text, item.nutr_cont7.text, item.nutr_cont8.text, item.nutr_cont9.text,
#                         item.bgn_year.text, item.animal_plant.text]
#
# df.to_csv('C:/python-Django/food.csv', encoding='cp949')
#
# # 수정
# data = pd.read_csv('C:/python-Django/food.csv', encoding='cp949')
# data1 = data.iloc[:,1:7]
# data1['company'] = data.iloc[:,-1]
# data1.isnull().sum()
# data1['company'] = data1['company'].fillna(' ')
# data1.isnull().sum()
# data2 = data1.dropna()
# data2.to_csv('C:/python-Django/food2.csv', encoding='cp949')

# csv to sqlite3
import sqlite3
import pandas as pd

# load data 경로설정
df = pd.read_csv('food2.csv', encoding='cp949')

# strip whitespace from headers
df.columns = df.columns.str.strip()

con = sqlite3.connect("db.sqlite3")

# drop data into database
df.to_sql("Table", con)

con.close()

# python manage.py inspectdb
# python manage.py inspectdb > models.py 로 저장