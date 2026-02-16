# 🍽️ Dinner Bot - 토양체질 저녁 식단 추천봇

매일 **17:30**에 토양체질에 맞는 저녁 식단 5가지를 Telegram으로 추천해주는 봇입니다.

## ✨ 주요 기능

- 🧬 **8체질 의학 기반** 토양체질 맞춤 식단 추천
- 🤖 **Gemini AI** 활용 메뉴 자동 생성
- 📱 **Telegram** 자동 발송 (매일 17:30)
- 📊 **영양 정보** 포함 (칼로리, 탄수화물, 단백질, 지방)
- 📺 **유튜브 레시피 링크** 제공
- ⭐ **난이도별** 5가지 메뉴 (쉬움 → 어려움)
- 🔄 **중복 방지** 최근 30일 히스토리 관리

## ⚙️ 설정

1. `.env.example`을 `.env`로 복사
2. Telegram Bot Token, Chat ID, Gemini API Key 입력

```bash
cp .env.example .env
```

## 🚀 실행

```bash
# 의존성 설치
pip install -r requirements.txt

# 실행
python main.py

# 테스트 (즉시 식단 추천 발송)
python main.py --test
```

## 🚂 Railway 배포

1. GitHub 저장소 연결하여 프로젝트 생성
2. **Variables** 탭에서 아래 환경변수 추가 (필수!):

| 변수명 | 값 예시 | 설명 |
|---|---|---|
| `TELEGRAM_BOT_TOKEN` | `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11` | 텔레그램 봇 토큰 |
| `TELEGRAM_CHAT_ID` | `123456789` | 본인 채팅 ID |
| `GEMINI_API_KEY` | `AIzaSy...` | Gemini API 키 |
| `TIMEZONE` | `Asia/Seoul` | (선택) 타임존 (기본: Asia/Seoul) |
| `MEAL_SEND_HOUR` | `17` | (선택) 발송 시 (0-23) |
| `MEAL_SEND_MINUTE` | `30` | (선택) 발송 분 (0-59) |

## 📁 프로젝트 구조

```
dinner_bot/
├── main.py              # 메인 엔트리포인트
├── config.py            # 설정 관리
├── meal_recommender.py  # Gemini AI 식단 추천 엔진
├── meal_history.py      # 추천 히스토리 관리 (중복 방지)
├── toyang_diet.py       # 토양체질 식생표 데이터
├── telegram_notifier.py # Telegram 알림 발송
├── requirements.txt     # 의존성
├── railway.json         # Railway 배포 설정
├── .env.example         # 환경변수 예시
└── .gitignore
```
