# Team14_AI


### 인공지능 기반 축제 조회 API

- fastAPI 활용

### 예시

GET

```
http://127.0.0.1:8000/festivals/random?limit=5
```
(limit : 축제 조회 제한 개수)

RETURN

```
[
    {
        "id": 31,
        "contentId": "2490376",
        "title": "겸재문화예술제",
        "areaCode": 1,
        "addr1": "서울특별시 강서구 양천로 291 (마곡동)",
        "addr2": "",
        "startDate": "2025-05-10",
        "endDate": "2025-05-10",
        "homePage": "https://www.gangseo.seoul.kr/munhwa/mh010204",
        "imageUrl": "http://tong.visitkorea.or.kr/cms/resource/49/3495349_image2_1.jpg",
        "overView": "겸재의 향기, 강서를 물들이다 <제9회 겸재문화예술제> 5월 10일, 강서구 대표 봄 축제인 겸재문화예술제가 마곡 어울림공원에서 개최된다. 올해로 20회를 맞은 겸재전국사생대회와 어린이부터 어르신까지 남녀노소 누구나 참여할 수 있는 다채로운 프로그램과 문화예술공연,  다양한 전시까지 겸재문화예술제에서 만나볼 수 있다."
    },
    {
        "id": 49,
        "contentId": "3524418",
        "title": "고메 잇 강남 서울야장",
        "areaCode": 1,
        "addr1": "서울특별시 강남구 영동대로 513 (삼성동)",
        "addr2": "코엑스 동측광장",
        "startDate": "2025-08-17",
        "endDate": "2025-08-31",
        "homePage": "no_homepage",
        "imageUrl": "http://tong.visitkorea.or.kr/cms/resource/73/3524373_image2_1.jpg",
        "overView": "도심 한가운데에서 펼치지는 레트로 감성의 F&B 야장 페스티벌 이다. 누구나 쉽게 접근할 수 있는 야외 포차의 매력, 트렌디한 미식문화를 결합한 도심 속 리츄얼 공간이다. MZ 세대와 외국인 방문객이 많은 코엑스 한복판에서, ‘야장’이라는 공간 속에 서울의 정취를 녹아내며, 과거와 현재가 공존하는 도심형 푸드 페스티벌이다."
    },
    {
        "id": 20,
        "contentId": "2755016",
        "title": "강주해바라기 축제",
        "areaCode": 36,
        "addr1": "경상남도 함안군 강주4길 16",
        "addr2": "강주마을",
        "startDate": "2025-06-18",
        "endDate": "2025-07-06",
        "homePage": "https://blog.naver.com/arahaman/223888107268",
        "imageUrl": "http://tong.visitkorea.or.kr/cms/resource/70/3497270_image2_1.jpg",
        "overView": "강주해바라기 축제는 2013년 1회를 시작으로 올해 13회를 맞는다. 18일 오전 11시 축제 시작을 알리는 개막행사를 시작으로 공연과 농특산물 판매, 먹거리마당 등이 다채롭게 펼쳐진다. 강주마을 일원에서 열리는 강주해바라기 축제는 식재면적 총 4만2,500㎡ 규모 내  해바라기와 백일홍, 이색 박터널이 방문객을 맞이한다. 성공적인 축제 개최를 위해 마을 주민들이 힘을 모아 비료살포, 비닐멀칭 등을 통해 해바라기가 잘 자랄 수 있도록 사전작업을 하였으며, 해바라기를 정성스럽게 파종하고 온 힘을 쏟아 재배관리를 하였다. '당신을 기다립니다'와 같은 해바라기의 꽃말과 같이 초여름의 파란 하늘 아래 태양 같이 활짝 핀 수십만 송이의 해바라기가 관람객들을 기다리고 있다."
    },
    {
        "id": 48,
        "contentId": "2667017",
        "title": "고령대가야축제",
        "areaCode": 35,
        "addr1": "경상북도 고령군 대가야로 1216 대가야역사테마관광지",
        "addr2": "",
        "startDate": "2025-03-28",
        "endDate": "2025-03-30",
        "homePage": "https://www.festdgy.com/",
        "imageUrl": "http://tong.visitkorea.or.kr/cms/resource/25/3476725_image2_1.jpg",
        "overView": "대가야의 독특한 역사와 문화를 배우고 즐길 수 있는 차별화된 축제이다.대가야 고도 지정, 고령 대가야 궁성지 해자에서 '대왕 토기' 출도로 강력한 고대왕국임이 입증되고, 문체부 주관 최우수 문화관광축제로 선정되었다."
    },
    {
        "id": 45,
        "contentId": "3329992",
        "title": "계양아라온워터축제",
        "areaCode": 2,
        "addr1": "인천광역시 계양구 아라로 548 (장기동)",
        "addr2": "계양아라온 황어광장",
        "startDate": "2025-07-26",
        "endDate": "2025-07-27",
        "homePage": "https://www.gyeyang.go.kr/open_content/main/bbs/bbsMsgDetail.do?msg_seq=14953&bcd=board_4",
        "imageUrl": "http://tong.visitkorea.or.kr/cms/resource/91/3500291_image2_1.jpg",
        "overView": "\"계양아라온 수변에서 펼쳐지는 체험형 물놀이 축제인 \"계양아라온 워터축제\"가 시작된다. 행사는  7.26.(토) ~ 7.27.(일) 이틀간 계양아라온 황어광장에서 펼쳐지며, 물놀이, 워터슬라이드, 카약, 문화공연, 체험부스, (토)야간영화상영,노마드리딩 등 다채로운 행사가 열릴 예정이다. 물놀이와 카약체험은 사전접수와 현장접수로 나누어 진행하는데 사전접수는 \"해양레저스포츠\" 홈페이지에서 7. 8.(화) ~ 15.(화) 까지 진행되며 사전접수를 신청하면 더욱 편하게 축제를 즐길 수 있다."
    }
]
```


### 텍스트 기반 추천 축제 조회 API

- TfidfVectorizer 활용

### 예시

GET

```
http://127.0.0.1:8000/festivals/recommend
```
출력 동일

### 추천 축제 조회 및 설명 api

GET
```
http://127.0.0.1:8000/festivals/recommend/explain
```

출력 동일 + 유사도 가장 높은 단어


### 2025 10 31 수정

- ai기반 축제 시스템 추가
  POST 입력 예시
```
http://localhost:8000/ai/recommend/model
{
    "areaCode": 6,
    "styles": ["TRENDY", "FOOD", "FUNEXPERIENCE"],
    "isNewPlace": true,
    "isSolo": false,
    "prefersEnjoyment": true,
    "isSpontaneous": false,
    "additionalInfo": "먹거리와 재미가 있는 부산 축제",
    "limit": 5
  }
```
