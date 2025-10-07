def find_single_number_with_steps(numbers: list[int]) -> int:
    result = 0
    print(f"Initial result = {result}")

    for number in numbers:
        print(f"XOR {result} ^ {number}", end=" = ")
        result ^= number
        print(result)

    return result


def test_xor():
    test = [1, 2, 3, 1, 2]
    print(f"\nИщем одиночное число в {test}")
    result = find_single_number_with_steps(test)
    print(f"\nРезультат: {result}")

    # Показываем, что работает для разных чисел
    print("\nБинарное представление:")
    print(f"1 в двоичной системе:   {bin(1)[2:]:>8}")
    print(f"2 в двоичной системе:   {bin(2)[2:]:>8}")
    print(f"3 в двоичной системе:   {bin(3)[2:]:>8}")
