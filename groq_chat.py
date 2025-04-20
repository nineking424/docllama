import os
import sys
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import argparse
from datetime import datetime

# .env 파일 로드
load_dotenv()

# API 키 설정
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY 환경 변수를 설정해주세요.")

# 기본 모델 설정
DEFAULT_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

def read_file_content(file_path):
    """
    파일의 내용을 읽어오는 함수
    
    Args:
        file_path (str): 파일 경로
        
    Returns:
        str: 파일 내용 또는 None (오류 발생 시)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"파일을 읽는 중 오류가 발생했습니다: {e}")
        return None

def detect_file_type(file_path):
    """
    파일 확장자를 기반으로 파일 유형 감지
    
    Args:
        file_path (str): 파일 경로
        
    Returns:
        str: 파일 유형 (python, javascript, java, etc.)
    """
    extension = file_path.split('.')[-1].lower()
    extension_map = {
        'py': 'Python',
        'js': 'JavaScript',
        'ts': 'TypeScript',
        'java': 'Java',
        'c': 'C',
        'cpp': 'C++',
        'cs': 'C#',
        'go': 'Go',
        'rb': 'Ruby',
        'php': 'PHP',
        'swift': 'Swift',
        'kt': 'Kotlin',
        'rs': 'Rust',
        'sh': 'Shell',
        'html': 'HTML',
        'css': 'CSS',
        'md': 'Markdown',
        'json': 'JSON',
        'xml': 'XML',
        'yaml': 'YAML',
        'yml': 'YAML',
        'sql': 'SQL',
        'txt': '텍스트',
    }
    return extension_map.get(extension, '알 수 없음')

def ensure_docs_directory():
    """
    docs 디렉토리가 존재하는지 확인하고, 없으면 생성
    """
    docs_dir = 'docs'
    if not os.path.exists(docs_dir):
        os.makedirs(docs_dir)
        print(f"📁 {docs_dir} 디렉토리를 생성했습니다.")
    return docs_dir

def save_to_markdown(content, file_path):
    """
    생성된 위키 문서를 마크다운 파일로 저장
    
    Args:
        content (str): 마크다운 내용
        file_path (str): 원본 파일 경로
    """
    # docs 디렉토리 확인 및 생성
    docs_dir = ensure_docs_directory()
    
    # 파일 이름에서 확장자를 제거하고 _wiki.md 추가
    file_name = os.path.basename(file_path)
    base_name = os.path.splitext(file_name)[0]
    output_file = os.path.join(docs_dir, f"{base_name}_wiki.md")
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"\n✅ 위키 문서가 성공적으로 저장되었습니다: {output_file}")
    except Exception as e:
        print(f"\n❌ 위키 문서 저장 중 오류 발생: {e}")

def generate_wiki(content, file_path, model_name=DEFAULT_MODEL, save=True):
    """
    위키 문서를 생성하는 함수
    
    Args:
        content (str): 파일 내용
        file_path (str): 파일 경로
        model_name (str): 사용할 모델 이름
        save (bool): 결과를 파일로 저장할지 여부
    """
    print(f"🤖 모델 {model_name}을(를) 사용하여 위키 생성 중...")
    
    chat = ChatGroq(
        temperature=0.2,
        model_name=model_name,
        api_key=api_key,
        max_tokens=4000  # 출력 토큰 수 증가
    )

    file_type = detect_file_type(file_path)
    file_name = os.path.basename(file_path)
    
    system = f"""당신은 최고의 기술 문서 작성자입니다. 
    주어진 {file_type} 코드를 상세히 분석하여 포괄적인 마크다운 형식의 기술 위키 문서를 생성해주세요.
    다음 형식을 따라 최대한 구체적이고 상세하게 작성해주세요:
    
    # {file_name} 분석 문서
    
    *생성일: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
    
    ## 1. 개요
    - 파일의 주요 목적과 핵심 기능에 대한 명확한 설명
    - 이 코드가 어떤 문제를 해결하는지, 어떤 가치를 제공하는지 설명
    - 전체적인 아키텍처 또는 설계 철학 요약
    
    ## 2. 기술 스택
    - 사용된 언어: {file_type}
    - 주요 라이브러리 및 프레임워크
    - 의존성 및 외부 API
    
    ## 3. 주요 구성 요소
    ### 3.1 클래스 및 함수
    각 클래스/함수에 대해:
    - 목적과 역할
    - 입/출력 파라미터
    - 주요 로직 설명
    - 호출 관계 및 상호작용
    
    ### 3.2 데이터 구조
    - 사용된 주요 데이터 구조
    - 데이터 흐름 설명
    
    ## 4. 코드 실행 흐름
    - 주요 실행 경로 설명
    - 조건부 로직 및 분기점
    - 비동기/동시성 처리 방식 (해당되는 경우)
    
    ## 5. 코드 예제
    - 주요 기능 사용 예시
    - 각 예제에 대한 설명과 기대 결과
    
    ```{file_type.lower()}
    // 주요 사용 예시 코드
    ```
    
    ## 6. 구현 세부사항
    - 사용된 알고리즘 설명
    - 성능 최적화 기법
    - 오류 처리 방식
    
    ## 7. 주의사항 및 제한사항
    - 사용 시 주의해야 할 점
    - 알려진 버그나 제한사항
    - 잠재적인 오류 상황과 대처 방법
    
    ## 8. 확장 및 개선 가능성
    - 코드 확장 가능성
    - 개선 가능한 부분
    - 추가 기능 제안
    
    ## 9. 결론
    - 코드의 장점 및 특징 요약
    - 활용 시나리오 제안
    """
    
    human = "{content}"
    prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])
    
    # 결과를 저장할 변수
    full_response = ""
    
    print("\n" + "=" * 50)
    print(f"📄 {file_path} 파일 분석 결과")
    print("=" * 50 + "\n")
    
    # 스트리밍 응답 처리
    chain = prompt | chat
    response = chain.stream({"content": content})
    for chunk in response:
        chunk_content = chunk.content if chunk.content else ""
        full_response += chunk_content
        print(chunk_content, end="", flush=True)
    
    # 결과를 마크다운 파일로 저장
    if save:
        save_to_markdown(full_response, file_path)
    
    return full_response

def parse_arguments():
    """명령줄 인수 파싱"""
    parser = argparse.ArgumentParser(description='파일을 분석하여 위키 문서 생성')
    parser.add_argument('file_path', type=str, nargs='?', help='분석할 파일 경로')
    parser.add_argument('--model', '-m', type=str, default=DEFAULT_MODEL, 
                      help=f'사용할 모델 (기본값: {DEFAULT_MODEL}, .env 파일의 GROQ_MODEL에서 설정 가능)')
    parser.add_argument('--no-save', action='store_true', help='결과를 파일로 저장하지 않음')
    
    return parser.parse_args()

def main():
    """메인 함수"""
    args = parse_arguments()
    
    # 파일 경로가 제공되지 않은 경우 사용자 입력 요청
    file_path = args.file_path
    if not file_path:
        file_path = input("분석할 파일 경로를 입력하세요: ")
    
    # 파일 존재 확인
    if not os.path.exists(file_path):
        print(f"❌ 오류: {file_path} 파일을 찾을 수 없습니다.")
        return
    
    content = read_file_content(file_path)
    if content:
        generate_wiki(
            content=content, 
            file_path=file_path, 
            model_name=args.model,
            save=not args.no_save
        )

if __name__ == "__main__":
    main()