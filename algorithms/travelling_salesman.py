import itertools
from typing import List, Tuple


def brute_force_tsp(distances: List[List[float]]) -> Tuple[float, List[int]]:
    """
    Решение задачи комивояжера перебором всех путей (полный перебор)

    Находит кратчайший маршрут, проходящий через все города ровно один раз и возвращающийся в начальный город.

    Сложность: O(n!) где n - количество городов

    Args:
        distances (List[List[float]]): Матрица расстояний между городами

    Returns:
        Tuple[float, List[int]]: (минимальная стоимость, путь)

    Example:
        >>> distances = [[0, 10, 15, 20], [10, 0, 35, 25], [15, 35, 0, 30], [20, 25, 30, 0]]
        >>> brute_force_tsp(distances)
        (80, [0, 1, 3, 2])
    """
    n = len(distances)
    if n <= 1:
        return 0, []

    # Все перестановки городов (начинаются с 0)
    min_cost = float("inf")
    best_path: List[int] | None = None

    for perm in itertools.permutations(range(1, n)):
        path = [0] + list(perm) + [0]
        cost = 0.0

        for i in range(len(path) - 1):
            cost += distances[path[i]][path[i + 1]]

        if cost < min_cost:
            min_cost = cost
            best_path = path

    return min_cost, best_path or []


def nearest_neighbor_tsp(distances: List[List[float]]) -> Tuple[float, List[int]]:
    """
    Решение задачи комивояжера жадным алгоритмом (алгоритм ближайшего соседа)

    Начинает с произвольного города и на каждом шаге выбирает ближайший непосещенный город.

    Сложность: O(n^2) где n - количество городов

    Args:
        distances (List[List[float]]): Матрица расстояний между городами

    Returns:
        Tuple[float, List[int]]: (стоимость пути, путь)

    Example:
        >>> distances = [[0, 10, 15, 20], [10, 0, 35, 25], [15, 35, 0, 30], [20, 25, 30, 0]]
        >>> nearest_neighbor_tsp(distances)
        (80, [0, 1, 3, 2])
    """
    n = len(distances)
    if n <= 1:
        return 0, []

    unvisited = set(range(1, n))
    current_city = 0
    path = [0]
    total_cost = 0.0

    while unvisited:
        nearest_city = min(unvisited, key=lambda city: distances[current_city][city])
        unvisited.remove(nearest_city)
        total_cost += distances[current_city][nearest_city]
        current_city = nearest_city
        path.append(current_city)

    # Возвращаемся в начальный город
    total_cost += distances[current_city][0]
    path.append(0)

    return total_cost, path


def dynamic_tsp(distances: List[List[float]]) -> Tuple[float, List[int]]:
    """
    Решение задачи комивояжера с использованием динамического программирования

    Использует метод bitmask для представления подмножеств городов.

    Сложность: O(n^2 * 2^n) где n - количество городов

    Args:
        distances (List[List[float]]): Матрица расстояний между городами

    Returns:
        Tuple[float, List[int]]: (минимальная стоимость, путь)

    Example:
        >>> distances = [[0, 10, 15, 20], [10, 0, 35, 25], [15, 35, 0, 30], [20, 25, 30, 0]]
        >>> dynamic_tsp(distances)
        (80, [0, 1, 3, 2])
    """
    n = len(distances)
    if n <= 1:
        return 0, []

    # dp[mask][i] - минимальная стоимость пути, который посещает города в mask и заканчивается в городе i
    dp = [[float("inf")] * n for _ in range(1 << n)]
    parent = [[-1] * n for _ in range(1 << n)]

    # Начинаем с города 0
    dp[1][0] = 0

    for mask in range(1, 1 << n):
        for u in range(n):
            if not (mask & (1 << u)):
                continue

            for v in range(n):
                if mask & (1 << v):
                    continue

                new_mask = mask | (1 << v)
                new_cost = dp[mask][u] + distances[u][v]

                if new_cost < dp[new_mask][v]:
                    dp[new_mask][v] = new_cost
                    parent[new_mask][v] = u

    # Находим минимальную стоимость возвращения в начальный город
    final_mask = (1 << n) - 1
    min_cost = float("inf")
    last_city = -1

    for i in range(1, n):
        if dp[final_mask][i] + distances[i][0] < min_cost:
            min_cost = dp[final_mask][i] + distances[i][0]
            last_city = i

    # Восстановление пути
    path = []
    mask = final_mask
    current = last_city

    while current != -1:
        path.append(current)
        next_current = parent[mask][current]
        mask ^= 1 << current
        current = next_current

    path.reverse()
    path = [0] + path

    return min_cost, path
