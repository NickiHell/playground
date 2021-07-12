import datetime
import functools
import random
import string
from time import sleep
from typing import Union, Generator, Iterable, Tuple, List, Dict, Set
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


def my_gen(start, stop=None, step=None) -> Generator:
    current = start if start and stop else 0
    stop = start if not stop else stop
    while current < stop:
        yield current
        current += step or 1


class TreeNode:
    def __init__(self, info: str) -> None:
        self._id: uuid4 = str(uuid4())
        self._parent: Union[TreeNode, None] = None
        self.info: str = info


class Tree:
    def __init__(self, nodes: Union[List[TreeNode], None] = None) -> None:
        self._raw_nodes: Union[List[TreeNode], None] = nodes
        self._tree: Union[List[TreeNode], None] = None
        self._build_tree()

    def add_node(self, node: TreeNode) -> None:
        pass

    def remove_node(self, node: TreeNode) -> None:
        pass

    def search_node_by_info(self, info: str) -> Tuple[uuid4, str]:
        pass

    def _build_tree(self):
        if not self._raw_nodes or self._tree:
            raise RuntimeError("Already build")
        self._raw_nodes.sort(key=lambda x: x.info)


class Graph:
    def __init__(self, points: Iterable[Tuple[str, str]]) -> None:
        self._points: Iterable[Tuple[str, str]] = points
        self._graph: Dict[str, set] = {}
        self._build_graph()

    def add_point(self, point: Tuple[str, str]) -> None:
        links: set = self._graph.get(point[0])
        links.add(point[1])

    def remove_point(self, name: str) -> None:
        self._graph.pop(name)

    def remove_link(self, name: str, link: str) -> None:
        links: Set = self._graph.get(name)
        links.remove(link)

    def _build_graph(self):
        self._graph.clear()
        [self._graph.update({name: set(links.split())}) for name, links in self._points]

    def __repr__(self):
        return f'{self._graph}'


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

    nodes = [TreeNode(x) for x in string.ascii_letters]

    tree = Tree(nodes)

    graph = Graph((x, y) for x in 'AB' for y in 'C')
    print(graph)
    graph.add_point(('A', 'B'))
    print(graph)
    graph.remove_link('A', 'B')
    print(graph)
