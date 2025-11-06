# 🎉 FestaPick

<div align="center">

  <h3>
    🎉 <b>모두가 함께 만들어가는 축제 플랫폼</b> 🎊
  </h3>

  <img 
    src="https://github.com/user-attachments/assets/f1c3b239-52a7-4329-accf-f17bb096b77e" 
    alt="FestaPick_hero_image" 
    width="60%" 
  />

  <br/>

  <!-- Custom Website Badge -->
  <a href="https://www.festapick.com">
    <img 
      src="https://img.shields.io/badge/Website-FestaPick-FF6B00?style=for-the-badge&logoColor=white" 
      alt="Website - FestaPick" 
    />
  </a>

  <p>
    <b>
      <a href="https://www.notion.so/FestaPick-2a33ff5fbfc78001b4f0d3f4a33f87a0" target="_blank">
        FestaPick 가이드북
      </a>
    </b>
  </p>

</div>

## 소개
FestaPick은 **축제 참여자**와 **축제 관리자(주최측)** 모두가 함께 쓰는 플랫폼입니다.  

- 💬 축제별 채팅방을 통해 참여자 간 정보 공유
- 🧭 여행 MBTI 입력으로 사용자 맞춤 축제 추천
- 📝 간편한 축제 등록 및 관리 지원
- 📢 공지사항 기능을 통한 빠른 정보 전달

---

## 핵심 기능

### 👤 사용자 기능

#### 🎯 성향 기반 축제 맞춤 추천  
<p>
  <img src="https://github.com/user-attachments/assets/36242224-b7eb-495c-8c09-ef2c9dbf77c9" alt="성향 추천 1" width="200" />
</p>

- 지도에 있는 픽픽(PickPick)을 선택해 지역을 설정하고, 여행 MBTI를 입력하면 사용자의 성향에 맞는 축제를 추천받을 수 있습니다.  
- 추천받은 축제 중 마음에 드는 축제를 클릭하면 상세 정보를 조회할 수 있습니다.  

#### ❤️ 좋아요 / 리뷰 작성  
<p>
  <img src="https://github.com/user-attachments/assets/08948c0b-01f2-46c9-a625-bf34e61ddccb" alt="좋아요/리뷰" width="200" />
</p>

- 마음에 드는 축제는 좋아요를 눌러 저장할 수 있습니다.  
- 다녀온 축제에 대해서는 리뷰를 작성해 다른 사용자와 경험을 공유할 수 있습니다.
  
#### 💬 채팅 / 채팅 알람 기능  
<p>
  <img src="https://github.com/user-attachments/assets/84806e0d-bbd9-415b-8206-aa160b995829" alt="채팅 1" width="180" />
  <img src="https://github.com/user-attachments/assets/1706acdc-b6fc-482c-9df0-563fde81d03a" alt="채팅 2" width="180" />
</p>

- 각 축제별 채팅방에서 참여자들과 실시간으로 정보를 공유할 수 있습니다.  
- 마이페이지에서는 참여 중인 채팅방의 알림 여부를 확인할 수 있습니다.  

### 🧩 관리자 기능

#### 🧑‍💼 축제 관리자 등업 신청  
<p>
  <img src="https://github.com/user-attachments/assets/92c33993-3595-4701-a4ac-5774093dc4da" alt="관리자 등업 신청" width="200" />
</p>

- 축제를 직접 관리하고 싶다면 관리자 등업을 신청할 수 있습니다.  
- 신청 시 소속 정보와 관련 서류를 제출합니다.  
- Admin 승인 후 등업 여부가 결정됩니다.

#### 🛂 등록된 축제에 대한 관리자 신청  
<p>
  <img src="https://github.com/user-attachments/assets/2e20b0f3-0989-4b2e-b5a2-444f1a8fd892" alt="나의 축제 등록" width="200" />
</p>

- 관광공사(TourAPI)에 등록된 축제에 대해 관리자 권한을 신청할 수 있습니다.  
- Admin 승인 후, 해당 축제에 대한 수정·삭제·공지사항 등록 권한을 획득합니다.  

#### 📝 나의 축제 등록하기  
<p>
  <img src="https://github.com/user-attachments/assets/f4d85b13-0e71-4d09-bfce-fbd2a0a5bcd5" alt="기존 축제 관리자 신청" width="200" />
</p>

- 축제 관리자는 새로운 축제를 등록할 수 있습니다.  
- 등록된 축제는 Admin의 승인 후 일반 사용자에게 노출됩니다.  

#### 🗂️ 등록 축제 관리  
<p>
  <img src="https://github.com/user-attachments/assets/b27bd4a4-3e6f-4822-af47-f3a5baa95baa" alt="등록 축제 관리" width="200" />
</p>

- 자신이 등록한 축제에 대해 공지사항을 등록할 수 있습니다.  
- 축제 정보를 수정 및 삭제할 수 있습니다.  

---

## 모니터링
#### 🔎 ELK(ElasticSearch, Logstash, Kibana), Filebeat를 활용한 로그 모니터링
<img width="2926" height="1202" alt="image" src="https://github.com/user-attachments/assets/fc873a53-5af8-4f0f-a025-ec43984f9217" />

- 로그를 직접 서버 인스턴스에 접속해서 확인하는게 아닌 전문 검색을 통해서 로그를 확인할 수 있습니다.
- 예외가 발생한 REQUEST/RESPONSE에 대해서는 UUID를 저장한 로그를 남겨 어떤 엔드포인트에서 어떤 예외가 발생했는지 확인할 수 있습니다.

#### 📊 Prometheus, Grafana를 활용한 메트릭 모니터링
<img width="1468" height="805" alt="스크린샷 2025-11-06 오후 11 06 46" src="https://github.com/user-attachments/assets/983bea0c-1ac4-4cef-97d5-97b059dacffb" />

- Prometheus를 통해 Spring Boot 서버의 메트릭을 수집하고 Grafana를 통해서 시각화하여 대시보드를 제공합니다.

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

### 2025 11 05 수정

- api 불러오기 기능 수정
- 텍스트 기반으로 빠른 응답 기능 추가

---

## 시스템 아키텍쳐

<img width="2614" height="1470" alt="Group 82" src="https://github.com/user-attachments/assets/87624179-0cde-4bed-b789-e3fd031770c8" />


## ERD

<div align="center">

<img src="https://github.com/user-attachments/assets/e7ba25ba-68ce-4be3-a3a4-6be5d4b5099b" alt="ERD" width="800" />

<table width="800" align="center">
  <thead>
    <tr>
      <th><b>엔티티(Entity)</b></th>
      <th><b>설명(Description)</b></th>
    </tr>
  </thead>
  <tbody>
    <tr><td><b>ChatMessage</b></td><td>사용자가 보낸 채팅 메시지를 저장합니다.</td></tr>
    <tr><td><b>ChatParticipant</b></td><td>사용자가 어느 채팅방에 들어갔는지, 채팅방의 채팅을 어디까지 읽었는지 저장합니다.</td></tr>
    <tr><td><b>ChatRoom</b></td><td>각 축제별 채팅방 정보를 저장합니다.</td></tr>
    <tr><td><b>Festival</b></td><td>축제에 대한 상세 정보를 저장합니다.</td></tr>
    <tr><td><b>FestivalNotice</b></td><td>축제 관리자(Festival Manager)가 작성한 공지사항을 저장합니다.</td></tr>
    <tr><td><b>FestivalPermission</b></td><td>축제(TourAPI를 통해 등록된 축제)에 대한 관리 신청서를 저장합니다.</td></tr>
    <tr><td><b>FMPermission</b></td><td>축제 관리자(Festival Manager) 신청서를 저장합니다.</td></tr>
    <tr><td><b>RecommendationHistory</b></td><td>사용자가 가장 최근에 받았던 AI 추천 내역을 저장합니다.</td></tr>
    <tr><td><b>Review</b></td><td>사용자가 등록한 축제의 리뷰를 저장합니다.</td></tr>
    <tr><td><b>users</b></td><td>사용자 정보를 저장합니다.</td></tr>
    <tr><td><b>Wish</b></td><td>사용자의 축제 좋아요 기록을 저장합니다.</td></tr>
  </tbody>
</table>

</div>




## 팀원 소개

<div align="center">
  <table>
    <thead>
      <tr>
        <th style="text-align:center;">이진원</th>
        <th style="text-align:center;">이윤재</th>
        <th style="text-align:center;">주연학</th>
        <th style="text-align:center;">하석현</th>
        <th style="text-align:center;">문수호</th>
        <th style="text-align:center;">심영찬</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td align="center"><img src="https://github.com/jinwon1234.png" width="150" height="150" alt="이진원"></td>
        <td align="center"><img src="https://github.com/YUNJAEGOONER.png" width="150" height="150" alt="이윤재"></td>
        <td align="center"><img src="https://github.com/jyhyt1567.png" width="150" height="150" alt="주연학"></td>
        <td align="center"><img src="https://github.com/studyhard01.png" width="150" height="150" alt="하석현"></td>
        <td align="center"><img src="https://github.com/dib3474.png" width="150" height="150" alt="문수호"></td>
        <td align="center"><img src="https://github.com/skybluesharkk.png" width="150" height="150" alt="심영찬"></td>
      </tr>
      <tr>
        <td align="center">BE</td><td align="center">BE</td><td align="center">BE</td>
        <td align="center">AI</td><td align="center">FE</td><td align="center">FE</td>
      </tr>
      <tr>
        <td align="center"><a href="https://github.com/jinwon1234">GitHub</a></td>
        <td align="center"><a href="https://github.com/YUNJAEGOONER">GitHub</a></td>
        <td align="center"><a href="https://github.com/jyhyt1567">GitHub</a></td>
        <td align="center"><a href="https://github.com/studyhard01">GitHub</a></td>
        <td align="center"><a href="https://github.com/dib3474">GitHub</a></td>
        <td align="center"><a href="https://github.com/skybluesharkk">GitHub</a></td>
      </tr>
    </tbody>
  </table>
</div>
