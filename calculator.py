print("=== КАЛЬКУЛЯТОР ===")

num1 = float(input("Введите первое число: "))
operator = input("Введите операцию (+, -, *, /): ")
num2 = float(input("Введите второе число: "))

if operator == "+":
    result = num1 + num2
elif operator == "-":
    result = num1 - num2
elif operator == "*":
    result = num1 * num2
elif operator == "/":
    if num2 == 0:
        print("Ошибка: деление на ноль!")
        exit()
    result = num1 / num2
else:
    print("Ошибка: неизвестная операция!")
    exit()

print("Результат:", result)
