"""Tests for Fibonacci core logic."""
import pytest
from fib.core import fibonacci, fibonacci_sequence


@pytest.mark.parametrize("n,expected", [(0, 0), (1, 1), (5, 5), (10, 55)])
def test_fibonacci_values(n: int, expected: int) -> None:
    assert fibonacci(n) == expected


def test_fibonacci_negative() -> None:
    with pytest.raises(ValueError):
        fibonacci(-1)


@pytest.mark.parametrize(
    "length,expected",
    [
        (0, []),
        (1, [0]),
        (5, [0, 1, 1, 2, 3]),
    ],
)
def test_fibonacci_sequence(length: int, expected: list[int]) -> None:
    assert fibonacci_sequence(length) == expected


def test_fibonacci_sequence_negative() -> None:
    with pytest.raises(ValueError):
        fibonacci_sequence(-1)
