import pytest
from json_store import JsonStore


@pytest.fixture
def store(tmp_path):
    return JsonStore(str(tmp_path / "test.json"))


# ── 초기화 ──────────────────────────────────────────────

class TestInit:
    def test_파일이_없으면_자동_생성된다(self, tmp_path):
        path = tmp_path / "new.json"
        assert not path.exists()
        JsonStore(str(path))
        assert path.exists()

    def test_파일이_이미_있으면_덮어쓰지_않는다(self, tmp_path):
        path = tmp_path / "existing.json"
        s = JsonStore(str(path))
        s.create("key", "value")
        JsonStore(str(path))  # 재초기화
        assert JsonStore(str(path)).read("key") == "value"


# ── Create ───────────────────────────────────────────────

class TestCreate:
    def test_새_항목을_저장한다(self, store):
        store.create("a", 1)
        assert store.read("a") == 1

    def test_딕셔너리_값을_저장한다(self, store):
        store.create("user", {"name": "홍길동", "age": 30})
        assert store.read("user") == {"name": "홍길동", "age": 30}

    def test_리스트_값을_저장한다(self, store):
        store.create("tags", ["python", "json"])
        assert store.read("tags") == ["python", "json"]

    def test_중복_키는_KeyError를_발생시킨다(self, store):
        store.create("a", 1)
        with pytest.raises(KeyError):
            store.create("a", 2)

    def test_중복_키_오류_후_원본값이_유지된다(self, store):
        store.create("a", 1)
        with pytest.raises(KeyError):
            store.create("a", 99)
        assert store.read("a") == 1


# ── Read ─────────────────────────────────────────────────

class TestRead:
    def test_저장된_값을_반환한다(self, store):
        store.create("x", "hello")
        assert store.read("x") == "hello"

    def test_없는_키는_KeyError를_발생시킨다(self, store):
        with pytest.raises(KeyError):
            store.read("없는키")

    def test_None_값을_저장하고_읽는다(self, store):
        store.create("n", None)
        assert store.read("n") is None

    def test_빈_문자열_키를_허용한다(self, store):
        store.create("", "empty_key")
        assert store.read("") == "empty_key"


# ── Read All ─────────────────────────────────────────────

class TestReadAll:
    def test_빈_저장소는_빈_딕셔너리를_반환한다(self, store):
        assert store.read_all() == {}

    def test_모든_항목을_반환한다(self, store):
        store.create("a", 1)
        store.create("b", 2)
        assert store.read_all() == {"a": 1, "b": 2}

    def test_반환값은_독립적인_복사본이다(self, store):
        store.create("a", 1)
        result = store.read_all()
        result["a"] = 999
        assert store.read("a") == 1


# ── Update ───────────────────────────────────────────────

class TestUpdate:
    def test_값을_수정한다(self, store):
        store.create("a", 1)
        store.update("a", 2)
        assert store.read("a") == 2

    def test_타입을_변경한다(self, store):
        store.create("a", 1)
        store.update("a", {"new": "value"})
        assert store.read("a") == {"new": "value"}

    def test_없는_키는_KeyError를_발생시킨다(self, store):
        with pytest.raises(KeyError):
            store.update("없는키", 1)

    def test_다른_키는_영향받지_않는다(self, store):
        store.create("a", 1)
        store.create("b", 2)
        store.update("a", 99)
        assert store.read("b") == 2


# ── Delete ───────────────────────────────────────────────

class TestDelete:
    def test_항목을_삭제한다(self, store):
        store.create("a", 1)
        store.delete("a")
        assert not store.exists("a")

    def test_삭제_후_read하면_KeyError가_발생한다(self, store):
        store.create("a", 1)
        store.delete("a")
        with pytest.raises(KeyError):
            store.read("a")

    def test_없는_키는_KeyError를_발생시킨다(self, store):
        with pytest.raises(KeyError):
            store.delete("없는키")

    def test_다른_키는_영향받지_않는다(self, store):
        store.create("a", 1)
        store.create("b", 2)
        store.delete("a")
        assert store.read("b") == 2


# ── Exists ───────────────────────────────────────────────

class TestExists:
    def test_존재하는_키는_True를_반환한다(self, store):
        store.create("a", 1)
        assert store.exists("a") is True

    def test_없는_키는_False를_반환한다(self, store):
        assert store.exists("없는키") is False

    def test_삭제된_키는_False를_반환한다(self, store):
        store.create("a", 1)
        store.delete("a")
        assert store.exists("a") is False


# ── 파일 영속성 ───────────────────────────────────────────

class TestPersistence:
    def test_인스턴스를_새로_만들어도_데이터가_유지된다(self, tmp_path):
        path = str(tmp_path / "persist.json")
        s1 = JsonStore(path)
        s1.create("key", "value")

        s2 = JsonStore(path)
        assert s2.read("key") == "value"

    def test_한글_값이_손상_없이_저장된다(self, tmp_path):
        path = str(tmp_path / "korean.json")
        s1 = JsonStore(path)
        s1.create("name", "홍길동")

        s2 = JsonStore(path)
        assert s2.read("name") == "홍길동"
