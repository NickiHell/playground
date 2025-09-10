import pytest
from algorithms.graph_algorithms import dijkstra


@pytest.mark.parametrize(
    "graph, start, expected",
    [
        # Тест 1: Простой граф
        (
            {
                "A": [("B", 1), ("C", 4)],
                "B": [("C", 2), ("D", 5)],
                "C": [("D", 1)],
                "D": [],
            },
            "A",
            {"A": 0, "B": 1, "C": 3, "D": 4},
        ),
        # Тест 2: Граф с циклом
        (
            {
                "A": [("B", 3), ("C", 2)],
                "B": [("D", 1)],
                "C": [("B", 1), ("D", 4)],
                "D": [],
            },
            "A",
            {"A": 0, "B": 3, "C": 2, "D": 4},
        ),
        # Тест 3: Граф с одной вершиной
        ({"A": []}, "A", {"A": 0}),
        # Тест 4: Пустой граф
        ({}, "A", {}),
    ],
)
def test_dijkstra(graph, start, expected):
    """Тестирование алгоритма Дейкстры с различными входными данными"""
    result = dijkstra(graph, start)
    assert result == expected
