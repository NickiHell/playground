import datetime
import functools
import random
from time import sleep
from typing import Union, Generator, Iterable, Tuple
from uuid import uuid4


def elapsed_time(func: callable) -> callable:
    elapsed_time: Union[datetime.datetime, None] = None

    @functools.wraps(func)
    def inner(*args, **kwargs):
        now = datetime.datetime.now()
        result = func(*args, **kwargs)
        globals()[func.__name__].elapsed_time = datetime.datetime.now() - now
        return result

    inner.elapsed_time = elapsed_time
    return inner


@elapsed_time
def test1(a: str, b: str) -> str:
    sleep(1)
    return f'{a} {b}'


@functools.lru_cache(10)
def get_random(not_needed=None) -> int:
    return random.randint(0, 999)


@functools.singledispatch
def add(x, y):
    raise NotImplemented


@add.register(int)
def _(x: int, y: int) -> int:
    return x + y


@add.register(str)
def _(x: str, y: str) -> str:
    return x + y


def mul(a, b):
    return a * b


def my_gen(start, stop=None, step=None) -> Generator[int]:
    current = start if start and stop else 0
    stop = start if not stop else stop
    while current < stop:
        yield current
        current += step or 1


class TreeNode:
    def __init__(self, info: str) -> None:
        self._id: uuid4 = str(uuid4())
        self.info: str = info


class Tree:
    def __init__(self, nodes: Iterable[TreeNode]) -> None:
        self._raw_nodes: Iterable[TreeNode] = nodes
        self._tree = None

    def add_node(self, node: TreeNode) -> None:
        pass

    def remove_node(self, node: TreeNode) -> None:
        pass

    def search_node_by_info(self, info: str) -> Tuple[uuid4, str]:
        pass

    def _build_tree(self):
        pass


if __name__ == '__main__':
    assert test1.elapsed_time is None
    assert test1('1', '2') == '1 2'
    assert test1.elapsed_time > datetime.timedelta(0)

    assert get_random(1) == get_random(1) == get_random(1) != get_random(2)
    assert get_random(2) == get_random(2)

    assert add(1, 2) == 3

    assert add('1', '2') == '12'

    mul_new = functools.partial(mul, 2)

    assert mul_new(2) == 4

    assert [x for x in my_gen(2)] == [0, 1]
    assert [x for x in my_gen(1, 2)] == [1]
    assert [x for x in my_gen(0, 10, 2)] == [0, 2, 4, 6, 8]
