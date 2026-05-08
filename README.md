# DataPersistence

JSON 파일 기반의 CRUD 데이터 영속성 라이브러리입니다.

## 기술 스택

- Python 3.14
- pytest 9.0.3
- 외부 의존성 없음 (표준 라이브러리만 사용)

## 설치 및 실행

```powershell
# 가상환경 활성화
.\.venv\Scripts\Activate.ps1

# 예제 실행
$env:PYTHONUTF8=1
python main.py

# 테스트 실행
.\.venv\Scripts\pytest.exe tests/ -v
```

## 구조

```
datapersistence/
├── json_store.py        # JsonStore 클래스 (핵심 로직)
├── main.py              # 사용 예제
├── tests/
│   └── test_json_store.py  # pytest 테스트 (27개)
└── pyproject.toml
```

## API

```python
from json_store import JsonStore

store = JsonStore("data.json")

store.create("key", value)   # 생성 — 중복 키 시 KeyError
store.read("key")            # 단일 조회 — 없으면 KeyError
store.read_all()             # 전체 조회
store.update("key", value)   # 수정 — 없으면 KeyError
store.delete("key")          # 삭제 — 없으면 KeyError
store.exists("key")          # 존재 여부 확인 (bool)
```

`value`는 `dict`, `list`, `str`, `int`, `None` 등 JSON 직렬화 가능한 모든 타입을 지원합니다.

## 구현 사항

### JsonStore 클래스 (`json_store.py`)

- 파일이 없으면 인스턴스 생성 시 자동으로 빈 JSON 파일 초기화
- 모든 연산은 파일 전체를 읽고 쓰는 방식으로 동작
- `ensure_ascii=False` 설정으로 한글 등 유니코드 그대로 저장
- 존재하지 않는 키 접근 / 중복 생성 시 `KeyError` 발생

### 테스트 (`tests/test_json_store.py`)

총 27개 테스트, 8개 클래스로 구성

| 클래스 | 테스트 수 | 주요 검증 항목 |
|---|---|---|
| `TestInit` | 2 | 파일 자동 생성, 기존 파일 보존 |
| `TestCreate` | 5 | 기본 저장, dict/list 값, 중복 키 오류, 원본 보호 |
| `TestRead` | 4 | 값 반환, 없는 키 오류, None 값, 빈 문자열 키 |
| `TestReadAll` | 3 | 빈 저장소, 전체 반환, 독립 복사본 |
| `TestUpdate` | 4 | 값/타입 수정, 없는 키 오류, 사이드이펙트 없음 |
| `TestDelete` | 4 | 삭제, 삭제 후 오류, 없는 키 오류, 사이드이펙트 없음 |
| `TestExists` | 3 | 존재/비존재/삭제 후 False |
| `TestPersistence` | 2 | 인스턴스 재생성 후 데이터 유지, 한글 무결성 |

각 테스트는 `tmp_path` fixture로 격리된 임시 파일을 사용합니다.
