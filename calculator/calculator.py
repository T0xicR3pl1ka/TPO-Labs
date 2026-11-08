import math


class Calculator:
    """Простой калькулятор с базовыми арифметическими операциями."""

    def add(self, a, b):
        """Сложение двух чисел."""
        return a + b

    def subtract(self, a, b):
        """Вычитание: a - b."""
        return a - b

    def multiply(self, a, b):
        """Умножение двух чисел."""
        return a * b

    def divide(self, a, b):
        """
        Деление a / b.
        Возбуждает ZeroDivisionError при b == 0.
        """
        if b == 0:
            raise ZeroDivisionError("Деление на ноль невозможно")
        return a / b

    def power(self, base, exponent):
        """Возведение base в степень exponent."""
        return base ** exponent

    @staticmethod
    def is_prime_number(n):
        """
        Проверяет, является ли n простым числом.
        Простое число: натуральное > 1, делится только на 1 и себя.
        """
        if not isinstance(n, int) or isinstance(n, bool):
            raise TypeError("Аргумент должен быть целым числом")
        if n < 2:
            return False
        for i in range(2, int(math.isqrt(n)) + 1):
            if n % i == 0:
                return False
        return True


# ============================================================
# Интерактивный консольный режим (выполняется только при
# прямом запуске: python calculator.py)
# ============================================================
def _read_number(prompt: str):
    """Читает число с консоли, повторяет ввод при ошибке."""
    while True:
        raw = input(prompt).strip().replace(",", ".")
        try:
            # Целое, если вводили без точки, иначе float
            return int(raw) if raw.lstrip("-").isdigit() else float(raw)
        except ValueError:
            print("  Ошибка: введите число (например, 5 или 3.14). Попробуйте снова.")


def _interactive_mode() -> None:
    """Интерактивный калькулятор в консоли."""
    calc = Calculator()

    menu = """
==========================================
           КАЛЬКУЛЯТОР
==========================================
  1. Сложение            (+)
  2. Вычитание           (-)
  3. Умножение           (*)
  4. Деление             (/)
  5. Возведение в степень (^)
  6. Проверка на простоту (p)
  0. Выход
==========================================
"""

    print(menu)

    while True:
        choice = input("Выберите операцию (0-6, p): ").strip().lower()

        if choice in ("0", "q", "exit", "выход"):
            print("До свидания!")
            break

        try:
            if choice in ("1", "+", "сложение"):
                a = _read_number("Введите первое число: ")
                b = _read_number("Введите второе число: ")
                print(f"  Результат: {a} + {b} = {calc.add(a, b)}")

            elif choice in ("2", "-", "вычитание"):
                a = _read_number("Введите первое число: ")
                b = _read_number("Введите второе число: ")
                print(f"  Результат: {a} - {b} = {calc.subtract(a, b)}")

            elif choice in ("3", "*", "умножение"):
                a = _read_number("Введите первое число: ")
                b = _read_number("Введите второе число: ")
                print(f"  Результат: {a} * {b} = {calc.multiply(a, b)}")

            elif choice in ("4", "/", "деление"):
                a = _read_number("Введите делимое: ")
                b = _read_number("Введите делитель: ")
                try:
                    print(f"  Результат: {a} / {b} = {calc.divide(a, b)}")
                except ZeroDivisionError as e:
                    print(f"  Ошибка: {e}")

            elif choice in ("5", "^", "степень"):
                base = _read_number("Введите основание: ")
                exp = _read_number("Введите показатель степени: ")
                print(f"  Результат: {base} ^ {exp} = {calc.power(base, exp)}")

            elif choice in ("6", "p", "простота"):
                n = _read_number("Введите целое число: ")
                if not isinstance(n, int):
                    print("  Ошибка: для проверки простоты нужно целое число.")
                else:
                    result = calc.is_prime_number(n)
                    print(f"  Число {n} {'простое' if result else 'не является простым'}")

            else:
                print("  Неизвестная команда. Попробуйте снова.")

        except Exception as e:
            # Страховка от неожиданных ошибок — калькулятор не должен падать
            print(f"  Непредвиденная ошибка: {e}")

        print(menu)


if __name__ == "__main__":
    _interactive_mode()