import time
from typing import Callable, Any, Hashable, Mapping

CallableT = Callable[[tuple[Any], Mapping[Hashable, Any]], Any]
DictT = Mapping[Hashable, Any]


def time_it(func: CallableT) -> Any:
    def inner_func(*args: tuple[tuple[Any]], **kwargs: DictT):
        now = time.time()
        result = func(*args, **kwargs)
        execute_time = time.time() - now
        print(f"Execute time: {execute_time}")
        return result

    return inner_func
