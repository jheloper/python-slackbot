import requests
import xml.etree.ElementTree as Et
import json
from datetime import datetime, date, timedelta


# sercet file read, this file content is api token, key, and other secrets...
secrets = open('../secret.json')
secrets_data = json.loads(secrets.read())
NAVER_API_CLIENT_ID = secrets_data.get('NAVER_API_CLIENT_ID')
NAVER_API_CLIENT_SECRET = secrets_data.get('NAVER_API_CLIENT_SECRET')
PUBLIC_KMA_API_KEY = secrets_data.get('PUBLIC_KMA_API_KEY')
secrets.close()

city_xy = open('../city_xy.json', 'r', encoding='utf-8')
CITY_XY = json.loads(city_xy.read())
city_xy.close()

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
def search_weather(city_str):
    tu = (23, 20, 17, 14, 11, 8, 5, 2)
    base_time = None
    fcst_time = None
    base_date = None
    fcst_date = None

    for i in range(len(tu)):
        if datetime.today().hour == tu[i] and datetime.today().minute > 30:
            base_time = tu[i]
            break
        elif datetime.today().hour > tu[i]:
            base_time = tu[i]
            break

    if base_time > 19:
        base_date = datetime.today()
        fcst_date = datetime.today() + timedelta(days=1)
        if base_time == 20:
            fcst_time = '0000'
        elif base_time == 23:
            fcst_time = '0300'
    elif base_time < 10:
        base_time = '0' + str(base_time)
        base_date = datetime.today()
        fcst_date = datetime.today()
        fcst_time = str(tu[i] + 4) + '00'
    else:
        base_date = datetime.today()
        fcst_date = datetime.today()
        fcst_time = str(tu[i] + 4) + '00'

    base_date = str(base_date.year) + str(base_date.month) + str(base_date.day)
    fcst_date = str(fcst_date.year) + str(fcst_date.month) + str(fcst_date.day)
    base_time = str(base_time) + '00'

    params = {'base_date': base_date, 'base_time': base_time, 'nx': CITY_XY.get(city_str).get('nx'),
              'ny': CITY_XY.get(city_str).get('ny'), '_type': 'json', 'numOfRows': '30'}
    headers = {'Content-Type': 'application/json'}
    res = requests.get('http://newsky2.kma.go.kr/service/SecndSrtpdFrcstInfoService2/ForecastSpaceData?ServiceKey=' +
                       PUBLIC_KMA_API_KEY, params=params, headers=headers)
    res_list = res.json().get('response').get('body').get('items').get('item')
    dic = {}

    for item in res_list:
        categoty_value = item.get('category')
        fcst_time_value = str(item.get('fcstTime'))
        fcst_date_value = str(item.get('fcstDate'))
        if categoty_value in ['POP', 'R06', 'S06', 'T3H'] \
                and fcst_time_value == fcst_time and fcst_date_value == fcst_date:
            dic[categoty_value] = item.get('fcstValue')
        elif categoty_value == 'PTY' and fcst_time_value == fcst_time and fcst_date_value == fcst_date:
            if item.get('fcstValue') == 0:
                dic[categoty_value] = '없음'
            elif item.get('fcstValue') == 1:
                dic[categoty_value] = '비'
            elif item.get('fcstValue') == 2:
                dic[categoty_value] = '비/눈'
            elif item.get('fcstValue') == 3:
                dic[categoty_value] = '눈'
        elif categoty_value == 'SKY' and fcst_time_value == fcst_time and fcst_date_value == fcst_date:
            if item.get('fcstValue') == 1:
                dic[categoty_value] = '맑음'
            elif item.get('fcstValue') == 2:
                dic[categoty_value] = '구름 조금'
            elif item.get('fcstValue') == 3:
                dic[categoty_value] = '구름 많음'
            elif item.get('fcstValue') == 4:
                dic[categoty_value] = '흐림'

    return '{4}시 기준 : [{5}]의 강수확룔은 [{0}%]이며 강수형태는 [{1}]입니다. 예상기온은 [{2}℃]이며 하늘상태는 [{3}]입니다.'\
        .format(dic.get('POP'), dic.get('PTY'), dic.get('T3H'), dic.get('SKY'), fcst_time[:2], city_str)

if __name__ == '__main__':
    print(search_weather('서울'))
    print(search_location('토즈 강남점'))
    print(search_translate('hi, there'))
