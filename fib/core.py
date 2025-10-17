"""Core Fibonacci logic."""


def fibonacci(n: int) -> int:
    """Return the nth Fibonacci number.

    Parameters
    ----------
    n: int
        Non-negative index of the Fibonacci sequence.

    Returns
    -------
    int
        The Fibonacci number at position n.

    Raises
    ------
    ValueError
        If n is negative.
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def fibonacci_sequence(length: int) -> list[int]:
    """Return the first ``length`` Fibonacci numbers as a list.

    Parameters
    ----------
    length: int
        The number of Fibonacci values to include starting from ``F(0)``.

    Returns
    -------
    list[int]
        The requested prefix of the Fibonacci sequence.

    Raises
    ------
    ValueError
        If ``length`` is negative.
    """

    if length < 0:
        raise ValueError("length must be non-negative")

    sequence: list[int] = []
    a, b = 0, 1
    for _ in range(length):
        sequence.append(a)
        a, b = b, a + b
    return sequence
