from __future__ import annotations

import json
import math
from pathlib import Path

HISTORY_FILE = Path(__file__).with_name("calculator_history.json")


def format_number(value: float) -> str:
    return f"{value:.12g}"


def read_number(prompt: str) -> float:
    """Повторяет запрос до корректного конечного числа."""
    while True:
        try:
            value = float(input(prompt).strip().replace(",", "."))
            if not math.isfinite(value):
                raise ValueError
            return value
        except ValueError:
            print("Ошибка: введите конечное число, например 12.5.")


def load_history() -> list[str]:
    try:
        data = json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except (OSError, json.JSONDecodeError):
        return []


def save_history(history: list[str]) -> None:
    try:
        HISTORY_FILE.write_text(json.dumps(history[-100:], ensure_ascii=False, indent=2), encoding="utf-8")
    except OSError:
        print("Не удалось сохранить историю в файл.")


def show_menu() -> None:
    print("""
=== РАСШИРЕННЫЙ КАЛЬКУЛЯТОР ===
Две переменные: +  -  *  /  //  %  **
Одна переменная: sqrt  abs  sin  cos  tan  ln  log10  fact
Служебные команды: history  clear  M+  M-  MR  MC  help  exit
Тригонометрические функции принимают градусы.
""")


def calculate_binary(operation: str, first: float, second: float) -> float:
    operations = {
        "+": lambda: first + second, "-": lambda: first - second,
        "*": lambda: first * second, "/": lambda: first / second,
        "//": lambda: first // second, "%": lambda: first % second,
        "**": lambda: first ** second,
    }
    if operation not in operations:
        raise ValueError("Неизвестная операция.")
    if operation in {"/", "//", "%"} and second == 0:
        raise ZeroDivisionError("Деление на ноль невозможно.")
    result = operations[operation]()
    if isinstance(result, complex) or not math.isfinite(result):
        raise ValueError("Результат не является конечным действительным числом.")
    return result


def calculate_unary(operation: str, number: float) -> float:
    if operation == "sqrt":
        if number < 0:
            raise ValueError("Нельзя извлечь корень из отрицательного числа.")
        return math.sqrt(number)
    if operation == "abs":
        return abs(number)
    if operation in {"sin", "cos", "tan"}:
        radians = math.radians(number)
        if operation == "sin": return math.sin(radians)
        if operation == "cos": return math.cos(radians)
        if math.isclose(math.cos(radians), 0.0, abs_tol=1e-12):
            raise ValueError("Тангенс для этого угла не определён.")
        return math.tan(radians)
    if operation in {"ln", "log10"}:
        if number <= 0:
            raise ValueError("Логарифм определён только для чисел больше нуля.")
        return math.log(number) if operation == "ln" else math.log10(number)
    if operation == "fact":
        if number < 0 or not number.is_integer() or number > 170:
            raise ValueError("Факториал: целое число от 0 до 170.")
        return float(math.factorial(int(number)))
    raise ValueError("Неизвестная операция.")


def show_history(history: list[str]) -> None:
    if not history:
        print("История пока пуста.")
        return
    print("\n--- Последние вычисления ---")
    for index, item in enumerate(history[-20:], start=max(1, len(history) - 19)):
        print(f"{index}. {item}")


def main() -> None:
    history, memory = load_history(), 0.0
    unary = {"sqrt", "abs", "sin", "cos", "tan", "ln", "log10", "fact"}
    binary = {"+", "-", "*", "/", "//", "%", "**"}
    show_menu()

    while True:
        command = input("Операция или команда: ").strip().lower()
        if command in {"exit", "выход", "q"}:
            save_history(history); print("До свидания!"); break
        if command in {"help", "помощь", "?"}:
            show_menu(); continue
        if command in {"history", "история"}:
            show_history(history); continue
        if command == "clear":
            history.clear(); save_history(history); print("История очищена."); continue
        if command == "mr":
            print(f"Память: {format_number(memory)}"); continue
        if command == "mc":
            memory = 0.0; print("Память очищена."); continue
        if command in {"m+", "m-"}:
            value = read_number("Число для памяти: ")
            memory = memory + value if command == "m+" else memory - value
            print(f"Память: {format_number(memory)}"); continue
        try:
            if command in unary:
                number = read_number("Введите число: ")
                result = calculate_unary(command, number)
                record = f"{command}({format_number(number)}) = {format_number(result)}"
            elif command in binary:
                first, second = read_number("Введите первое число: "), read_number("Введите второе число: ")
                result = calculate_binary(command, first, second)
                record = f"{format_number(first)} {command} {format_number(second)} = {format_number(result)}"
            else:
                print("Неизвестная команда. Напишите help, чтобы увидеть список."); continue
        except (ValueError, ZeroDivisionError, OverflowError) as error:
            print(f"Ошибка: {error}"); continue
        history.append(record); save_history(history)
        print(f"Результат: {format_number(result)}")


if __name__ == "__main__":
    main()

