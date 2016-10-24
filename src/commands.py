import requests
import xml.etree.ElementTree as Et

NAVER_API_CLIENT_ID = 'z4SmZil0RYHCtsqQk8QP'
NAVER_API_CLIENT_SECRET = 'WT5IKiNKO_'


def test():
    # NAVER 지역 검색 API를 통해 특정 장소의 위치 알아내기

    query = {'query': '토즈 강남점', 'display': 5}
    headers = {'X-Naver-Client-Id': NAVER_API_CLIENT_ID, 'X-Naver-Client-Secret': NAVER_API_CLIENT_SECRET}
    res = requests.get('https://openapi.naver.com/v1/search/local.xml', params=query, headers=headers)
    res_content = res.content.decode()
    print(res_content)

    xml = Et.fromstring(res_content)
    items = xml.findall('./channel/item')
    print(items)

    for i in items:
        print(i.find('title').text)
        print(i.find('category').text)
        print(i.find('description').text)
        print(i.find('link').text)


def view_map(word):
    query = {'query': '토즈 강남점', 'type': 'SITE_1'}
    url = 'http://map.naver.com'
    res = requests.get('http://map.naver.com/?query=%ED%86%A0%EC%A6%88+%EA%B0%95%EB%82%A8%EC%A0%90&type=SITE_1')
    print(res.content)

view_map('')
