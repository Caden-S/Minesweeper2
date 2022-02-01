import random

class Game:
    def play(self):
        difficulty = int(input("Select the difficulty (1-3): "))
        difficulty -= 1
        board_size = self.get_board_size(difficulty)

        board = self.create_board(board_size, difficulty)

        resp = self.bomb_loop(difficulty, board, board_size)
        board = resp[0]
        bomb_list = resp[1]

        self.set_bomb_counter(board, bomb_list)
        self.board_print(board)
        self.set_safe_area(bomb_list)

    def board_print(self, board):
        for row in board:
            print(row)

    def create_board(self, board_size, difficulty):
        if difficulty == 2:
            return [ [0 for x in range(0, 30)] for y in range(0, 16) ]
        else:
            return [ [0 for x in range(0, board_size)] for y in range(0, board_size)]

    def get_board_size(self, difficulty):
        sizes = [[8,9,10], [13,14,15], [16,16,16]]
        return sizes[difficulty][random.randrange(0,3,1)]

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
        row = random.randrange(0, board_size - 1, 1)
        col = random.randrange(0, board_size - 1, 1)
        row16 = random.randrange(0, 15, 1)
        col30 = random.randrange(0, 29, 1)

        if [row, col] in bomb_list or [row16, col30] in bomb_list:
            return self.place_bomb(board, board_size, difficulty, bomb_list)

        if difficulty == 2:
            return [row16, col30]
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

    def set_safe_area(self, bomb_list):
        # set 3x3 box in bomb_list to prevent bombs in click area
        # bomb_location = x get bomb location from click
        bomb_row1 = [[-1, -1], [-1, 0], [-1, 1]]
        bomb_row2 = [[0, -1], [0, 0], [0, 1]]
        bomb_row3 = [[1, -1], [1, 0], [1, 1]]
        bomb_row1 += bomb_row2
        bomb_row1 += bomb_row3
        print(bomb_row1)
