from urllib.request import urlopen
from bs4 import BeautifulSoup as BS
from urllib.parse import quote
import ssl
import requests

url_str = 'https://search.naver.com/search.naver?date_from=&date_option=0&date_to=&dup_remove=1&nso=&post_blogurl=&post_blogurl_without=&query='
url_page = '&sm=tab_pge&srchby=all&st=sim&where=post&start='

# 사용자가 입력한 검색어에 대한 블로그 조회
def call_sch_url(keyword, start, stop):
    for i in range(start, stop, 10):
        url = url_str + quote(keyword) + url_page + str(i)

        context = ssl._create_unverified_context()
        html = urlopen(url, context=context)
        bs_obj = BS(html, "html.parser")

        scr_htm = bs_obj.find('ul', {'class': 'type01'})

        href_htm = scr_htm.find_all('dt')
        for hhtm in href_htm:
            href = hhtm.find('a')
            link_txt = href['href'].replace('?Redirect=Log&logNo=', '/')
            links.append(link_txt)
            #print(link_txt)


# 검색 후 페이지 텍스트 추출 및 저장
def call_url_text(links):
    for url in links:
        #print(url)
        html = requests.get(url)
        sub_temp = BS(html.text, "html.parser")
        # print(soup_temp)
        order_temp = sub_temp.find(id='screenFrame')

        if order_temp != None:
            ss_url = order_temp.get('src')
            res = urlopen(ss_url)
            sub_temp = BS(res, 'html.parser')
        area_temp = sub_temp.find(id='mainFrame')
        # print(area_temp)
        url_2 = area_temp.get('src')
        # print(url_2)

        url = "https://blog.naver.com" + url_2
        res = urlopen(url)
        soup = BS(res, 'html.parser')
        # print(soup)

        texts = soup.find_all('div', {'class': 'se-module se-module-text'})
        if len(texts) != 0:
            call_txt_prn(texts)

    f.close()
    print('작업이 종료되었습니다.')
    # print(text_prn)


def call_txt_prn(texts):
    for prn in texts:
        txt = prn.text.replace('\u200b', '')
        txt = txt.replace('\xa0\n', '')
        txt = txt.replace('\n\n', '')

        if txt != '':
            f.write(txt + '\n')
            # text_prn.append(txt+"\n")
            # print(txt)
    f.write('\n\n')
    # print('============================================')


keyword = input('검색어를 입력하세요 : ')
f = open('' + keyword + '.txt', 'w', encoding='utf-8')

links = []
call_sch_url(keyword, 1, 10)
call_url_text(links)