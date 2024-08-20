import time
import requests
import pandas
from bs4 import BeautifulSoup


"""變數準備

"""

# 目標網址
target_url = "https://www.ptt.cc/bbs/"

# 目標看板
target_board = "Tech_Job"

#目標頁面
target_page = "/index"

#目標頁數
page_num = ""

#頁面附屬檔名
page_ext = ".html"

target = target_url + target_board + target_page + page_num  + page_ext

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
}

'''
import requests
data = requests.get(target, headers=headers)
print(data.content) 
'''

def download_html(target, headers):
    # data = requests.get(target, headers=headers)
    # return data
    return requests.get(target, headers=headers)

def parser_board_urls(requests_):
    # 傳入request_ 並解析成 bs4 物件
    html_code = BeautifulSoup(requests_.content, features="html.parser")
    div_list = html_code.find_all('div', class_='title')
   
    urls = []
    for div_ in div_list:
        try:
            a_tag = div_.find('a').attrs['href']
        except:
            a_tag = None
        urls.append(a_tag)
    return urls

def parser_article_content(url_list):
    ptt_data = []
    for url_ in url_list:
        if url_ != None:
            article_url = 'https://www.ptt.cc' + url_
            page_data = download_html(article_url, headers)
            page_html_code = BeautifulSoup(page_data.content, features="html.parser")
            try:
                article_data = page_html_code.find_all('span', class_="article-meta-value")
                article_author = article_data[0].contents[0]
                article_title = article_data[2].contents[0]
                article_time = article_data[3].contents[0]
                article_body = page_html_code.find('div', id='main-content').contents[4]
                article_row = {
                    'url': article_url,
                    'title': article_title,
                    'author': article_author,
                    'time': article_time,
                    'content': article_body
                }
                ptt_data.append(article_row)
            except:
                print("parser error:", article_url)
   
    time.sleep(0.5)
    return ptt_data

def export_json(data):
    ptt_df = pandas.DataFrame(data)
    ptt_df.to_json("ptt.json")
    return True


## Test
a = download_html(target, headers)
b = parser_board_urls(a)
c = parser_article_content(b)
export_json(c)
print(c)


