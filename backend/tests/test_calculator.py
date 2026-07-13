import pytest
from app.calculator import Calculator, CalculationError


def test_addition():
    calc = Calculator()
    result = calc.evaluate("2 +3")
    assert result == 5


def test_subtraction():
    calc = Calculator()
    result = calc.evaluate("3- 2")
    assert result == 1


def test_multiplication():
    calc = Calculator()
    result = calc.evaluate("2 * 3")
    assert result == 6


def test_division():
    calc = Calculator()
    result = calc.evaluate("6/3")
    assert result == 2


def test_unary_minus():
    calc = Calculator()
    result = calc.evaluate("-5 +3")
    assert result == -2


def test_division_by_zero():
    calc = Calculator()
    with pytest.raises(CalculationError):
        calc.evaluate("5/0")


def test_invalid_syntax():
    calc = Calculator()
    with pytest.raises(CalculationError):
        calc.evaluate("2 + ")


def test_disallowed_expression():
    calc = Calculator()
    with pytest.raises(CalculationError):
        calc.evaluate("print(1)")
