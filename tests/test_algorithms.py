import unittest
import time
import random
from algorithms.base_algorithms import (
    binary_search, 
    selection_sort, 
    quicksort,
    dijkstra,
    breadth_first_search
)
from algorithms.greedy_algorithms import (
    activity_selection,
    fractional_knapsack,
    coin_change_greedy
)
from algorithms.divide_and_conquer import (
    merge_sort,
    power,
    max_subarray_sum,
    find_peak_element
)
from algorithms.trees import (
    TreeNode,
    inorder_traversal,
    preorder_traversal,
    postorder_traversal,
    level_order_traversal,
    tree_height,
    is_balanced,
    search_in_bst
)
from algorithms.travelling_salesman import (
    brute_force_tsp,
    nearest_neighbor_tsp,
    dynamic_tsp
)


class TestBaseAlgorithms(unittest.TestCase):

    def test_binary_search(self):
        arr = [1, 3, 5, 7, 9]
        self.assertEqual(binary_search(arr, 3), 1)
        self.assertIsNone(binary_search(arr, 4))

    def test_selection_sort(self):
        arr = [64, 34, 25, 12, 22, 11, 90]
        expected = [11, 12, 22, 25, 34, 64, 90]
        self.assertEqual(selection_sort(arr), expected)

    def test_quicksort(self):
        arr = [64, 34, 25, 12, 22, 11, 90]
        expected = [11, 12, 22, 25, 34, 64, 90]
        self.assertEqual(quicksort(arr), expected)

    def test_dijkstra(self):
        graph = {'A': {'B': 5, 'C': 2}, 'B': {'D': 4}, 'C': {'B': 8, 'D': 6}}
        distance, path = dijkstra(graph, 'A', 'D')
        self.assertEqual(distance, 11)
        self.assertEqual(path, ['A', 'C', 'D'])

    def test_breadth_first_search(self):
        graph = {'A': ['B', 'C'], 'B': ['D'], 'C': ['E']}
        self.assertTrue(breadth_first_search(graph, 'A', 'E'))
        self.assertFalse(breadth_first_search(graph, 'A', 'F'))

    def test_binary_search_performance(self):
        # Тест скорости для большого массива
        size = 100000
        arr = list(range(size))
        target = size // 2

        start_time = time.time()
        result = binary_search(arr, target)
        end_time = time.time()

        self.assertEqual(result, target)
        # Проверяем, что выполнение занимает менее секунды
        self.assertLess(end_time - start_time, 1.0)

    def test_quicksort_performance(self):
        # Тест скорости для большого массива
        size = 10000
        arr = [random.randint(1, 1000) for _ in range(size)]

        start_time = time.time()
        sorted_arr = quicksort(arr)
        end_time = time.time()

        # Проверяем правильность сортировки
        self.assertEqual(sorted_arr, sorted(arr))
        # Проверяем, что выполнение занимает менее секунды
        self.assertLess(end_time - start_time, 1.0)


class TestGreedyAlgorithms(unittest.TestCase):

    def test_activity_selection(self):
        activities = [(1, 4, 'A'), (3, 5, 'B'), (0, 6, 'C'), (5, 7, 'D')]
        selected = activity_selection(activities)
        self.assertEqual(len(selected), 2)

    def test_fractional_knapsack(self):
        items = [(10, 60, 'A'), (20, 100, 'B'), (30, 120, 'C')]
        value, selected = fractional_knapsack(items, 50)
        self.assertEqual(value, 240.0)

    def test_coin_change_greedy(self):
        coins = [25, 10, 5, 1]
        result = coin_change_greedy(coins, 67)
        self.assertEqual(result, [25, 25, 10, 5, 1, 1])


class TestDivideAndConquerAlgorithms(unittest.TestCase):

    def test_merge_sort(self):
        arr = [64, 34, 25, 12, 22, 11, 90]
        expected = [11, 12, 22, 25, 34, 64, 90]
        self.assertEqual(merge_sort(arr), expected)

    def test_power(self):
        self.assertEqual(power(2, 10), 1024)
        self.assertEqual(power(3, 4), 81)

    def test_max_subarray_sum(self):
        arr = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
        self.assertEqual(max_subarray_sum(arr), 6)

    def test_find_peak_element(self):
        arr = [1, 3, 20, 4, 1, 0]
        self.assertEqual(find_peak_element(arr), 20)


class TestTreeAlgorithms(unittest.TestCase):

    def setUp(self):
        # Создаем тестовое дерево:
        #       1
        #      / \
        #     2   3
        #    / \
        #   4   5
        self.root = TreeNode(1)
        self.root.left = TreeNode(2)
        self.root.right = TreeNode(3)
        self.root.left.left = TreeNode(4)
        self.root.left.right = TreeNode(5)

    def test_inorder_traversal(self):
        result = inorder_traversal(self.root)
        self.assertEqual(result, [4, 2, 5, 1, 3])

    def test_preorder_traversal(self):
        result = preorder_traversal(self.root)
        self.assertEqual(result, [1, 2, 4, 5, 3])

    def test_postorder_traversal(self):
        result = postorder_traversal(self.root)
        self.assertEqual(result, [4, 5, 2, 3, 1])

    def test_level_order_traversal(self):
        result = level_order_traversal(self.root)
        self.assertEqual(result, [1, 2, 3, 4, 5])

    def test_tree_height(self):
        height = tree_height(self.root)
        self.assertEqual(height, 3)

    def test_is_balanced(self):
        balanced = is_balanced(self.root)
        self.assertTrue(balanced)

    def test_search_in_bst(self):
        # Создаем BST:
        #     4
        #    / \
        #   2   6
        #  / \ / \
        # 1  3 5  7
        bst_root = TreeNode(4)
        bst_root.left = TreeNode(2)
        bst_root.right = TreeNode(6)
        bst_root.left.left = TreeNode(1)
        bst_root.left.right = TreeNode(3)
        bst_root.right.left = TreeNode(5)
        bst_root.right.right = TreeNode(7)

        node = search_in_bst(bst_root, 3)
        self.assertIsNotNone(node)
        self.assertEqual(node.val, 3)

        node = search_in_bst(bst_root, 8)
        self.assertIsNone(node)


class TestTravellingSalesman(unittest.TestCase):

    def test_brute_force_tsp(self):
        # Тестовая матрица расстояний для 4 городов
        distances = [
            [0, 10, 15, 20],
            [10, 0, 35, 25],
            [15, 35, 0, 30],
            [20, 25, 30, 0]
        ]

        cost, path = brute_force_tsp(distances)
        self.assertEqual(cost, 80)
        self.assertEqual(len(path), 5)  # Путь должен включать начало и конец

    def test_nearest_neighbor_tsp(self):
        distances = [
            [0, 10, 15, 20],
            [10, 0, 35, 25],
            [15, 35, 0, 30],
            [20, 25, 30, 0]
        ]

        cost, path = nearest_neighbor_tsp(distances)
        self.assertEqual(len(path), 5)
        # Проверяем, что путь начинается и заканчивается в городе 0
        self.assertEqual(path[0], 0)
        self.assertEqual(path[-1], 0)

    def test_dynamic_tsp(self):
        distances = [
            [0, 10, 15, 20],
            [10, 0, 35, 25],
            [15, 35, 0, 30],
            [20, 25, 30, 0]
        ]

        cost, path = dynamic_tsp(distances)
        self.assertEqual(cost, 80)
        self.assertEqual(len(path), 5)


if __name__ == '__main__':
    unittest.main()
