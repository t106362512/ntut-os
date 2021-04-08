import logging
from decimal import Decimal
from typing import List, Dict, Optional
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED
from Matrix.helper import (
    Matrix,
    MatrixEquation,
    equation,
    zero_matrix_generator,
    matrix_printer,
    measure,
)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@measure
def for_loops_matrix_multiplication(
    matrix_1: Matrix,
    matrix_2: Matrix,
    start_row: Optional[int] = None,
    end_row: Optional[int] = None,
    **kwargs,
) -> List:
    matrix = zero_matrix_generator(matrix_1.m)
    calc_row = (
        (start_row, end_row)
        if isinstance(start_row, int) and isinstance(end_row, int)
        else [matrix_1.m]
    )
    for i in range(*calc_row):
        for j in range(matrix_1.m):
            for k in range(matrix_1.n):
                matrix[i][j] += equation(i, k, matrix_1.matrix_equation) * equation(
                    k, j, matrix_2.matrix_equation
                )
    logger.debug(f"sr:{start_row}, er:{end_row}, {matrix}")
    return matrix


@measure
def by_row_matrix_multiplication(
    matrix_1: Matrix, matrix_2: Matrix, num_of_threads: Optional[int] = None, **kwargs
) -> List:
    t = num_of_threads or matrix_1.m
    with ThreadPoolExecutor(max_workers=t) as executor:
        jobs = [
            executor.submit(
                for_loops_matrix_multiplication,
                matrix_1,
                matrix_2,
                int(matrix_1.m / t) * n,
                int(matrix_2.n / t) * (n + 1),
                log_time_enable=False,
            )
            for n in range(t)
        ]
        return [v[i] for i, v in enumerate([r.result() for r in jobs])]


@measure
def by_cell_matrix_multiplication(
    matrix_1: Matrix, matrix_2: Matrix, num_of_threads: Optional[int] = None, **kwargs
) -> List:
    t = num_of_threads or matrix_1.m * matrix_1.n
    matrix = zero_matrix_generator(matrix_1.m)

    def matrix_multi(row, col):
        for k in range(matrix_1.m):
            matrix[row][k] += equation(row, col, matrix_1.matrix_equation) * equation(
                col, k, matrix_2.matrix_equation
            )

    with ThreadPoolExecutor(max_workers=t) as executor:
        jobs = []
        for i in range(matrix_1.m):
            for j in range(matrix_1.n):
                jobs.append(executor.submit(matrix_multi, i, j))
        wait(jobs, return_when=ALL_COMPLETED)
        return matrix


def main(
    m: int = 35, n: int = 60, measure_dict: Dict = dict, list_matrix: bool = False
) -> Dict:
    param = {
        "matrix_1": Matrix(
            m,
            n,
            MatrixEquation(coefficient_1=Decimal(3.5), coefficient_2=Decimal(-6.6)),
        ),
        "matrix_2": Matrix(
            n,
            m,
            MatrixEquation(
                coefficient_1=Decimal(8.8),
                coefficient_2=Decimal(-3.5),
                constant=Decimal(6.6),
            ),
        ),
        "log_time": measure_dict,
    }

    if list_matrix:
        matrix_printer(for_loops_matrix_multiplication(**param), float_fmt=0.5)
        matrix_printer(by_cell_matrix_multiplication(**param), float_fmt=0.5)
        matrix_printer(by_row_matrix_multiplication(**param), float_fmt=0.5)
    else:
        for_loops_matrix_multiplication(**param)
        by_cell_matrix_multiplication(**param)
        by_row_matrix_multiplication(**param)

    return measure_dict
