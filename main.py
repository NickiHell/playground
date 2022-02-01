import datetime
import functools
import itertools
import os
import random
import string
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from multiprocessing import Queue
from time import sleep
from typing import (Any, Callable, Dict, Generator, Iterable, List, Optional,
                    Set, Tuple, Union)
from uuid import uuid4

from loguru import logger


class Singleton:
    instance = None

    def __new__(cls):
        if not cls.instance:
            cls.instance = super().__new__(cls)
        return cls.instance


class TestClass:
    instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super().__new__(cls)
        return cls.instance


def timeit_results(func: Callable) -> Callable:
    # series = []

    @functools.wraps(func)
    def inner(*args, **kwargs):
        # nonlocal series
        now = time.time()
        # sleep(1)
        result = func(*args, **kwargs)
        result_time: float = time.time() - now
        # series.append(result_time)
        arguments = ', '.join([str(x) for x in args] + [f'{k}:{v}' for k, v in kwargs.items()])
        print(f'Func: {func.__name__}({arguments}): {result_time:2f}s')
        return result

    return inner


def elapsed_time(func: Callable) -> Callable:
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
        self._id: str = str(uuid4())
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

    @timeit_results
    def add_point(self, point: Tuple[str, str]) -> None:
        links: Optional[Set[Any]] = self._graph.get(point[0])
        links.add(point[1])

    @timeit_results
    def remove_point(self, name: str) -> None:
        self._graph.pop(name)

    @timeit_results
    def remove_link(self, name: str, link: str) -> None:
        links: Optional[Set[Any]] = self._graph.get(name)
        links.remove(link)

    @timeit_results
    def _build_graph(self):
        self._graph.clear()
        [self._graph.update({name: set(links.split())}) for name, links in self._points]

    def __repr__(self):
        return f'{self._graph}'


@timeit_results
# @functools.lru_cache(24)
def big_job(stop: int = 0, stype: str = 'tuple'):
    return eval(f'{stype}(x for x in range({stop}))')


def infinite_job(queue: Queue, name: str) -> None:
    while True:
        sleep(1)
        if name == 'producer':
            number: int = random.randint(0, 999)
            queue.put(number)
        else:
            pass
            logger.info(f'Consumer -> {os.getpid()} get: {queue.get()}')


class A:
    def exec(self):
        print()


class B:
    a = A()

    def __call__(self, *args, **kwargs):
        self.a.exec()


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

    big_job(10000000, 'set')

    a = TestClass()
    b = TestClass()

    assert a is b

    assert list(itertools.chain([1, 2], [3, 4])) == [1, 2, 3, 4]
    assert sum([sum(y) for y in itertools.tee(big_job(5, 'set'), 5)]) == 50
    counter = itertools.count(0, 10)
    val = next(counter)
    assert val == 0
    val = next(counter)
    assert val == 10

    assert list(itertools.combinations_with_replacement('AB', r=2)) == [('A', 'A'), ('A', 'B'), ('B', 'B')]
    assert list(itertools.dropwhile(len, ('1', '2', ''))) == ['']
    assert list(itertools.combinations('AB', r=2)) == [('A', 'B')]
    data = {
        'a': {
            'key': 1,
            'data': set(string.ascii_letters.upper()),
        },
        'b': {
            'key': 2,
            'data': set(string.ascii_letters.lower()),
        },
        'c': {
            'key': 2,
            'data': set(string.ascii_letters.lower()),
        },
    }

    grouped_by_key = [(x, tuple(y)) for x, y in itertools.groupby(data, key=lambda x: data[x]['key'])]
    assert str(grouped_by_key) == "[(1, ('a',)), (2, ('b', 'c'))]"

    assert str(list(itertools.product([1, 2], repeat=2))) == "[(1, 1), (1, 2), (2, 1), (2, 2)]"

    results = []
    now = time.time()
    with ProcessPoolExecutor(8) as executor:
        for i in range(8):
            future = executor.submit(big_job, 100000, random.choice(('set', 'tuple', 'list')))
            # results.append(future.result())
    print(f'Process Job Done! {time.time() - now:2f} sec')

    # results = []
    now = time.time()
    with ThreadPoolExecutor(8) as executor:
        for i in range(8):
            future = executor.submit(big_job, 100000, random.choice(('set', 'tuple', 'list')))
            # results.append(future.result())
    print(f'Threads Job Done! {time.time() - now:2f} sec')

    # q = Queue(maxsize=64)
    # p1 = Process(name='producer', target=infinite_job, args=(q, 'producer'))
    # p1.start()
    # proc_array: Dict = {
    #     '1': Process(name='consumer', target=infinite_job, args=(q, 'consumer')),
    #     '2': Process(name='consumer', target=infinite_job, args=(q, 'consumer')),
    #     '3': Process(name='consumer', target=infinite_job, args=(q, 'consumer')),
    # }
    # for _, value in proc_array.items():
    #     value.start()

    b = B()
    b()


    def enumerate1(xss: Iterable):
        counter = 0
        for item in xss:
            yield counter, item
            counter += 1


    a = (1, 2, 3)
    print([(x, y) for x, y in enumerate1(a)])
