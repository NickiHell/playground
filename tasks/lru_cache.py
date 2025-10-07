from dataclasses import dataclass
from datetime import datetime
from typing import Iterable, Any
from loguru import logger

from utils.datetime import now


@dataclass()
class MemoryDT:
    key: int
    value: int
    created_at: datetime = now()

    def __str__(self) -> str:
        return f"Memory unit: {self.key}:{self.value}, dt - {self.created_at}"


class LRUCache:
    def __init__(
        self, size: int, cache_timeout: int = 60, raise_error: bool = False
    ) -> None:
        self._cache_timeout: int = cache_timeout  # in secs
        self._memory_size: int = size
        self._memory: list[MemoryDT] = []

    @property
    def memory(self) -> str:
        return str(self.memory)

    @memory.getter
    def memory(self, key: int) -> int | None:
        logger.info(f"Get cache by key {key}")
        return self._memory.get(key, default=None)  # type: ignore

    @memory.setter
    def memory(self, data: MemoryDT) -> None:
        if self._is_cache_overheaded:
            self._remove_old_cache(self._get_old_cache_records)
        logger.info(f"Put {data.key}:{data.value}")
        self._memory.append(MemoryDT(key=data.key, value=data.value))

    @property
    def _is_cache_overheaded(self) -> bool:
        return True if self.__len__() else False

    @property
    def _get_old_cache_records(self) -> Iterable[int]:
        return tuple(dt.key for dt in self._memory)

    def _remove_old_cache(self, keys: Iterable[int]) -> None:
        for key in keys:
            try:
                self._memory.pop(key)
                logger.info(f"Cache with key removed: {key}")
            except IndexError as exc:
                logger.debug(f"{self.__class__} - Excutiox: {exc}")

    def __str__(self) -> str:
        return f"Cache: {self._memory}"

    def __len__(self) -> list[Any]:
        return [
            dt.key for dt in self.memory if now - dt.created_at > self._cache_timeout
        ]
