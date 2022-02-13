from random import randrange
from math import ceil
import os


class GameState():
    difficulty = 0
    board = []
    safe_area = []


def start(Game):
    Game.difficulty = get_choice([], 0)

    board = true_board(create_board(Game))
    os.system('cls' if os.name == 'nt' else 'clear')
    print_board(board)

    choice = get_choice(board, 1)
    os.system('cls' if os.name == 'nt' else 'clear')

    Game.safe_area = get_safe_area(board, choice)
    Game.board = get_bombs(Game, board)

    play(Game, [choice], 0)

def get_choice(board, type):
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

    if type == 1:
        resp = format_choice(input("Enter the tile position (row, col): "))
        if resp != False:
            if resp[0] < board_size(board)[0] and resp[1] < board_size(board)[1]:
                return resp
        else:
            print("Please select a valid tile")
            return get_choice(board, 1)


def play(Game, chosen_tiles, error):
    board = true_board(Game.board)

    for tile in chosen_tiles:
        board = reveal(board, tile, [])
    if check_win_loss(Game, board, chosen_tiles[-1]) == True:
        return
    print_board(board)
    
    
    if error == 1:
        print("Please pick a valid tile.")

    choice = get_choice(board, 1)
    if choice in chosen_tiles:
        os.system('cls' if os.name == 'nt' else 'clear')
        play(Game, chosen_tiles, 1)
    else:
        os.system('cls' if os.name == 'nt' else 'clear')
        chosen_tiles.append(choice)
        play(Game, chosen_tiles, 0)


def win(board):
    os.system('cls' if os.name == 'nt' else 'clear')
    print_board(board)
    print(" ")
    print("You win!")



def lose(Game):
    os.system('cls' if os.name == 'nt' else 'clear')
    board = true_board(Game.board)
    rows = board_size(board)[0]
    cols = board_size(board)[1]
    for row in range(0, rows):
        for col in range(0, cols):
            if board[row][col][1] != 'B':
                board[row][col] = (1, board[row][col][1])
            else:
                board[row][col] = (1, 'B')
    print_board(board)
    print(" ")
    print("You lose!")


def check_win_loss(Game, board, choice):
    if board[choice[0]][choice[1]][1] == 'B':
        lose(Game)
        return True
    else:
        if all_safe_revealed(board) == True:
            win(board)
            return True
        else:
            return


def all_safe_revealed(board):
    tiles = []
    for row in board:
        for tile in row:
            if tile[1] != 'B':
                if tile[0] == 1:
                    tiles.append(True)
                else:
                    tiles.append(False)
    return (False not in tiles)


def format_choice(choice):
    if ',' not in choice:
        return False
    else:
        choice = choice.split(',')
        if choice[0] and choice[1]:
            return ((int(choice[0]) - 1, int(choice[1]) - 1))
        else:
            return False


def print_board(board):
    starting_rows = ["", ""]
    for tile in range(0, board_size(board)[1]):
        if tile == 0:
            starting_rows[0] += "     {} ".format(str(tile + 1))
            starting_rows[1] += "    ---"
        else:
            if tile < 10:
                starting_rows[0] += "  {} ".format(str(tile + 1))
                starting_rows[1] += " ---"
            else:
                starting_rows[0] += " {} ".format(str(tile + 1))
                starting_rows[1] += " ---"
    print(starting_rows[0])
    print(starting_rows[1])

    string_row = ""
    spacer = ""
    counter = 0
    for row in board:
        counter += 1
        if counter < 10:
            string_row += "{}  |".format(counter)
        else:
            string_row += "{} |".format(counter)
        spacer += "   |"
        for tile in row:
            if tile[0] == 0:
                string_row += (" X |")
            else:
                if tile[1] == 0:
                    string_row += "   |"
                else:
                    string_row += (" {} |".format(tile[1]))
            spacer += "---|"
        print(string_row)
        print(spacer)
        string_row = ""
        spacer = ""
    print("\n")


def reveal(board, choice, checked):
    if board[choice[0]][choice[1]][1] == 0:
        adjacent_tiles = get_adjacent_tiles(board_size(board), choice)
        safe_adjacent = [ tile for tile in adjacent_tiles if board[tile[0]][tile[1]][1] != 'B' ]
        safe_adjacent.append(choice)
        for tile in safe_adjacent:
            if tile not in checked:
                checked.append(tile)
                board[tile[0]][tile[1]] = (1, board[tile[0]][tile[1]][1])
                if board[tile[0]][tile[1]][1] > 0:
                    continue
                else:
                    reveal(board, tile, checked)
            else:
                continue
        return board
    else:
        board[choice[0]][choice[1]] = (1, board[choice[0]][choice[1]][1])
        return board

def true_board(board):
    num_rows = board_size(board)[0]
    num_cols = board_size(board)[1]

    for row in range(0, num_rows):
        for col in range(0, num_cols):
            if board[row][col] == 1:
                board[row][col] = (0, 'B')
            else:
                board[row][col] = (0, bomb_count(board, (row, col)))
    return board


def board_size(board):
    return (len(board), len(board[0]))


def create_board(Game):
    # returns board with x rows and y columns
    num_rows = get_board_rows(Game.difficulty)
    num_cols = get_board_cols(Game.difficulty)
    grid = [[0 for x in range(0, num_cols)] for y in range(0, num_rows)]
    return grid


def get_bombs(Game, board):
    bomb_list = [place_bomb(Game, board)
                 for bomb in range(0, get_num_bombs(Game.difficulty))]
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


def place_bomb(Game, board):
    # places bombs anywhere outside the safe area
    row = randrange(0, board_size(board)[0])
    col = randrange(0, board_size(board)[1])

    if board[row][col] == 1 or (row, col) in Game.safe_area:
        return place_bomb(Game, board)
    else:
        board[row][col] = 1
        return [row, col]


def bomb_count(board, position):
    # sets number of bombs surrounding each tile
    adjacent_tiles = get_adjacent_tiles(board_size(board), position)
    bombs = [tile for tile in adjacent_tiles if board[tile[0]][tile[1]] == 1]
    return len(bombs)


def get_adjacent_tiles(board_size, position):
    row = position[0]
    col = position[1]
    tiles = [(row - 1, col - 1), (row - 1, col), (row - 1, col + 1),
             (row, col - 1), (row, col + 1),
             (row + 1, col - 1), (row + 1, col), (row + 1, col + 1)]
    return [tile for tile in tiles if valid_tile(board_size, tile)]


def valid_tile(board_size, position):
    row = position[0]
    col = position[1]
    return ((row >= 0 and row < board_size[0]) and (col >= 0 and col < board_size[1]))


def get_safe_area(board, choice):
    # set 3x3 box in bomb_list to prevent bombs in click area
    # change later to use click location
    size = board_size(board)
    adjacent_tiles = get_adjacent_tiles(size, choice)
    adjacent_tiles.append(choice)
    return adjacent_tiles
