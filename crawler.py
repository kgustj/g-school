# 2021 M2 D-lab 수업 실습 — 네이버 쇼핑(2021-05-17), 네이버 영화 평점(2021-05-24) 크롤러
# 현재 대상 사이트 구조가 바뀌어(네이버 영화는 서비스 종료) 동작하지 않음. 기록용.

# ── 1. 네이버 쇼핑 블루투스 스피커 (2021-05-17) ──
import requests
from bs4 import BeautifulSoup

url = 'https://search.shopping.naver.com/search/all?query=%EB%B8%94%EB%A3%A8%ED%88%AC%EC%8A%A4+%EC%8A%A4%ED%94%BC%EC%BB%A4&cat_id=&frm=NVSHATC'
data = requests.get(url)
content = data.content

bs = BeautifulSoup(content, 'html.parser')
ul = bs.find('ul', {'class': 'list_basis'})

# lis = ul.findAll('li', {'class': 'basicList_item__2XT81 ad'})
lit = ul.findAll('li', {'class': 'basicList_item__2XT81'})

print(len(lit))


def parseListItem(li):
    a = li.find('a', {'class': 'basicList_link__1MaTN'})
    title = a['title']
    link = a['href']
    span = li.find('span', {'class': 'price_num__2WUXn'})
    price = span.text.replace(',', '')
    return {'title': title, 'link': link, 'price': price}


print(parseListItem(lit[2]))

items = []

# for li in lis:
#     items.append(parseListItem(li))
for li in lit:
    items.append(parseListItem(li))
for item in items:
    print(item['title'], ',', item['price'], ',', item['link'])

# ── 2. 네이버 영화 평점 순위 (2021-05-24) ──

# URL을 읽어서 HTML를 받아오고,
headers2 = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}
data = requests.get('https://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=pnt&date=20200716', headers=headers2)

# HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
soup = BeautifulSoup(data.text, 'html.parser')

# 선택자 예: #old_content > table > tbody > tr:nth-child(2) > td.point

# select를 이용해서, tr들을 불러오기
movies = soup.select('#old_content > table > tbody > tr')
# movies (tr들) 의 반복문을 돌리기
for movie in movies:
    # movie 안에 a 가 있으면,
    a_tag = movie.select_one('td.title > div > a')
    point = movie.select_one('td.point')
    if a_tag is not None:
        # a의 text를 찍어본다.
        print(a_tag.text, point.text)
