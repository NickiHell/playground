def merge_sort(arr):
    """
    Сортировка слиянием (алгоритм "разделяй и властвуй")

    Рекурсивно разделяет массив на две половины, сортирует их отдельно,
    а затем объединяет отсортированные части.

    Сложность: O(n log n)

    Args:
        arr (list): Список чисел для сортировки

    Returns:
        list: Отсортированный список

    Example:
        >>> merge_sort([64, 34, 25, 12, 22, 11, 90])
        [11, 12, 22, 25, 34, 64, 90]
    """
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)


def merge(left, right):
    """
    Вспомогательная функция для сортировки слиянием

    Объединяет два отсортированных массива в один отсортированный.

    Args:
        left (list): Левый отсортированный массив
        right (list): Правый отсортированный массив

    Returns:
        list: Объединенный отсортированный массив
    """
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])

    return result


def power(base, exp):
    """
    Быстрое возведение в степень (алгоритм "разделяй и властвуй")

    Вычисляет base^exp используя рекурсивное деление показателя степени пополам.

    Сложность: O(log n)

    Args:
        base (int): Основание
        exp (int): Показатель степени

    Returns:
        int: Результат возведения в степень

    Example:
        >>> power(2, 10)
        1024
    """
    if exp == 0:
        return 1
    if exp == 1:
        return base

    half = power(base, exp // 2)

    if exp % 2 == 0:
        return half * half
    else:
        return base * half * half


def max_subarray_sum(arr):
    """
    Максимальная сумма подмассива (алгоритм "разделяй и властвуй")

    Находит максимальную сумму непустого подмассива с использованием
    рекурсивного подхода: максимальная сумма либо в левой части, либо в правой,
    либо пересекает середину.

    Сложность: O(n log n)

    Args:
        arr (list): Список чисел

    Returns:
        int: Максимальная сумма подмассива

    Example:
        >>> max_subarray_sum([-2, 1, -3, 4, -1, 2, 1, -5, 4])
        6
    """
    if len(arr) == 1:
        return arr[0]

    mid = len(arr) // 2
    left_sum = max_subarray_sum(arr[:mid])
    right_sum = max_subarray_sum(arr[mid:])

    # Максимальная сумма, пересекающая середину
    left_max = float("-inf")
    current_sum = 0

    for i in range(mid - 1, -1, -1):
        current_sum += arr[i]
        left_max = max(left_max, current_sum)

    right_max = float("-inf")
    current_sum = 0

    for i in range(mid, len(arr)):
        current_sum += arr[i]
        right_max = max(right_max, current_sum)

    cross_sum = left_max + right_max

    return max(left_sum, right_sum, cross_sum)


def find_peak_element(arr):
    """
    Поиск пика в массиве (алгоритм "разделяй и властвуй")

    Пик - элемент, который больше своих соседей. Использует рекурсивный подход
    для поиска пика в массиве.

    Сложность: O(log n)

    Args:
        arr (list): Список чисел

    Returns:
        int: Значение пика

    Example:
        >>> find_peak_element([1, 3, 20, 4, 1, 0])
        20
    """

    def peak_util(arr, low, high, n):
        mid = (low + high) // 2

        # Проверяем, является ли элемент пиком
        if (mid == 0 or arr[mid - 1] <= arr[mid]) and (
            mid == n - 1 or arr[mid + 1] <= arr[mid]
        ):
            return arr[mid]

        # Если левый сосед больше текущего, ищем в левой части
        elif mid > 0 and arr[mid - 1] > arr[mid]:
            return peak_util(arr, low, mid - 1, n)
        else:
            # Иначе ищем в правой части
            return peak_util(arr, mid + 1, high, n)

    if len(arr) == 0:
        return None

    return peak_util(arr, 0, len(arr) - 1, len(arr))
