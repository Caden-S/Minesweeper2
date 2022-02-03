from random import randrange
from math import ceil


class GameState():
    difficulty = 0
    board = []
    safe_area = []


def play(Game):
    Game.difficulty = int(input("Select the difficulty (1-3): ")) - 1
    Game.board = create_board(Game.difficulty)
    Game.safe_area = get_safe_area(Game)
    Game.bomb_list = [place_bomb(Game) for x in range(0, get_bomb_count(Game.difficulty))]

    board_print(Game)


def board_print(Game):
    new_board = [ [bomb_count(Game,row,col) for row in board_size(Game.board) - 1] for col in row]
    for row in new_board:
        print(row)

def board_size(board):
    return (len(board[1]), len(board[0]))

def create_board(difficulty):
    # returns board with x rows and y columns
    num_rows = get_board_rows(difficulty)
    num_cols = get_board_cols(difficulty)
    return [[0 for x in range(0, num_rows)] for y in range(0, num_cols)]


def get_board_rows(difficulty):
    sizes = [[8, 9, 10], [13, 14, 15], [16, 16, 16]]
    return sizes[difficulty][randrange(0, 3)]


def get_board_cols(difficulty):
    sizes = [[8, 9, 10], [13, 14, 15], [30, 30, 30]]
    return sizes[difficulty][randrange(0, 3)]


def get_bomb_count(difficulty):
    bomb_nums = [10, 40, 99]
    return bomb_nums[difficulty]


def place_bomb(Game):
    # places bombs anywhere outside the safe area
    row = randrange(0, board_size(Game.board)[0])
    col = randrange(0, board_size(Game.board)[1])

    if Game.board[row][col] == 1:
        return place_bomb(Game)
    if [row, col] in Game.safe_area:
        return place_bomb(Game)
    else:
        Game.board[row][col] = 1
        return [row, col]


def bomb_count(Game, row, col):
    # sets number of bombs surrounding each tile
    adjacent_tiles = get_adjacent_tiles(board_size(Game.board), row, col)
    bombs = [ tile for tile in adjacent_tiles if Game.board[tile[0]][tile[1]] == 1 ]
    return len(bombs)

def get_adjacent_tiles(board_size, row, col):
    tiles = [(row - 1, col - 1), (row - 1, col), (row - 1, col + 1),
             (row, col - 1), (row, col + 1),
             (row + 1, col - 1), (row + 1, col), (row + 1, col + 1)]
    return [ tile for tile in tiles if validate_tile(board_size, row, col) ]


def validate_tile(board_size, row, col):
    return ( (row >= 0 and row < board_size[0] - 1) and (col >= 0 and col < board_size[1] - 1) )


def get_safe_area(Game):
    # set 3x3 box in bomb_list to prevent bombs in click area
    # change later to use click location
    size = board_size(Game.board)
    click_row = ceil(size[0] / 2) - 1
    click_col = ceil(size[1] / 2) - 1
    return get_adjacent_tiles(board_size(Game.board), click_row, click_col)
