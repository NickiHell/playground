class TreeNode:
    """Узел бинарного дерева"""
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def inorder_traversal(root):
    """
    Обход дерева в порядке (inorder traversal)

    Проходит по дереву в порядке: левое поддерево, корень, правое поддерево

    Сложность: O(n) где n - количество узлов

    Args:
        root (TreeNode): Корень дерева

    Returns:
        list: Список значений узлов в порядке обхода

    Example:
        >>> root = TreeNode(1)
        >>> root.right = TreeNode(2)
        >>> root.right.left = TreeNode(3)
        >>> inorder_traversal(root)
        [1, 3, 2]
    """
    result = []

    def traverse(node):
        if node:
            traverse(node.left)
            result.append(node.val)
            traverse(node.right)

    traverse(root)
    return result


def preorder_traversal(root):
    """
    Обход дерева в прямом порядке (preorder traversal)

    Проходит по дереву в порядке: корень, левое поддерево, правое поддерево

    Сложность: O(n) где n - количество узлов

    Args:
        root (TreeNode): Корень дерева

    Returns:
        list: Список значений узлов в порядке обхода

    Example:
        >>> root = TreeNode(1)
        >>> root.right = TreeNode(2)
        >>> root.right.left = TreeNode(3)
        >>> preorder_traversal(root)
        [1, 2, 3]
    """
    result = []

    def traverse(node):
        if node:
            result.append(node.val)
            traverse(node.left)
            traverse(node.right)

    traverse(root)
    return result


def postorder_traversal(root):
    """
    Обход дерева в обратном порядке (postorder traversal)

    Проходит по дереву в порядке: левое поддерево, правое поддерево, корень

    Сложность: O(n) где n - количество узлов

    Args:
        root (TreeNode): Корень дерева

    Returns:
        list: Список значений узлов в порядке обхода

    Example:
        >>> root = TreeNode(1)
        >>> root.right = TreeNode(2)
        >>> root.right.left = TreeNode(3)
        >>> postorder_traversal(root)
        [3, 2, 1]
    """
    result = []

    def traverse(node):
        if node:
            traverse(node.left)
            traverse(node.right)
            result.append(node.val)

    traverse(root)
    return result


def level_order_traversal(root):
    """
    Обход дерева по уровням (BFS)

    Проходит по дереву уровень за уровнем слева направо

    Сложность: O(n) где n - количество узлов

    Args:
        root (TreeNode): Корень дерева

    Returns:
        list: Список значений узлов в порядке обхода по уровням

    Example:
        >>> root = TreeNode(3)
        >>> root.left = TreeNode(9)
        >>> root.right = TreeNode(20)
        >>> root.right.left = TreeNode(15)
        >>> root.right.right = TreeNode(7)
        >>> level_order_traversal(root)
        [3, 9, 20, 15, 7]
    """
    from collections import deque

    if not root:
        return []

    result = []
    queue = deque([root])

    while queue:
        node = queue.popleft()
        result.append(node.val)

        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)

    return result


def tree_height(root):
    """
    Вычисление высоты дерева

    Сложность: O(n) где n - количество узлов

    Args:
        root (TreeNode): Корень дерева

    Returns:
        int: Высота дерева

    Example:
        >>> root = TreeNode(1)
        >>> root.left = TreeNode(2)
        >>> root.right = TreeNode(3)
        >>> tree_height(root)
        2
    """
    if not root:
        return 0

    left_height = tree_height(root.left)
    right_height = tree_height(root.right)

    return max(left_height, right_height) + 1


def is_balanced(root):
    """
    Проверка баланса дерева

    Дерево считается сбалансированным, если разница высот поддеревьев 
    для каждого узла не превышает 1.

    Сложность: O(n^2) в худшем случае, O(n) в среднем случае

    Args:
        root (TreeNode): Корень дерева

    Returns:
        bool: True если дерево сбалансировано, False в противном случае

    Example:
        >>> root = TreeNode(1)
        >>> root.left = TreeNode(2)
        >>> root.right = TreeNode(3)
        >>> is_balanced(root)
        True
    """
    def check_height(node):
        if not node:
            return 0

        left_height = check_height(node.left)
        right_height = check_height(node.right)

        if left_height == -1 or right_height == -1 or abs(left_height - right_height) > 1:
            return -1

        return max(left_height, right_height) + 1

    return check_height(root) != -1


def search_in_bst(root, val):
    """
    Поиск значения в бинарном дереве поиска

    Использует свойство BST: левое поддерево содержит значения меньше узла,
    правое поддерево содержит значения больше узла.

    Сложность: O(log n) в среднем случае, O(n) в худшем случае

    Args:
        root (TreeNode): Корень дерева
        val: Значение для поиска

    Returns:
        TreeNode: Узел с найденным значением или None

    Example:
        >>> root = TreeNode(4)
        >>> root.left = TreeNode(2)
        >>> root.right = TreeNode(6)
        >>> node = search_in_bst(root, 2)
        >>> node.val if node else None
        2
    """
    if not root or root.val == val:
        return root

    if val < root.val:
        return search_in_bst(root.left, val)
    else:
        return search_in_bst(root.right, val)
