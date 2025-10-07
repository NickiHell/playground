# Poor solution O(n2)
def find_single_number_poor(numbers: list[int]) -> int:
    already_seen: set[int] = set()  # set is hash map O(1) in better case
    for number in numbers:
        if number in already_seen:
            already_seen.remove(number)
        else:
            already_seen.add(number)
    return already_seen.pop()


# Better solution O(n)
def find_single_number_best(numbers: list[int]) -> int:
    result = 0
    for number in numbers:
        result ^= number
    return result


def test_find_single_number_solutions() -> None:
    test_cases = [
        [1, 2, 3, 1, 2],
        [5, 5, 2, 2, 8],
        [1, 1, 2, 2, 3, 3, 4],
    ]

    print("Poor solution")
    for test in test_cases:
        result = find_single_number_poor(test)
        print(f"Input: {test}")
        print(f"Output: {result}\n")

    print("Best Solution")
    for test in test_cases:
        result = find_single_number_poor(test)
        print(f"Input: {test}")
        print(f"Output: {result}\n")
