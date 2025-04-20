# 코드 분석 위키 생성기

*Last updated: 2024-04-21*

## 소개

이 프로젝트는 코드 파일을 분석하여 상세한 기술 위키 문서를 자동으로 생성하는 도구입니다. Groq API와 LangChain을 활용하여 코드의 구조, 기능, 아키텍처를 이해하기 쉽게 문서화합니다. 개발자가 새로운 코드베이스를 빠르게 이해하거나, 프로젝트 문서화를 자동화하는 데 유용합니다.

## 주요 기능

- 다양한 프로그래밍 언어 파일 분석 지원 (Python, JavaScript, TypeScript, Java 등 20+ 언어)
- 마크다운 형식의 포괄적인 기술 문서 생성
- 코드의 구조, 클래스, 함수에 대한 상세 설명 
- 자동 문서 저장 및 관리 (`docs` 폴더에 자동 저장)
- 환경 변수를 통한 모델 선택 및 설정
- 명령줄 인터페이스를 통한 간편한 사용

## 설치 방법

1. Python 3.12 이상 설치
2. 의존성 설치:

```bash
pip install langchain-groq langchain-core python-dotenv
```

3. Groq API 키 설정:
   - [Groq](https://console.groq.com/) 계정 생성 및 API 키 발급
   - `.env` 파일을 프로젝트 루트에 생성하고 다음 내용 추가:

```bash
GROQ_API_KEY=your_api_key_here
GROQ_MODEL=meta-llama/llama-4-scout-17b-16e-instruct  # 사용할 모델 지정
```

## 사용 방법

### 기본 사용법

```bash
python groq_chat.py 분석할_파일.py
```

### 특정 모델 사용

```bash
python groq_chat.py 분석할_파일.py --model llama-3.1-8b-instant
```

### 결과 저장 없이 출력만 보기

```bash
python groq_chat.py 분석할_파일.py --no-save
```

### 대화형 모드

```bash
python groq_chat.py  # 파일 경로를 입력받는 대화형 모드
```

## 지원 모델

Groq API에서 제공하는 다양한 모델을 사용할 수 있습니다:

- `llama-3.1-8b-instant`: 빠른 응답속도, 가벼운 분석에 적합
- `meta-llama/llama-4-scout-17b-16e-instruct`: 더 상세하고 정확한 분석 결과 (기본값)
- 그 외 Groq 지원 모델 ([Groq 가격 정책](https://groq.com/pricing/) 참조)

## 생성되는 문서 구조

생성된 위키 문서는 다음과 같은 구조로 작성됩니다:

1. **개요**: 파일의 주요 목적과 핵심 기능 설명
2. **기술 스택**: 사용된 언어, 라이브러리, 의존성
3. **주요 구성 요소**: 클래스/함수의 역할, 파라미터, 관계 설명
4. **코드 실행 흐름**: 메인 로직 및 분기점 설명
5. **코드 예제**: 주요 사용 예시
6. **구현 세부사항**: 알고리즘, 성능 최적화, 오류 처리
7. **주의사항 및 제한사항**: 사용 시 주의점, 알려진 이슈
8. **확장 및 개선 가능성**: 향후 개발 방향 제안
9. **결론**: 코드의 장점 및 활용 시나리오

## 프로젝트 구조

```
.
├── groq_chat.py         # 메인 스크립트
├── .env                 # 환경 변수 설정
├── docs/                # 생성된 위키 문서 저장 디렉토리
│   └── *.md             # 생성된 마크다운 문서들
└── README.md            # 이 문서
```

## groq_chat.py 상세 설명

`groq_chat.py`는 이 프로젝트의 핵심 스크립트로, 다음과 같은 주요 기능을 제공합니다:

1. **파일 분석**: 다양한 파일 형식 감지 및 내용 분석
2. **문서 생성**: LLM을 활용한 고품질 마크다운 문서 생성
3. **문서 저장**: `docs` 폴더에 자동 저장 기능

### 주요 함수

- `read_file_content()`: 파일 내용을 읽어옵니다.
- `detect_file_type()`: 파일 확장자를 기반으로 프로그래밍 언어를 감지합니다.
- `ensure_docs_directory()`: 문서 저장용 디렉토리를 생성합니다.
- `save_to_markdown()`: 생성된 문서를 마크다운 파일로 저장합니다.
- `generate_wiki()`: 위키 문서 생성의 핵심 함수로, LLM을 활용해 문서를 생성합니다.
- `parse_arguments()`: 명령줄 인수를 파싱합니다.
- `main()`: 프로그램의 진입점으로 전체 실행 흐름을 관리합니다.

### 환경 설정

- `.env` 파일에서 API 키와 모델 이름을 로드합니다.
- 명령줄 인수로 설정을 재정의할 수 있습니다.

### 문서 템플릿

문서는 구조화된 템플릿을 따라 생성됩니다:
- 파일명과 생성 날짜 헤더
- 9개의 주요 섹션으로 구성된 상세 분석
- 코드 예제 및 구현 설명
- 주의사항 및 향후 개선 가능성

## 라이센스

MIT 라이센스

## 기여하기

1. 이 저장소를 포크합니다.
2. 새 기능 브랜치를 생성합니다 (`git checkout -b feature/amazing-feature`).
3. 변경사항을 커밋합니다 (`git commit -m 'Add some amazing feature'`).
4. 브랜치를 푸시합니다 (`git push origin feature/amazing-feature`).
5. Pull Request를 생성합니다.

## 문의하기

프로젝트에 관한 질문이나 제안이 있으시면 이슈를 생성해주세요.
