def binary_search(arr, item):
    """
    Бинарный поиск

    Алгоритм ищет элемент в отсортированном массиве, сравнивая его с серединой.
    Если элемент меньше середины, то ищем в левой половине, если больше - в правой.

    Сложность: O(log n)

    Args:
        arr (list): Отсортированный список чисел
        item: Элемент для поиска

    Returns:
        int: Индекс элемента или None если не найден

    Example:
        >>> binary_search([1, 3, 5, 7, 9], 3)
        1
        >>> binary_search([1, 3, 5, 7, 9], 4)
        None
    """
    low = 0
    high = len(arr) - 1

    while low <= high:
        mid = (low + high) // 2
        guess = arr[mid]

        if guess == item:
            return mid
        elif guess > item:
            high = mid - 1
        else:
            low = mid + 1

    return None


def find_smallest(arr):
    """
    Поиск наименьшего элемента в массиве

    Сравнивает каждый элемент с текущим минимальным и обновляет его при необходимости.

    Сложность: O(n)

    Args:
        arr (list): Список чисел

    Returns:
        int: Наименьший элемент

    Example:
        >>> find_smallest([3, 1, 4, 1, 5])
        1
    """
    smallest = arr[0]
    smallest_index = 0

    for i in range(1, len(arr)):
        if arr[i] < smallest:
            smallest = arr[i]
            smallest_index = i

    return smallest_index


def selection_sort(arr):
    """
    Сортировка выбором

    Алгоритм находит наименьший элемент и помещает его в начало массива,
    затем повторяет процесс для оставшихся элементов.

    Сложность: O(n^2)

    Args:
        arr (list): Список чисел для сортировки

    Returns:
        list: Отсортированный список

    Example:
        >>> selection_sort([64, 34, 25, 12, 22, 11, 90])
        [11, 12, 22, 25, 34, 64, 90]
    """
    new_arr = []

    for i in range(len(arr)):
        smallest_index = find_smallest(arr)
        new_arr.append(arr.pop(smallest_index))

    return new_arr


def factorial(n):
    """
    Рекурсивный алгоритм вычисления факториала

    Факториал числа n - это произведение всех положительных целых чисел от 1 до n.

    Сложность: O(n)

    Args:
        n (int): Положительное число

    Returns:
        int: Факториал числа n

    Example:
        >>> factorial(5)
        120
    """
    if n == 1:
        return 1
    else:
        return n * factorial(n - 1)


def quicksort(arr):
    """
    Быстрая сортировка (алгоритм Хоара)

    Рекурсивный алгоритм, который выбирает опорный элемент и разделяет массив
    на элементы меньше и больше опорного. Затем рекурсивно сортирует обе части.

    Сложность: O(n log n) в среднем случае, O(n^2) в худшем случае

    Args:
        arr (list): Список чисел для сортировки

    Returns:
        list: Отсортированный список

    Example:
        >>> quicksort([64, 34, 25, 12, 22, 11, 90])
        [11, 12, 22, 25, 34, 64, 90]
    """
    if len(arr) < 2:
        return arr
    else:
        pivot = arr[0]
        less = [i for i in arr[1:] if i <= pivot]
        greater = [i for i in arr[1:] if i > pivot]

        return quicksort(less) + [pivot] + quicksort(greater)


def dijkstra(graph, start, finish):
    """
    Алгоритм Дейкстры для поиска кратчайшего пути

    Находит кратчайший путь от начальной вершины до конечной в графе с неотрицательными весами.

    Сложность: O((V + E) log V), где V - количество вершин, E - количество рёбер

    Args:
        graph (dict): Граф представлен как словарь смежности с весами
        start: Начальная вершина
        finish: Конечная вершина

    Returns:
        tuple: (расстояние, путь) или (None, None) если путь не найден

    Example:
        >>> graph = {'A': {'B': 5, 'C': 2}, 'B': {'D': 4}, 'C': {'B': 8, 'D': 6}}
        >>> dijkstra(graph, 'A', 'D')
        (11, ['A', 'C', 'D'])
    """
    costs = {}
    parents = {}

    # Инициализация
    for node in graph:
        if node == start:
            costs[node] = 0
        else:
            costs[node] = float("inf")
        parents[node] = None

    processed = []

    def find_lowest_cost_node():
        lowest_cost = float("inf")
        lowest_cost_node = None

        for node in costs:
            cost = costs[node]
            if cost < lowest_cost and node not in processed:
                lowest_cost = cost
                lowest_cost_node = node

        return lowest_cost_node

    node = find_lowest_cost_node()

    while node is not None:
        cost = costs[node]
        neighbors = graph.get(node, {})

        for neighbor, weight in neighbors.items():
            new_cost = cost + weight

            if new_cost < costs[neighbor]:
                costs[neighbor] = new_cost
                parents[neighbor] = node

        processed.append(node)
        node = find_lowest_cost_node()

    # Восстановление пути
    if costs[finish] == float("inf"):
        return None, None

    path = []
    current = finish

    while current is not None:
        path.append(current)
        current = parents[current]

    path.reverse()

    return costs[finish], path


def breadth_first_search(graph, start, target):
    """
    Поиск в ширину (BFS)

    Алгоритм обходит граф по уровням, начиная с заданной вершины.
    Используется очередь для хранения вершин для посещения.

    Сложность: O(V + E), где V - количество вершин, E - количество рёбер

    Args:
        graph (dict): Граф представлен как словарь смежности
        start: Начальная вершина
        target: Целевая вершина

    Returns:
        bool: True если целевая вершина найдена, False в противном случае

    Example:
        >>> graph = {'A': ['B', 'C'], 'B': ['D'], 'C': ['E']}
        >>> breadth_first_search(graph, 'A', 'E')
        True
    """
    from collections import deque

    queue = deque()
    queue.append(start)
    visited = set()

    while queue:
        node = queue.popleft()

        if node not in visited:
            visited.add(node)

            if node == target:
                return True

            neighbors = graph.get(node, [])
            for neighbor in neighbors:
                if neighbor not in visited:
                    queue.append(neighbor)

    return False
