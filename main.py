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
          python main.py sol example_board.txt 3
          python main.py gen 3 20
          python main.py genAndSol 3 20"""
    )
    print(
        """COMMANDS:
          solve <file_path> <base>
          generate <base> <number_of_empty_squares>
          genAndSol <base> <number_of_empty_squares>"""
    )


def print_graph(graph: Graph):
    """Print graph like an adjancency list"""
    for key in graph.keys():
        print(f"{key}({graph[key][0]}): {sorted(graph[key][1])}")


def divide_list(l: List[Any], size: int) -> List[List[Any]]:
    """Divide len(l) list into a size x size list"""
    new_list = []
    for n in range(0, len(l), size):
        new_list.append(l[n : n + size])

    return new_list


def print_simple_board(board: Graph):
    """Print board in a simple way for debug"""
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

    symbols = " 123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

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


def set_cell_color(board: Graph, cell: Cell, color: Color) -> Graph:
    """Set color to new board and return a new one"""
    new_board = board.copy()
    new_board[cell] = (color, new_board[cell][1])
    return new_board


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


def get_empty_squares(board: Graph) -> List[Cell]:
    return [cell for cell in board.keys() if board[cell][0] == BLANK]


def can_color(board: Graph, cell: Cell, color: Color) -> bool:
    for neighbor in get_cell_neighbors(board, cell):
        if get_cell_color(board, neighbor) == color:
            return False

    return True


def back_track_solution(
    board: Graph, colors: Set[Color], steps: List[str] = []
) -> Tuple[bool, Graph, List[str]]:
    """Performs a back_track algorithm tring to color the board"""

    # if board has none empty squares return board
    empty_squares = get_empty_squares(board)
    if len(empty_squares) == 0:
        return is_board_valid(board), board, steps

    cell_to_color = empty_squares[0]

    # Try every color that works
    for col in colors:
        if can_color(board, cell_to_color, col):
            new_board = set_cell_color(board, cell_to_color, col)
            possible_to_solve, solved_board, steps = back_track_solution(
                new_board, colors, steps
            )

            # Check if no need to Back track
            if possible_to_solve:
                return True, solved_board, [board_to_string(new_board)] + steps

    # Back track
    return False, board, steps


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


def generate_sudoku_game(base: int, empties: int) -> Tuple[Graph]:
    """Generate a valid solvable sudoku game"""
    board_matrix = generate_random_full_board(base)
    empty_board_matrix = remove_squares_from_board(board_matrix, base, empties)

    return matrix_to_graph(empty_board_matrix)


def main(args: List[str]):

    commands = ["sol", "gen", "genAndSol"]

    if len(args) < 4:
        usage()
        exit(1)

    if args[1] not in commands:
        usage()
        exit(1)

    if args[1] == "sol":
        base = int(args[3])
        graph = file_to_graph(args[2], base)
        valid, _, steps = back_track_solution(graph, set(range(1, (base * base) + 1)))

        print("\n-----------------------------------")
        print("SUDOKU SOLVER\n")
        print("BOARD:")
        print(board_to_string(graph))
        print(f"VALID = {valid}")

        if valid:
            print("\nSOLVER")
            for i, b in enumerate(steps):
                print(f"step {i + 1}:")
                print(b)
                print()

    elif args[1] == "gen":
        base = int(args[2])
        empty_values = int(args[3])

        board = generate_sudoku_game(base, empty_values)
        print("\n-----------------------------------")
        print("SUDOKU GENERATOR")
        print(f"\nBoard {base * base}x{base * base} with {empty_values} empty squares:")
        print(board_to_string(board))

    elif args[1] == "genAndSol":
        base = int(args[2])
        empty_values = int(args[3])

        board = generate_sudoku_game(base, empty_values)
        print("\n-----------------------------------")
        print("SUDOKU GENERATOR AND SOLVER")
        print(f"\nBoard {base * base}x{base * base} with {empty_values} empty squares:")
        print(board_to_string(board))

        _, _, steps = back_track_solution(board, set(range(1, (base * base) + 1)))
        print("\nSOLVER")
        for i, b in enumerate(steps):
            print(f"step {i + 1}:")
            print(b)
            print()


if __name__ == "__main__":
    main(argv)
