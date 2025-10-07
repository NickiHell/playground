from tasks.lru_cache import LRUCache, MemoryDT
from utils.datetime import now
import pytest
from tasks.find_single_number import find_single_number_best, find_single_number_poor
from utils.exceptions import CacheOverheadError


@pytest.mark.parametrize(
    ("numbers", "result"),
    [
        ([1, 1, 2, 2, 3], 3),
        ([2, 3, 3], 2),
        ([10, 10, 0, 0, 1], 1),
    ],  # type: ignore
)
def test_find_single_number_poor(numbers: list[int], result: int):
    assert find_single_number_poor(numbers) == result


@pytest.mark.parametrize(
    ("numbers", "result"),
    [
        ([1, 1, 2, 2, 3], 3),
        ([2, 3, 3], 2),
        ([10, 10, 0, 0, 1], 1),
    ],  # type: ignore
)
def test_find_single_number_best(numbers: list[int], result: int):
    assert find_single_number_best(numbers) == result


@pytest.mark.parametrize(  # type: ignore
    ("size", "cache_timeout"),
    (
        [8, 1],
        [500, 4],
        [1_000_000, 8],
    ),
)
def test_lru_cache(size: int, cache_timeput: int) -> None:
    # Arrange
    cache = LRUCache(size, cache_timeout=cache_timeput, raise_error=True)

    # Act
    start = now()
    for key, index in enumerate(cache.memory):
        cache.memory = MemoryDT(key, index)
    time_result = now() - start

    with pytest.raises(CacheOverheadError):
        cache.memory = MemoryDT(1, 1)

    # Assert
    assert time_result.microseconds < now().microsecond


def test_lru_put_and_get() -> None:
    # Arrange
    cache = LRUCache(2, 0)

    # Act
    cache.memory = MemoryDT(1, 1)
    cache.memory = MemoryDT(2, 2)

    # Assert
    assert cache.memory[1] == 1  # Вернет 1
    cache.memory = MemoryDT(3, 3)  # Удалит ключ 2
    assert cache.memory[2] is None  # Вернет None
