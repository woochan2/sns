import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

base_url = 'http://www.yes24.com/24/category/bestseller'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}

all_books = []

for page in range(1, 43):  # 1~42페이지까지 반복
    params = {'PageNumber': page}
    res = requests.get(base_url, headers=headers, params=params)
    soup = BeautifulSoup(res.text, 'html.parser')
    books = soup.select('li[data-goods-no]')
    if not books:
        break

    for idx, book in enumerate(books, start=1 + (page-1)*24):
        # 책 제목
        title_tag = book.select_one('.gd_name')
        책제목 = title_tag.text.strip() if title_tag else ''
        # 저자
        author_tag = book.select_one('.authPub.info_auth')
        저자 = author_tag.text.strip() if author_tag else ''
        # 출판사
        pub_tag = book.select_one('.authPub.info_pub')
        출판사 = pub_tag.text.strip() if pub_tag else ''
        # 순위
        순위 = str(idx)
        all_books.append([순위, 책제목, 저자, 출판사])
    time.sleep(1)  # 서버 부하 방지

df = pd.DataFrame(all_books, columns=['순위', '책제목', '저자', '출판사'])
df.to_csv('yes24_bestseller_full.csv', encoding='cp949', index=False)
print('CSV 파일 저장 완료!')
