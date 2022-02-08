from random import randrange
from math import ceil

class GameState():
    difficulty = 0
    board = []
    safe_area = []


def start(Game):
    Game.difficulty = int(input("Select the difficulty (1-3): ")) - 1
    choice = input("Enter tile position (x,y): ")
    choice = (int(choice[0]), int(choice[2]))
    board = create_board(Game)
    Game.safe_area = get_safe_area(board, choice)
    Game.board = bombs(Game, board)
    reveal(Game.board, choice, [])
    play(Game, [])
    
def play(Game, chosen_tiles):
    revealed_board = true_board(Game.board)
    

def print_board(board):
    # Change later for better format
    rows = []
    for row in board:
        for tile in row:
            rows.append(tile[0])
        print(rows)
        rows = []

def reveal(board, choice, checked):
    checked.append(choice)

    adjacent_tiles = get_adjacent_tiles(board_size(board), choice)
    safe_adjacent = [tile for tile in adjacent_tiles if tile[1] <= 1]
    for tile in safe_adjacent:
        if tile not in checked:
            checked.append(tile)
        else:
            continue
    for tile in safe_adjacent:
        board[tile[0]][tile[1]][0] = board[tile[0]][tile[1]][1]
        reveal(board, tile, checked)
    

    


def true_board(board):
    new_board = []
    rows = []
    num_rows = board_size(board)[0]
    num_cols = board_size(board)[1]

    for row in range(0, num_rows):
        for col in range(0, num_cols):
            if board[row][col] == 1:
                rows.append(([],9))
            else:
                rows.append(([], bomb_count(board, (row, col))))
            if len(rows) == board_size(board)[1]:
                new_board += [rows]
                rows = []
    return new_board
  
def board_size(board):
    return (len(board), len(board[0]))

def create_board(Game):
    # returns board with x rows and y columns
    num_rows = get_board_rows(Game.difficulty)
    num_cols = get_board_cols(Game.difficulty)
    grid = [[0 for x in range(0, num_rows)] for y in range(0, num_cols)]
    return grid

def bombs(Game, board):
    bomb_list = [ place_bomb(board, Game.safe_area) for bomb in range(0, get_num_bombs(Game.difficulty)) ]
    for bomb in bomb_list:
        board[bomb[0]][bomb[1]] = 1
    return board  

def get_board_rows(difficulty):
    sizes = [[8, 9, 10], [13, 14, 15], [16, 16, 16]]
    return sizes[difficulty][randrange(0, 3)]

def get_board_cols(difficulty):
    sizes = [[8, 9, 10], [13, 14, 15], [30, 30, 30]]
    return sizes[difficulty][randrange(0, 3)]

def get_num_bombs(difficulty):
    bomb_nums = [10, 40, 99]
    return bomb_nums[difficulty]

def place_bomb(board, safe_area):
    # places bombs anywhere outside the safe area
    row = randrange(0, board_size(board)[0])
    col = randrange(0, board_size(board)[1])

    if board[row][col] == 1:
        return place_bomb(board, safe_area)
    if [row, col] in safe_area:
        return place_bomb(board, safe_area)
    else:
        board[row][col] = 1
        return [row, col]

def bomb_count(board, position):
    # sets number of bombs surrounding each tile
    adjacent_tiles = get_adjacent_tiles(board_size(board), position)
    bombs = [ tile for tile in adjacent_tiles if board[tile[0]][tile[1]] == 1 ]
    return len(bombs)

def get_adjacent_tiles(board_size, position):
    row = position[0]
    col = position[1]
    tiles = [(row - 1, col - 1), (row - 1, col), (row - 1, col + 1),
             (row, col - 1), (row, col + 1),
             (row + 1, col - 1), (row + 1, col), (row + 1, col + 1)]
    return [ tile for tile in tiles if valid_tile(board_size, tile[0],tile[1]) ]

def valid_tile(board_size, row, col):
    return ( (row >= 0 and row < board_size[0]) and (col >= 0 and col < board_size[1]) )

def get_safe_area(board, choice):
    # set 3x3 box in bomb_list to prevent bombs in click area
    # change later to use click location
    size = board_size(board)
    return get_adjacent_tiles(board_size(board), choice)
