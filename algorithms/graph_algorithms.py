import heapq
from typing import Dict, Union, List, Tuple


def dijkstra(
    graph: Dict[str, List[Tuple[str, int]]], start: str
) -> Dict[str, Union[int, float]]:
    """
    Реализация алгоритма Дейкстры для поиска кратчайшего пути в взвешенном графе.

    Args:
        graph: Словарь, представляющий граф в формате {вершина: [(сосед, вес), ...]}
        start: Начальная вершина

    Returns:
        Словарь с кратчайшими расстояниями от начальной вершины до всех остальных
    """
    # Если граф пустой или начальной вершины нет в графе, возвращаем пустой словарь
    if not graph or start not in graph:
        return {}

    distances = {vertex: float("infinity") for vertex in graph}
    distances[start] = 0
    pq = [(0, start)]
    visited = set()

    while pq:
        current_distance, current_vertex = heapq.heappop(pq)

        if current_vertex in visited:
            continue

        visited.add(current_vertex)

        # Обрабатываем соседей текущей вершины
        for neighbor, weight in graph[current_vertex]:
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))

    return distances
