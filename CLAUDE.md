# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 기술 스택

- **언어**: Python 3.14
- **의존성**: 외부 패키지 없음 (표준 라이브러리 `json`, `os`만 사용)
- **가상환경**: `.venv` (프로젝트 루트)
- **패키지 관리**: `pyproject.toml`

## 실행 명령어

```powershell
# 가상환경 활성화
.\.venv\Scripts\Activate.ps1

# 예제 실행 (data.json이 이미 존재하면 삭제 후 실행)
Remove-Item data.json -ErrorAction SilentlyIgnore
$env:PYTHONUTF8=1
python main.py
```

> Windows 환경에서 한글 출력이 깨질 경우 `$env:PYTHONUTF8=1`을 먼저 설정한다.

## 테스트 방법

별도 테스트 프레임워크는 설정되어 있지 않다. 테스트를 추가할 경우 `pytest`를 권장한다.

```powershell
# pytest 설치
.\.venv\Scripts\pip.exe install pytest

# 전체 테스트 실행
.\.venv\Scripts\pytest.exe

# 단일 테스트 파일 실행
.\.venv\Scripts\pytest.exe tests/test_json_store.py

# 단일 테스트 함수 실행
.\.venv\Scripts\pytest.exe tests/test_json_store.py::test_create
```

## 아키텍처

### 핵심 모듈: `json_store.py`

`JsonStore` 클래스가 JSON 파일 기반 CRUD 영속성 레이어 전체를 담당한다.

- **저장 구조**: `{ "key": value }` 형태의 단일 JSON 객체. `key`는 문자열, `value`는 JSON 직렬화 가능한 모든 타입.
- **읽기/쓰기**: 모든 연산은 `_read()` → 변경 → `_write()` 패턴으로 파일 전체를 재작성한다. 동시성 처리는 없다.
- **오류 처리**: 존재하지 않는 키 접근 또는 중복 생성 시 `KeyError`를 발생시킨다.

### 데이터 흐름

```
main.py (사용 예제)
    └── JsonStore (json_store.py)
            └── data.json (런타임 생성, 영속 저장소)
```

`data.json`은 `JsonStore` 인스턴스 생성 시 파일이 없으면 자동으로 빈 객체(`{}`)로 초기화된다.
