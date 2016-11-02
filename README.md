# Python-Slackbot

### 장고걸스 서울 10월 멜팅팟 세미나에서 공개한 슬랙 봇입니다.

슬라이드 자료 : http://www.slideshare.net/JoongHyeonKim/slackbot-with-python-67873010

### 실행방법
(secret.json -> secrets.py로 변경했습니다.)
프로젝트 루트 경로에 secrets.py 파일에 있는 "SLACK_API_TOKEN", "PUBLIC_KMA_API_KEY"의 내용을 넣어주셔야 합니다. 

`"Your Token"` 부분에는 여러분이 발급 받으신 API 토큰을 넣어주세요!

코드는 계속 개선해나갈 생각입니다. 문제가 있으시면 연락주세요!

src 디렉터리에 있는 echobot.py를 실행하시면 에코봇을, slackbot.py를 실행하시면 3가지 기능(지도, 날씨, 번역)을 구현한 봇을 테스트하실 수 있습니다!