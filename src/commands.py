import requests
import xml.etree.ElementTree as Et
import json

# sercet file read, this file content is api token, key, and other secrets...
secrets = json.loads(open('../secret.json').read())

NAVER_API_CLIENT_ID = secrets['NAVER_API_CLIENT_ID']
NAVER_API_CLIENT_SECRET = secrets['NAVER_API_CLIENT_SECRET']
PUBLIC_KMA_API_KEY = secrets['PUBLIC_KMA_API_KEY']


def test_api():
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


# 네이버 지도 검색 결과.
def search_location(location):
    url = 'http://map.naver.com/?query=' + requests.utils.quote(location) + '&type=SITE_1'
    return url


# 구글 번역 결과.
def search_translate(source_str):
    url = 'https://translate.google.co.kr/?hl=ko&tab=wT#en/ko/' + requests.utils.quote(source_str)
    return url


# 공공데이터 초단기예보 조회 결과.
def search_weather():
    print(PUBLIC_KMA_API_KEY)
    params = {'ServiceKey': PUBLIC_KMA_API_KEY, 'base_date': '20161026', 'base_time': '1230', 'nx': '1', 'ny': '1'}
    headers = {'Content-Type': 'application/xml'}
    res = requests.get('http://newsky2.kma.go.kr/service/SecndSrtpdFrcstInfoService2/ForecastTimeData', params=params, headers=headers)
    print(res.url)
    print(res.headers)
    print(res.content)

# search_weather()
# print(search_location('토즈 강남점'))
# print(search_translate('hi, there'))
