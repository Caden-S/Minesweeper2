from random import randrange
from math import ceil

class Game:
    def play(self):
        difficulty = int(input("Select the difficulty (1-3): ")) - 1
        board_x = self.get_board_rows(difficulty)
        board_y = self.get_board_cols(difficulty)
        board_size = [board_x, board_y]
        safe_area = self.get_safe_area(board_size)
        board = self.create_board(board_size, difficulty)
        resp = self.bomb_loop(difficulty, board, board_size)
        board = resp[0]
        bomb_list = resp[1]

        self.set_bomb_counter(board, bomb_list)
        self.board_print(board)
        #self.set_safe_area(bomb_list)

    def board_print(self, board):
        for row in board:
            print(row)

    def create_board(self, board_size, difficulty):
            return [ [0 for x in range(0, board_size[1])] for y in range(0, board_size[0]) ]

    def get_board_rows(self, difficulty):
        sizes = [[8,9,10], [13,14,15], [16,16,16]]
        return sizes[difficulty][randrange(0,3)]
    
    def get_board_cols(self, difficulty):
        sizes = [[8,9,10], [13,14,15], [30,30,30]]
        return sizes[difficulty][randrange(0,3)]

    def get_bomb_count(self, difficulty):
        bomb_nums = [10,40,99]
        return bomb_nums[difficulty]
    
    def bomb_loop(self, difficulty, board, board_size):
        bomb_list = []
        for bomb in range(0, self.get_bomb_count(difficulty)):
            bomb_loc = self.place_bomb(board, board_size, difficulty, bomb_list)
            bomb_list.append(bomb_loc)
            board[bomb_loc[0]][bomb_loc[1]] = 9
        return [board, bomb_list]

    def place_bomb(self, board, board_size, difficulty, bomb_list):
        row = randrange(0, board_size[0] - 1, 1)
        col = randrange(0, board_size[1] - 1, 1)
        safe_area = self.get_safe_area(board_size)

        if [row, col] in bomb_list:
            return self.place_bomb(board, board_size, difficulty, bomb_list)
        if [row, col] in safe_area:
            return self.place_bomb(board, board_size, difficulty, bomb_list)
        else:
            return [row, col]
    
    def set_bomb_counter(self, board, bomb_list):
        for row in range(0, len(board)):
            for tile in range(0, len(board[0])):
                if [row, tile] in bomb_list:
                    continue
                else:
                    for bomb in bomb_list:
                        if abs(bomb[0] - row) <= 1 and abs(bomb[1] - tile) <= 1:
                            board[row][tile] += 1
                        else:
                            continue
        return board 

    def get_safe_area(self, board_size):
        # set 3x3 box in bomb_list to prevent bombs in click area
        click_row = ceil(board_size[0] / 2) - 1
        click_col = ceil(board_size[1] / 2) - 1
        bomb_row1 = [[click_row-1, click_col-1], [click_row-1, click_col], [click_row-1, click_col+1]]
        bomb_row2 = [[click_row, click_col-1], [click_row, click_col], [click_row, click_col+1]]
        bomb_row3 = [[click_row+1, click_col-1], [click_row+1, click_col], [click_row+1, click_col+1]]
        bomb_row1 += bomb_row2
        bomb_row1 += bomb_row3
        return bomb_row1
