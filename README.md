# HeXA Bootcamp 2024 Backend Track 과제 #1

![Hexa Bootcamp Logo](docs/assets/hexa-bootcamp-logo.png)

헥사 부트캠프 2024 백엔드 트랙에 오신 것을 환영합니다! 
이 과제는 백엔드 트랙의 첫 번째 과제로, 백엔드 개발자로서 기초적인 API 개발 능력을 키우는 것을 목표로 합니다.
아래의 과제 설명을 자세히 읽어 성공적으로 과제를 완수하시기를 바라겠습니다.

## 과제 설명

본 과제에서 여러분은 실생활에서 흔히 볼 수 있는 URL 단축 서비스를 개발합니다.

URL 단축 서비스의 대표적인 예시로는 [Bitly](https://bitly.com/), [TinyURL](https://tinyurl.com/app) 등이 있습니다.

여러분은 수업에서 배운 내용을 활용하여, URL 단축 서비스의 주요 기능들을 REST API로써 구현해야 합니다.
구체적으로, 아래와 같은 기능들을 구현해야 합니다.

### 1. 단축 URL 생성

사용자가 입력한 URL을 단축 URL로 변환합니다.

이 기능은 변환하고자 하는 URL을 입력받아, 
해당 URL에 대한 고유한 슬러그를 생성한 뒤 
URL Shortener가 호스팅되는 서버의 도메인과 결합하여 단축 URL을 생성합니다.

만약 이미 생성된 URL에 대해 단축 URL을 생성하려고 할 경우, 
새로 생성하는 것이 아니라 기존에 생성된 단축 URL을 반환해야 합니다.

> 슬러그란 단축 URL의 경로 부분에 해당하는 문자열을 의미하며, 예를 들어 `http(s)://your-url-shortener.com/abc123`에서 `abc123`이 슬러그에 해당합니다. 자세한 내용은 아래 입출력 예시를 참고하시기 바랍니다.

또한, URL의 형식이 올바르지 않은 경우에는 적절한 에러 메시지를 반환해야 합니다. 자세한 내용은 아래의 엔드포인트 명세를 참고하시기 바랍니다.

#### 엔드포인트 명세

- 엔드포인트 경로: `POST /`
- 요청 데이터: JSON 형식의 객체
  - `url`: 단축하고자 하는 URL
- 응답 데이터: JSON 형식의 객체
  - `original_url`: 요청 시에 입력한 URL
  - `short_slug`: 생성된 단축 URL의 슬러그.
  - `short_url`: 생성된 단축 URL. 서버의 주소와 `short_slug`를 결합하여 생성됩니다.
- 응답 상태 코드:
  - `201 Created`: 단축 URL이 새로 생성된 경우
  - `200 OK`: 이미 생성된 단축 URL을 요청받아 반환하는 경우
  - `400 Bad Request`: 올바르지 않은 형식의 URL이 입력된 경우 (예: `http-misspelled://example.com`)

#### 입출력 예시

아래 입출력 예시에서는 서버의 주소를 `http://localhost:8000`이라고 가정합니다.

##### 요청-1

```bash
POST http://localhost:8000/ HTTP/1.1
Content-Type: application/json

{
  "url": "https://some-very-long-url.com/with/many/segments"
}
```

##### 응답-1

```bash
HTTP/1.1 201 Created
Content-Type: application/json

{
  "original_url": "https://some-very-long-url.com/with/many/segments",
  "short_slug": "abc123",
  "short_url": "http://localhost:8000/abc123"
}
```

##### 요청-2

```bash
POST http://localhost:8000/ HTTP/1.1
Content-Type: application/json

{
  "url": "http-misspelled://example.com"
}
```

##### 응답-2

```bash
HTTP/1.1 400 Bad Request
Content-Type: application/json

{
  "error": "Invalid URL format"
}
```

### 2. 단축 URL 접속

사용자가 [1번 기능](#1-단축-url-생성)에서 생성한 단축 URL로 접속하면, 원래의 URL로 리다이렉트합니다.

만약 단축 URL이 존재하지 않는 경우에는 적절한 에러 메시지를 반환해야 합니다.

#### 엔드포인트 명세

- 엔드포인트 경로: `GET /<slug>`
  - `<slug>`: 단축 URL의 슬러그
- 응답 상태 코드:
  - `308 Permanent Redirect`: 단축 URL이 존재하는 경우
  - `404 Not Found`: 단축 URL이 존재하지 않는 경우

#### 입출력 예시

아래 입출력 예시에서는 서버의 주소를 `http://localhost:8000`이라고 가정합니다.
또한 `https://some-very-long-url.com/with/many/segments`에 대한 단축 URL이 `http://localhost:8000/abc123`이라고 가정하며, 해당 단축 URL 외에 다른 단축 URL은 존재하지 않는다고 가정합니다.

##### 요청-1

```bash
GET http://localhost:8000/abc123 HTTP/1.1
```

##### 응답-1

```bash
HTTP/1.1 308 Permanent Redirect
Location: https://some-very-long-url.com/with/many/segments
```

##### 요청-2

```bash
GET http://localhost:8000/nonexistent-slug HTTP/1.1
```

##### 응답-2

```bash
HTTP/1.1 404 Not Found
Content-Type: application/json

{
  "error": "URL not found"
}
```

### 3. Health Check Endpoint

실제 프로덕션에서 API 서버들은 종종 `/` 경로에 health check 엔드포인트를 만들어 둡니다.
Health Check란 서버가 정상적으로 동작하는지를 확인하는 것으로,
Kubernetes, AWS ELB 등의 로드 밸런서들이 이 엔드포인트를 통해 서버의 상태를 확인합니다.

#### 엔드포인트 명세

- 엔드포인트 경로: `GET /`
- 응답 상태 코드: `200 OK`

## Pre-requisites

본 과제를 수행하기 위해서는 다음의 사항이 필요합니다.

- Python 3.11 이상의 버전
- Github 계정

## 과제 진행

본 과제는 아래와 같은 형식으로 진행해주시기 바랍니다.

### 1. 리포지토리 생성

본 템플릿 리포지토리를 자신의 Github 계정으로 fork합니다.


**리포지토리의 default 브랜치는 `master`로 설정해주시기 바랍니다.** 추후 과제 완료 확인을 위한 Github Action Workflow가 master 브랜치로의 PR로 트리거될 예정입니다.
