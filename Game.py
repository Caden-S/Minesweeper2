from random import randrange
from math import ceil
from copy import deepcopy
import os


class GameState:
    difficulty = 0
    board = []
    safe_area = []

class Tile:
    def __init__(self, revealed, bomb):
        self.revealed = revealed
        self.bomb = bomb
        self.counter = 0

    def __eq__(self, other):
        if isinstance(other, Tile):
            return (self.revealed == other.revealed and self.bomb == other.bomb)
        else:
            return False

def start(Game):
    os.system('cls' if os.name == 'nt' else 'clear')

    Game.difficulty = get_choice([], 0)
    Game.board = create_board(Game.difficulty)
    print_board(Game.board)
    choice = get_choice(Game.board, 1)

    os.system('cls' if os.name == 'nt' else 'clear')

    Game.safe_area = get_safe_area(Game.board, choice)
    Game.board = set_bomb_count(get_bomb_locs(Game, Game.board))
    play(Game, [choice], 0)

def play(Game, chosen_tiles, error):
    for tile in chosen_tiles:
        Game.board = reveal(Game.board, tile, [])
    if check_win_loss(Game, chosen_tiles[-1]) == True:
        return

    print_board(Game.board)
    if error == 1:
        print("Please pick a different tile.")

    choice = get_choice(Game.board, 1)
    if choice in chosen_tiles:
        os.system('cls' if os.name == 'nt' else 'clear')
        play(Game, chosen_tiles, 1)
    else:
        os.system('cls' if os.name == 'nt' else 'clear')
        chosen_tiles.append(choice)
        play(Game, chosen_tiles, 0)

def get_choice(board, type):
    # Type 0 checks if difficulty inputs are in range
    # and are valid inputs
    if type == 0:
        values = [0,1,2]
        try:
            resp = int(input("Select the difficulty (1-3): ")) - 1
            if resp not in values:
                print("Please select a valid difficulty")
                return get_choice(board, 0)
            else:
                return resp
        except ValueError:
            print("Please select a valid difficulty")
            return get_choice(board, 0)
        except TypeError:
            print("Please select a valid difficulty")
            return get_choice(board, 0)

    # Type 1 checks if inputs for coordinates are in range
    # and are valid inputs
    if type == 1:
        resp = format_choice(input("Enter the tile position (row, col): "))
        if resp != False:
            if resp[0] < board_size(board)[0] and resp[1] < board_size(board)[1]:
                return resp
            else:
                print("Please select a valid tile")
                return get_choice(board, 1)
        else:
            print("Please select a valid tile")
            return get_choice(board, 1)

def format_choice(choice):
    # Turns input 5,5 into tuple (5,5) and checks 
    # choice for valid inputs
    if ',' not in choice:
        return False
    else:
        choice = choice.split(',')
        if choice[0] and choice[1]:
            try:
                resp = ((int(choice[0]) - 1, int(choice[1]) - 1))
                return resp
            except ValueError:
                return False
        else:
            return False

def win(board):
    os.system('cls' if os.name == 'nt' else 'clear')
    print_board(board)
    print(" ")
    print("You win!")

def lose(Game):
    os.system('cls' if os.name == 'nt' else 'clear')
    print_board(reveal_all(Game.board))
    print(" ")
    print("You lose!")

def check_win_loss(Game, choice):
    if Game.board[choice[0]][choice[1]].bomb == True:
        lose(Game)
        return True
    else:
        if all_safe_revealed(Game.board) == True:
            win(Game.board)
            return True
        else:
            return

def reveal_all(board):
    # Returns revealed version of board
    for row in board:
        for tile in row:
            if tile.bomb == False:
                tile.revealed = True
    return board

def all_safe_revealed(board):
    not_bombs = [ tile for row in board for tile in row if tile.bomb == False ]
    all_revealed = [ True if tile.revealed == True else False for tile in not_bombs ]
    return False not in all_revealed

def print_board(board):
    # Prints column numbers
    num_row_string = "  "
    starting_row = "   "
    num_row = [ "   " + str(col + 1) if col < 10 else "  " + str(col + 1) for col in range(0, board_size(board)[1]) ]
    for col in num_row:
        num_row_string += str(col)
        starting_row += " ---"
    print(num_row_string + "\n" + starting_row)

    # Prints tiles as X for unrevealed, blank if no bombs, 
    # or the number of bombs nearby
    for row in enumerate(board):
        string_row = ""
        spacer = ""
        if row[0] < 9:
            string_row += "{}  |".format(row[0] + 1)
        else:
            string_row += "{} |".format(row[0] + 1)
        spacer += "   |"

        for tile in row[1]:
            string_row += get_tile_format(tile)
            spacer += "---|"
        print(string_row)
        print(spacer)
    print("\n")

def get_tile_format(tile):
    if tile.revealed == False:
        return " {} |".format(u"\u2588")
    else:
        if tile.bomb == False:
            if tile.counter == 0:
                return "   |"
            else:
                return " {} |".format(tile.counter)
        else:
            return " {} |".format(u"\u2588")

def reveal(board, choice, checked):
    # Recursively reveals if tiles around the 'choice'
    # does not reveal tiles adjacent to tiles with a counter
    # that is not 0 or is a bomb
    if board[choice[0]][choice[1]].counter == 0:
        adjacent_tiles = get_adjacent_tiles(board_size(board), choice)
        safe_adjacent = [ tile for tile in adjacent_tiles if board[tile[0]][tile[1]].bomb == False ]
        safe_adjacent.append(choice)

        for tile in safe_adjacent:
            if tile not in checked:
                checked.append(tile)
                board[tile[0]][tile[1]].revealed = True
                if board[tile[0]][tile[1]].counter > 0:
                    continue
                else:
                    reveal(board, tile, checked)
            else:
                continue
        return board
    else:
        board[choice[0]][choice[1]].revealed = True
        return board

def board_size(board):
    return (len(board), len(board[0]))

def create_board(difficulty):
    # Returns board with x rows and y columns
    num_rows = get_board_rows(difficulty)
    num_cols = get_board_cols(difficulty)
    board = [[Tile(False, False) for x in range(0, num_cols)] for y in range(0, num_rows)]
    return board

def get_board_rows(difficulty):
    sizes = [[8, 9, 10], [13, 14, 15], [16, 16, 16]]
    return sizes[difficulty][randrange(0, 3)]

def get_board_cols(difficulty):
    sizes = [[8, 9, 10], [13, 14, 15], [30, 30, 30]]
    return sizes[difficulty][randrange(0, 3)]

def set_total_bombs(difficulty):
    # Sets bomb count based on difficulty
    bomb_nums = [10, 40, 99]
    return bomb_nums[difficulty]

def get_bomb_locs(Game, board):
    # Returns list of tuples for coordinates of bombs
    bomb_list = [ place_bomb(Game, board) for bomb in range(0, set_total_bombs(Game.difficulty)) ]
    for bomb in bomb_list:
        board[bomb[0]][bomb[1]].bomb = True
    return board

def get_bomb_count(board, position):
    # Gets number of bombs surrounding each tile
    adjacent_tiles = get_adjacent_tiles(board_size(board), position)
    bombs = [tile for tile in adjacent_tiles if board[tile[0]][tile[1]].bomb == True]
    return len(bombs)

def set_bomb_count(board):
    # Sets counter for each tile
    for row in enumerate(board):
        for tile in enumerate(row[1]):
            board[row[0]][tile[0]].counter += get_bomb_count(board, (row[0],tile[0]))
    return board

def place_bomb(Game, board):
    # Places bombs anywhere outside the safe area
    row = randrange(0, board_size(board)[0])
    col = randrange(0, board_size(board)[1])

    if board[row][col].bomb == True or (row, col) in Game.safe_area:
        return place_bomb(Game, board)
    else:
        return [row, col]

def get_adjacent_tiles(board_size, position):
    # Gets all tiles in a 3x3 box around the position
    row = position[0]
    col = position[1]
    tiles = [(row - 1, col - 1), (row - 1, col), (row - 1, col + 1),
             (row, col - 1), (row, col + 1),
             (row + 1, col - 1), (row + 1, col), (row + 1, col + 1)]
    return [tile for tile in tiles if valid_tile(board_size, tile)]

def valid_tile(board_size, position):
    # Checks if each tile is within the bounds of the board
    row = position[0]
    col = position[1]
    return ((row >= 0 and row < board_size[0]) and (col >= 0 and col < board_size[1]))

def get_safe_area(board, choice):
    # Sets a 3x3 safe space around initial choice
    size = board_size(board)
    adjacent_tiles = get_adjacent_tiles(size, choice)
    adjacent_tiles.append(choice)
    return adjacent_tiles
