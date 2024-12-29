# 프로젝트 이름

프로젝트에 대한 간단한 설명을 작성하세요. 이 프로젝트는 무엇을 해결하고자 하는지, 어떤 기능을 제공하는지에 대한 내용을 포함해야 합니다.

## 목차
1. [소개](#소개)
2. [설치 방법](#설치-방법)
3. [사용 방법](#사용-방법)
4. [기여](#기여)
5. [라이센스](#라이센스)

## 소개

이 프로젝트는 데이터베이스의 DDL 변경 사항을 관리하는 자동화된 시스템입니다. Git과 SQLAlchemy를 활용하여 데이터베이스 구조 변경을 추적하고 GitHub 저장소에 자동으로 커밋합니다. 또한, OpenAI API를 사용하여 DDL 변경 사항에 대한 설명을 자동으로 생성하고 커밋 메시지에 반영합니다.

## 설치 방법

1. **필수 패키지 설치**

   프로젝트에 필요한 패키지를 설치하려면 `requirements.txt` 파일을 사용합니다. 아래 명령어로 설치하세요:
   
   ```bash
   pip install -r requirements.txt

2. **환경 변수 설정**

프로젝트에 필요한 환경 변수를 .env 파일에 설정합니다. .env 파일은 아래와 같은 내용을 포함해야 합니다:

```env
DB_URL=your_database_url
GIT_REPO_PATH=your_local_git_repo_path
GITHUB_REPO_URL=your_github_repository_url
OLLAMA_API_URL=your_ollama_api_url
DDL_CHANGE_LOG_DIR=your_ddl_change_log_directory
```
환경 변수의 의미는 아래와 같습니다:

- DB_URL: 연결할 데이터베이스의 URL (예: mysql://username:password@localhost/dbname)
- GIT_REPO_PATH: 로컬 Git 저장소 경로
- GITHUB_REPO_URL: GitHub 원격 저장소 URL
- OLLAMA_API_URL: OpenAI API와 호환되는 Ollama API URL
- DDL_CHANGE_LOG_DIR: DDL 변경 로그를 저장할 디렉토리 경로

3. **사용 방법**

데이터베이스 DDL 가져오기

프로젝트는 SQLAlchemy를 사용하여 데이터베이스에서 현재 DDL을 가져옵니다. get_current_ddl() 함수를 호출하여 현재 DDL을 가져올 수 있습니다.

DDL 변경 사항 추적 및 커밋

프로젝트는 DDL 변경 사항을 추적하고 GitHub 저장소에 자동으로 커밋합니다. 변경된 DDL을 비교하고, OpenAI API를 사용하여 DDL 변경 사항에 대한 설명을 추가한 후 GitHub에 커밋합니다.

```bash
python your_script.py
```
OpenAI API 사용

DDL 변경 사항에 대한 설명은 OpenAI API를 호출하여 생성됩니다. OLLAMA_API_URL을 사용하여 OpenAI 호환 API를 호출하고, 변경 사항에 대한 텍스트 설명을 가져옵니다.

4. **기여**
이 프로젝트에 기여하고 싶다면, 먼저 fork 후 pull request를 보내주세요. 기여 방법에 대해 궁금한 점이 있다면 이슈를 생성해 주세요.

5. **라이센스**
이 프로젝트는 MIT 라이센스 하에 배포됩니다.