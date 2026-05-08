import json
import os
from typing import Any


class JsonStore:
    def __init__(self, filepath: str):
        self.filepath = filepath
        if not os.path.exists(filepath):
            self._write({})

    def _read(self) -> dict:
        with open(self.filepath, "r", encoding="utf-8") as f:
            return json.load(f)

    def _write(self, data: dict) -> None:
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def create(self, key: str, value: Any) -> None:
        data = self._read()
        if key in data:
            raise KeyError(f"키 '{key}'가 이미 존재합니다.")
        data[key] = value
        self._write(data)

    def read(self, key: str) -> Any:
        data = self._read()
        if key not in data:
            raise KeyError(f"키 '{key}'를 찾을 수 없습니다.")
        return data[key]

    def read_all(self) -> dict:
        return self._read()

    def update(self, key: str, value: Any) -> None:
        data = self._read()
        if key not in data:
            raise KeyError(f"키 '{key}'를 찾을 수 없습니다.")
        data[key] = value
        self._write(data)

    def delete(self, key: str) -> None:
        data = self._read()
        if key not in data:
            raise KeyError(f"키 '{key}'를 찾을 수 없습니다.")
        del data[key]
        self._write(data)

    def exists(self, key: str) -> bool:
        return key in self._read()
