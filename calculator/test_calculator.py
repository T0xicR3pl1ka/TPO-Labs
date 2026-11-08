"""
Полные модульные тесты для класса Calculator.
Покрывают все методы: add, subtract, multiply, divide, power, is_prime_number.
Запуск: python -m pytest test_calculator.py -v
"""
import pytest

from calculator import Calculator


# ---------- Фикстура ----------
@pytest.fixture()
def calc():
    """Создает экземпляр калькулятора для каждого теста."""
    return Calculator()


# ============================================================
# add — параметризация
# ============================================================
class TestAdd:
    @pytest.mark.parametrize("a, b, expected", [
        (2, 3, 5),                 # положительные
        (-2, -3, -5),              # отрицательные
        (-2, 3, 1),                # разные знаки
        (0, 7, 7),                 # ноль + число
        (1.5, 2.5, 4.0),           # дробные
    ])
    def test_add(self, calc, a, b, expected):
        assert calc.add(a, b) == expected


# ============================================================
# subtract — параметризация
# ============================================================
class TestSubtract:
    @pytest.mark.parametrize("a, b, expected", [
        (10, 4, 6),
        (4, 10, -6),
        (-5, -5, 0),
        (0, 5, -5),
        (1.5, 0.5, 1.0),
    ])
    def test_subtract(self, calc, a, b, expected):
        assert calc.subtract(a, b) == expected


# ============================================================
# multiply — параметризация
# ============================================================
class TestMultiply:
    @pytest.mark.parametrize("a, b, expected", [
        (6, 7, 42),
        (-6, -7, 42),
        (0, 100, 0),
        (1.5, 2, 3.0),
        (0.5, 0.5, 0.25),
    ])
    def test_multiply(self, calc, a, b, expected):
        assert calc.multiply(a, b) == expected


# ============================================================
# divide — параметризация + проверка исключения
# ============================================================
class TestDivide:
    @pytest.mark.parametrize("a, b, expected", [
        (8, 2, 4.0),
        (10, 4, 2.5),
        (-9, 3, -3.0),
        (0, 5, 0.0),
        (1, 3, pytest.approx(0.333333, rel=1e-5)),
    ])
    def test_divide_valid(self, calc, a, b, expected):
        assert calc.divide(a, b) == expected

    def test_divide_by_zero_raises(self, calc):
        """Деление на ноль возбуждает ZeroDivisionError."""
        with pytest.raises(ZeroDivisionError):
            calc.divide(5, 0)

    def test_divide_by_zero_message(self, calc):
        """Сообщение об ошибке содержит текст про деление на ноль."""
        with pytest.raises(ZeroDivisionError) as exc_info:
            calc.divide(5, 0)
        assert "Деление на ноль" in str(exc_info.value)

    def test_divide_zero_by_zero_raises(self, calc):
        """0 / 0 также возбуждает ZeroDivisionError."""
        with pytest.raises(ZeroDivisionError):
            calc.divide(0, 0)

    def test_divide_negative_by_zero_raises(self, calc):
        """Отрицательное / 0 тоже возбуждает ZeroDivisionError."""
        with pytest.raises(ZeroDivisionError):
            calc.divide(-5, 0)


# ============================================================
# power — параметризация
# ============================================================
class TestPower:
    @pytest.mark.parametrize("base, exp, expected", [
        (2, 3, 8),
        (5, 0, 1),
        (2, -1, 0.5),
        (-2, 2, 4),
        (0, 5, 0),
        (0, 0, 1),
    ])
    def test_power(self, calc, base, exp, expected):
        assert calc.power(base, exp) == expected


# ============================================================
# is_prime_number — параметризация
# ============================================================
class TestIsPrimeNumber:
    @pytest.mark.parametrize("n, expected", [
        # простые
        (2, True),
        (5, True),
        (11, True),
        (13, True),
        (97, True),
        (7919, True),       # простое, проверка на большом числе
        # не простые
        (0, False),
        (1, False),
        (6, False),
        (8, False),
        (49, False),
        (100, False),
        (99, False),
        # отрицательные
        (-7, False),
        (-2, False),
    ])
    def test_is_prime_number(self, calc, n, expected):
        assert calc.is_prime_number(n) == expected

    def test_is_prime_number_string_raises(self, calc):
        """Строка вместо числа возбуждает TypeError."""
        with pytest.raises(TypeError):
            calc.is_prime_number("7")

    def test_is_prime_number_float_raises(self, calc):
        """Дробное число возбуждает TypeError."""
        with pytest.raises(TypeError):
            calc.is_prime_number(7.5)

    def test_is_prime_number_bool_raises(self, calc):
        """bool — подкласс int, но не должен приниматься."""
        with pytest.raises(TypeError):
            calc.is_prime_number(True)

    def test_is_prime_number_none_raises(self, calc):
        """None возбуждает TypeError."""
        with pytest.raises(TypeError):
            calc.is_prime_number(None)

    def test_is_prime_number_message(self, calc):
        """Сообщение об ошибке типа содержит пояснение."""
        with pytest.raises(TypeError) as exc_info:
            calc.is_prime_number("7")
        assert "целым числом" in str(exc_info.value)