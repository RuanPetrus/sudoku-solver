from sys import argv
from math import sqrt
from random import sample

from typing import Dict, Tuple, List, Set, Any, Optional, Sized
from collections.abc import Iterable

BLANK = 0

# Defining graph representation
Cell = int
Color = int
Graph = Dict[Cell, Tuple[Color, Set[Cell]]]


# Printing functions


def usage():
    """Print usage"""
    print("Sudoku solver and generator")
    print("USAGE: python main.py <command>")
    print(
        """EX:
          python main.py check_valid example_board.txt 3
          python main.py solve 3 20"""
    )
    print(
        """COMMANDS:
          check_valid <file_path> <base>
          solve <base> <number_of_empty_squares>"""
    )


def print_graph(graph: Graph):
    """Print graph like an adjancency list"""
    for key in graph.keys():
        print(f"{key}({graph[key][0]}): {sorted(graph[key][1])}")


def divide_list(l: List[Any], size: int) -> List[List[Any]]:
    """Divide len(l) list into a sizexsize list"""
    new_list = []
    for n in range(0, len(l), size):
        new_list.append(l[n : n + size])

    return new_list


def print_simple_board(board: Graph):
    side = int(sqrt(len(board)))
    nums_list = [str(board[n][0]) for n in board.keys()]
    nums = divide_list(nums_list, side)

    for line in nums:
        print(" ".join(line))


def board_to_string(board: Graph):
    """Generates a string represantation of a board"""
    side = int(sqrt(len(board)))
    base = int(sqrt(side))

    line0 = expandLine("╔═══╤═══╦═══╗", base)
    line1 = expandLine("║ . │ . ║ . ║", base)
    line2 = expandLine("╟───┼───╫───╢", base)
    line3 = expandLine("╠═══╪═══╬═══╣", base)
    line4 = expandLine("╚═══╧═══╩═══╝", base)

    symbols = " 1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    nums_list = [symbols[board[n][0]] for n in sorted(board.keys())]
    nums = [[""] + l for l in divide_list(nums_list, side)]

    str_board = []
    str_board.append(line0)
    for r in range(1, side + 1):
        str_board.append("".join(n + s for n, s in zip(nums[r - 1], line1.split("."))))
        str_board.append([line2, line3, line4][(r % side == 0) + (r % base == 0)])

    return "\n".join(str_board)


def expandLine(line: str, base: int):
    """Expand a line so fit well in terminal"""
    return line[0] + line[5:9].join([line[1:5] * (base - 1)] * base) + line[9:13]


def file_to_graph(input_path: str, base: int):
    """Read a file and generates a graph"""
    size = base * base

    list_of_values = []

    with open(input_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip() != ""]
        for line in lines:
            for number in line.split(" "):
                if number.isnumeric():
                    list_of_values.append(int(number))

    return matrix_to_graph(divide_list(list_of_values, size))


def gen_square(row: int, column: int, square_len: int) -> List[int]:
    """Generate sudoku squares from row and column"""
    square = []
    for k in range(square_len):
        index = (
            (((row * square_len) + k) * square_len * square_len)
            + (column * square_len)
            + 1
        )
        for l in range(square_len):
            square.append(index + l)

    return square


def generate_neighbors(i: int, j: int, matrix_len: int) -> Set[int]:
    """Generate neighbors from i and j"""
    square_len = int(sqrt(matrix_len))
    first_row_index = (i * matrix_len) + 1
    row_neighbors = [n for n in range(first_row_index, first_row_index + matrix_len)]

    column_neighbors = [(n * matrix_len) + j + 1 for n in range(matrix_len)]

    square_neighbors = gen_square(i // square_len, j // square_len, square_len)

    return set(row_neighbors + column_neighbors + square_neighbors)


def matrix_to_graph(matrix: List[List[int]]) -> Graph:
    """Generate a graph representation of a sudoku matrix"""
    graph = {}
    matrix_len = len(matrix)

    for i in range(matrix_len):
        for j in range(matrix_len):
            # Calculating keys
            key = (i * matrix_len) + j + 1

            full_neighbors = set(generate_neighbors(i, j, matrix_len) - set([key]))
            graph[key] = (matrix[i][j], full_neighbors)

    # adding rows neighbor and columns neighbor

    return graph


def get_cell_color(board: Graph, cell: Cell) -> Color:
    """Return cell color"""
    return board[cell][0]


def get_cell_neighbors(board: Graph, cell: Cell) -> Iterable:
    """Return cell neighbors"""
    return board[cell][1]


def is_board_valid(board: Graph) -> bool:
    """Return True if board is valid, else return False"""
    for cell in board.keys():
        color = get_cell_color(board, cell)
        if color == BLANK:
            continue

        for neighbor in get_cell_neighbors(board, cell):
            if color == get_cell_color(board, neighbor):
                return False

    return True


def try_color_graph(
    board: Graph, colors: Set[Any]
) -> Tuple[Optional[Graph], List[str]]:
    """Color algorithm in a graph"""
    blank_vertices_list = [v for v in board.keys() if board[v][0] == BLANK]

    available_colors = {}

    steps_in_strings = []

    for v in blank_vertices_list:
        for color in colors:
            available_colors[color] = True

        neighbors = board[v][1]

        for n in neighbors:
            n_color = board[n][0]
            if n_color != BLANK:
                available_colors[n_color] = False

        current_color = None

        for color in available_colors.keys():
            if available_colors[color]:
                current_color = color

        if current_color is None:
            return None, []

        board[v] = (current_color, board[v][1])

        steps_in_strings.append(board_to_string(board))

    return board, steps_in_strings


def pattern(row: int, collumn: int, base: int):
    """Generate sudoku pattern from row and column"""
    side = base * base
    return (base * (row % base) + row // base + collumn) % side


def shuffle(s: Sized):
    """Shufle a list from another list"""
    return sample(s, len(s))


def generate_random_full_board(base: int) -> List[List[int]]:
    """Generates a full random board of a valid sudoku"""
    # randomize rows, columns and numbers (of valid base pattern)
    rBase = range(base)
    rows = [g * base + r for g in shuffle(rBase) for r in shuffle(rBase)]
    cols = [g * base + c for g in shuffle(rBase) for c in shuffle(rBase)]
    nums = shuffle(range(1, base * base + 1))

    # produce board using randomized baseline pattern
    board = [[nums[pattern(r, c, base)] for c in cols] for r in rows]

    return board


def remove_squares_from_board(
    board: List[List[int]], base: int, empties: int
) -> List[List[int]]:
    """Remove some squares from a board"""
    side = base * base
    squares = side * side
    for p in sample(range(squares), empties):
        board[p // side][p % side] = 0

    return board


def generate_and_solve_sudoku_game(
    base: int, empties: int
) -> Tuple[Graph, Graph, List[str]]:
    """Generate a valid solvable sudoku game"""
    board = None
    while board is None:
        board_matrix = generate_random_full_board(base)
        empty_board_matrix = remove_squares_from_board(board_matrix, base, empties)
        board, steps = try_color_graph(
            matrix_to_graph(empty_board_matrix), set(range(1, 10))
        )

    return matrix_to_graph(empty_board_matrix), board, steps


def main(args: List[str]):

    commands = ["check_valid", "solve"]

    if len(args) < 4:
        usage()
        exit(1)

    if args[1] not in commands:
        usage()
        exit(1)

    if args[1] == "check_valid":
        base = int(args[3])
        graph = file_to_graph(args[2], base)
        valid = is_board_valid(graph)

        print("\n-----------------------------------")
        print("SUDOKU GENERATOR AND SOLVER\n")
        print("BOARD:")
        print(board_to_string(graph))
        print(f"VALID = {valid}")

    elif args[1] == "solve":
        base = int(args[2])
        empty_values = int(args[3])

        board, solved_board, steps = generate_and_solve_sudoku_game(base, empty_values)

        if is_board_valid(solved_board):
            # Sudoku board generator
            print("\n-----------------------------------")
            print("SUDOKU GENERATOR AND SOLVER")
            print(
                f"\nBoard {base * base}x{base * base} with {empty_values} empty squares:"
            )
            print(board_to_string(board))

            print("\nSOLVER")
            for i, b in enumerate(steps):
                print(f"step {i + 1}:")
                print(b)
                print()

        else:
            main()


if __name__ == "__main__":
    main(argv)


#  1  2  3  4          1: 2 3 4 5 9 13 6
#  5  6  7  8     ->   2: 1 3 4 6 10 14 5
#  9 10 11 12          3: 1 2 4 7 11 15 8
# 13 14 15 16
