import typer
from statistics import mean
from Matrix.matrix import main
from collections import defaultdict

app = typer.Typer()


@app.callback()
def callback():
    """
    此應用程式為測試 multithreading 所建，具體上是做矩陣乘法。並分別比較 for-loop, using threads by cells, using threads by rows 之速度與平均值。
    """


@app.command()
def test(
    matrix_m: int = typer.Option(35, prompt="請設置矩陣 M 列長度"),
    matrix_n: int = typer.Option(60, prompt="請設置舉列 N 行長度"),
):
    dd = defaultdict(list)
    test_time = 3
    a_b1_diffs = []
    a_b2_diffs = []
    for i in range(test_time):
        typer.secho(f"第 {i+1} 次測試", fg=typer.colors.MAGENTA)
        main(matrix_m, matrix_n, measure_dict=dd)
        a_b1_diff = (
            dd["for_loops_matrix_multiplication"][i]
            - dd["by_cell_matrix_multiplication"][i]
        )
        a_b2_diff = (
            dd["for_loops_matrix_multiplication"][i]
            - dd["by_row_matrix_multiplication"][i]
        )
        a_b1_diffs.append(a_b1_diff)
        a_b2_diffs.append(a_b2_diff)

        typer.secho(
            f"耗時時間差 `for-loop` - `by cells` time = {a_b1_diff:.5f} ms",
            fg=typer.colors.CYAN,
        )
        typer.secho(
            f"耗時時間差 `for-loop` - `by rows` time = {a_b2_diff:.5f} ms",
            fg=typer.colors.BRIGHT_CYAN,
        )

    typer.secho(f"以下為做 {test_time} 次之平均時間", fg=typer.colors.BRIGHT_BLACK)
    typer.secho(
        f'for_loops_matrix_multiplication 平均時間為 {mean(dd["for_loops_matrix_multiplication"]):.5f} ms',
        fg=typer.colors.BRIGHT_BLUE,
    )
    typer.secho(
        f'by_cell_matrix_multiplication 平均時間為 {mean(dd["by_cell_matrix_multiplication"]):.5f} ms',
        fg=typer.colors.BRIGHT_YELLOW,
    )
    typer.secho(
        f'by_row_matrix_multiplication 平均時間為 {mean(dd["by_row_matrix_multiplication"]):.5f} ms',
        fg=typer.colors.BRIGHT_GREEN,
    )
    typer.secho(
        f"耗時平均時間差 mean(`for-loop` - `by cells`) = {mean(a_b1_diffs):.5f} ms",
        fg=typer.colors.BRIGHT_MAGENTA,
    )
    typer.secho(
        f"耗時平均時間差 mean(`for-loop` - `by rows`) = {mean(a_b2_diffs):.5f} ms",
        fg=typer.colors.BRIGHT_RED,
    )
