#!/usr/bin/env python
# coding: utf-8

# In[ ]:


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
# df.to_csv('./food.csv', encoding='cp949')

import pandas as pd
import sqlite3

# 수정
data = pd.read_csv('./food.csv', encoding='cp949')
df = data.iloc[:,1:7]
df['year'] = data.iloc[:,-2]
df['company'] = data.iloc[:,-1]

# company 컬럼의 NA 값들을 공백 처리
df['company'] = data['company'].fillna(' ')

# TRACE가 들어간 행 제거
kcal = df['kcal'] == 'TRACE'
carbo = df['carbo'] =='TRACE'
protein = df['protein'] =='TRACE'
fat = df['fat'] =='TRACE'
find = df[kcal|carbo|protein|fat].index
df = df.drop(find)

# df의 NA값 제거 후 인덱스 재설정
df.isnull().sum()
df = df.dropna()
df.reset_index(drop=True, inplace=True)

# 조건에 해당하는 인덱스값들을 찾은 후 제거하여 csv로 저장
index_lst = []
for i in range(len(df)-1):
    if df['name'][i] == df['name'][i+1] :
        if df['year'][i] <= df['year'][i+1]:
            index_lst.append(df.index[i])
        else :
            index_lst.append(df.index[i+1])

df = df.drop(index_lst)
#DataFrame 저장
df.to_csv('./food_table.csv', encoding='cp949', index=False)

df['id'] = [x for x in range(1,len(df)+1)]
df = df[['id', 'name', 'serving_wt', 'kcal', 'carbo', 'protein','fat', 'company']]
conn = sqlite3.connect("db.sqlite3")
cur = conn.cursor()
record = df.values.tolist()
cur.executemany( 'INSERT INTO FoodInfo_table VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                record )
conn.commit()
conn.close()

