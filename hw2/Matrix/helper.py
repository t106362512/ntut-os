import time
from typing import List
from decimal import Decimal
from functools import wraps
from dataclasses import dataclass


@dataclass
class MatrixEquation:
    coefficient_1: Decimal
    coefficient_2: Decimal
    constant: Decimal = Decimal(0)


@dataclass
class Matrix:
    m: int
    n: int
    matrix_equation: MatrixEquation


def matrix_printer(matrix: List, float_fmt=0.1) -> None:
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            print(f"{matrix[i][j]:{float_fmt}}", end=" ")
        print()


def equation(i: int, j: int, matrix_equation: MatrixEquation) -> Decimal:
    return (
        matrix_equation.constant
        + matrix_equation.coefficient_1 * (i + 1)
        + matrix_equation.coefficient_2 * (j + 1)
    )


def zero_matrix_generator(n) -> List:
    return [[0] * n for i in range(n)]


def measure(func):
    @wraps(func)
    def _time_it(*args, **kwargs):
        if kwargs.get("log_time_enable", True):
            start = time.time()
            try:
                return func(*args, **kwargs)
            finally:
                end = (time.time() - start) * 1000
                _log_time_saver(end, **kwargs)
        else:
            return func(*args, **kwargs)

    def _log_time_saver(end, **kwargs):
        if "log_time" in kwargs:
            name = kwargs.get("log_name", func.__name__)
            kwargs["log_time"][name].append(end)
        print(f"{func.__name__} total execution time: {end:.5f} ms")

    return _time_it
