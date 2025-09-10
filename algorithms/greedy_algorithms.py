def activity_selection(activities):
    """
    Жадный алгоритм выбора активностей

    Выбирает максимальное количество непересекающихся активностей, 
    у которых время окончания меньше или равно времени начала следующей.

    Сложность: O(n log n) - из-за сортировки

    Args:
        activities (list): Список кортежей (начало, конец, название) активностей

    Returns:
        list: Список выбранных активностей

    Example:
        >>> activities = [(1, 4, 'A'), (3, 5, 'B'), (0, 6, 'C'), (5, 7, 'D')]
        >>> activity_selection(activities)
        [(1, 4, 'A'), (5, 7, 'D')]
    """
    # Сортируем по времени окончания
    sorted_activities = sorted(activities, key=lambda x: x[1])

    selected = [sorted_activities[0]]
    last_end_time = sorted_activities[0][1]

    for i in range(1, len(sorted_activities)):
        start_time = sorted_activities[i][0]

        if start_time >= last_end_time:
            selected.append(sorted_activities[i])
            last_end_time = sorted_activities[i][1]

    return selected


def fractional_knapsack(items, capacity):
    """
    Жадный алгоритм для задачи о рюкзаке (дробная версия)

    Выбирает предметы с наибольшим соотношением ценности к весу,
    при этом можно брать дроби предметов.

    Сложность: O(n log n) - из-за сортировки

    Args:
        items (list): Список кортежей (вес, ценность, название) предметов
        capacity (int): Вместимость рюкзака

    Returns:
        tuple: (максимальная ценность, список выбранных предметов)

    Example:
        >>> items = [(10, 60, 'A'), (20, 100, 'B'), (30, 120, 'C')]
        >>> fractional_knapsack(items, 50)
        (240.0, [('A', 10), ('B', 20), ('C', 20)])
    """
    # Сортируем по соотношению ценности к весу (убывающим)
    sorted_items = sorted(items, key=lambda x: x[1]/x[0], reverse=True)

    total_value = 0
    selected_items = []

    for weight, value, name in sorted_items:
        if capacity >= weight:
            # Берем полностью предмет
            capacity -= weight
            total_value += value
            selected_items.append((name, weight))
        else:
            # Берем дробь предмета
            fraction = capacity / weight
            total_value += value * fraction
            selected_items.append((name, capacity))
            capacity = 0
            break

    return total_value, selected_items


def coin_change_greedy(coins, amount):
    """
    Жадный алгоритм для задачи о сдаче

    Выбирает минимальное количество монет для формирования суммы.
    Работает корректно только для стандартных систем монет (например, в США).

    Сложность: O(n) - где n количество типов монет

    Args:
        coins (list): Список номиналов монет (в порядке убывания)
        amount (int): Сумма для формирования

    Returns:
        list: Список использованных монет

    Example:
        >>> coin_change_greedy([25, 10, 5, 1], 67)
        [25, 25, 10, 5, 1, 1]
    """
    result = []

    for coin in coins:
        count = amount // coin
        if count > 0:
            result.extend([coin] * count)
            amount -= coin * count

    return result
