import os
import subprocess
from datetime import datetime
from sqlalchemy import create_engine
from dotenv import load_dotenv
import difflib
import requests

# .env 파일 로드
load_dotenv()

# 환경 변수 가져오기
DB_URL = os.getenv("DB_URL")
GIT_REPO_PATH = os.getenv("GIT_REPO_PATH")
OLLAMA_API_URL = os.getenv("OLLAMA_API_URL")
DDL_CHANGE_LOG_DIR = os.path.join(GIT_REPO_PATH, "ddl_changes")

def get_current_ddl(engine):
    """
    현재 데이터베이스의 DDL 가져오기
    """
    ddl = {}
    with engine.connect() as connection:
        tables = connection.execute("SHOW TABLES").fetchall()
        for (table_name,) in tables:
            create_table_sql = connection.execute(f"SHOW CREATE TABLE {table_name}").fetchone()[1]
            ddl[table_name] = create_table_sql
    return ddl

def save_ddl_to_file(version, ddl_content):
    """
    DDL을 파일로 저장
    """
    if not os.path.exists(DDL_CHANGE_LOG_DIR):
        os.makedirs(DDL_CHANGE_LOG_DIR)

    file_name = f"{version}_ddl.sql"
    file_path = os.path.join(DDL_CHANGE_LOG_DIR, file_name)

    with open(file_path, "w", encoding="utf-8") as file:
        for table, ddl in ddl_content.items():
            file.write(f"-- Table: {table}\n")
            file.write(ddl + "\n\n")

    print(f"DDL 저장 완료: {file_path}")
    return file_name

def load_previous_ddl(version):
    """
    이전 버전의 DDL 로드
    """
    file_path = os.path.join(DDL_CHANGE_LOG_DIR, f"{version}_ddl.sql")
    if not os.path.exists(file_path):
        return {}
    ddl = {}
    with open(file_path, "r", encoding="utf-8") as file:
        current_table = None
        for line in file:
            if line.startswith("-- Table:"):
                current_table = line.split(":")[1].strip()
                ddl[current_table] = ""
            elif current_table:
                ddl[current_table] += line
    return ddl

def compare_ddl(previous_ddl, current_ddl):
    """
    DDL 비교
    """
    diff = {}
    for table, current_sql in current_ddl.items():
        previous_sql = previous_ddl.get(table, "")
        if current_sql != previous_sql:
            diff[table] = list(difflib.unified_diff(
                previous_sql.splitlines(), current_sql.splitlines(),
                lineterm='', fromfile="previous", tofile="current"
            ))
    return diff

def generate_commit_message_with_ollama(diff):
    """
    Ollama API를 사용하여 DDL 변경 사항 설명 생성
    """
    prompt = "다음 DDL 변경 사항을 바탕으로 간단한 설명을 작성하세요:\n\n"
    for table, changes in diff.items():
        prompt += f"Table: {table}\n"
        prompt += "\n".join(changes) + "\n\n"

    try:
        response = requests.post(
            OLLAMA_API_URL,
            json={"prompt": prompt},
            timeout=10
        )
        response.raise_for_status()

        result = response.json()
        commit_message = result.get("completion", "").strip()
        print(f"생성된 커밋 메시지: {commit_message}")
        return commit_message
    except requests.RequestException as e:
        print(f"Ollama API 호출 실패: {e}")
        return "DDL 변경 사항 업데이트"

def git_commit_and_push(file_name, commit_message):
    """
    Git 저장소에 변경 사항 추가, 커밋, 푸시
    """
    try:
        # Git add
        subprocess.run(["git", "-C", GIT_REPO_PATH, "add", os.path.join("ddl_changes", file_name)], check=True)

        # Git commit
        subprocess.run(["git", "-C", GIT_REPO_PATH, "commit", "-m", commit_message], check=True)

        # Git push
        subprocess.run(["git", "-C", GIT_REPO_PATH, "push"], check=True)

        print("Git에 변경 사항 커밋 및 푸시 완료")
    except subprocess.CalledProcessError as e:
        print(f"Git 작업 실패: {e}")

def manage_ddl_change(version):
    """
    DDL 변경 관리
    """
    if not DB_URL or not OLLAMA_API_URL:
        print("데이터베이스 URL 또는 Ollama API URL이 설정되지 않았습니다. .env 파일을 확인하세요.")
        return

    engine = create_engine(DB_URL)

    # 현재 DDL 가져오기
    current_ddl = get_current_ddl(engine)

    # 이전 DDL 로드
    previous_ddl = load_previous_ddl(version)

    # DDL 비교
    diff = compare_ddl(previous_ddl, current_ddl)
    if diff:
        print("DDL 변경 사항 발견:")
        for table, changes in diff.items():
            print(f"Table: {table}")
            print("\n".join(changes))
    else:
        print("변경 사항 없음.")
        return

    # Ollama를 사용해 커밋 메시지 생성
    commit_message = generate_commit_message_with_ollama(diff)

    # 현재 DDL 저장
    file_name = save_ddl_to_file(version, current_ddl)

    # Git 커밋 및 푸시
    git_commit_and_push(file_name, commit_message)

# 사용 예시
if __name__ == "__main__":
    version = datetime.now().strftime("%Y%m%d_%H%M%S")

    # DDL 변경 관리
    manage_ddl_change(version)
