from tasks.lru_cache import LRUCache, MemoryDT


if __name__ == "__main__":
    # test_find_single_number_solutions()
    # test_xor()
    cache = LRUCache(size=2, cache_timeout=10)
    print(cache)
    cache.memory = MemoryDT(1, 1)
    cache.memory = MemoryDT(1, 1)
    cache.memory = MemoryDT(1, 1)
