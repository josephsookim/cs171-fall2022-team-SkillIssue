from random import randint
from BoardClasses import Move
from BoardClasses import Board
#The following part should be completed by students.
#Students can modify anything except the class name and exisiting functions and varibles.
class StudentAI():

    def __init__(self,col,row,p):
        self.col = col
        self.row = row
        self.p = p
        self.board = Board(col,row,p)
        self.board.initialize_game()
        self.color = ''
        self.opponent = {1:2,2:1}
        self.color = 2

    def get_move(self, move):
        if len(move) != 0:
            self.board.make_move(move,self.opponent[self.color])
        else:
            self.color = 1

        moves = self.board.get_all_possible_moves(self.color)
        best_seq_score, best_seq = self.minimax(3, 0, moves[0][0])

        self.board.make_move(best_seq, self.color)
        return best_seq

    def minimax(self, depth, best_seq_score, best_move):
        if depth == 0:
            if self.color == 1:
                return self.board.black_count - self.board.white_count, best_move
            elif self.color == 2:
                return self.board.white_count - self.board.black_count, best_move

        if self.board.is_win(self.color) == self.color:
            return 100, best_move

        elif self.board.is_win(self.color) == self.opponent[self.color]:
            return -100, best_move

        moves = self.board.get_all_possible_moves(self.color)
        best_seq_score = 0
        best_seq = moves[0][0]

        for possible_move in moves:
            current_seq_score = 0
            for possible_seq in possible_move:
                self.board.make_move(possible_seq, self.color)
                if self.get_possible_move_count() > 0:
                    seq_score, _ = self.minimax(depth - 1, best_seq_score, best_seq)
                    current_seq_score += seq_score
                    self.board.undo()

                else:
                    self.board.undo()
                    break # next iteration

            # if there is no inner break, check max seq score
            else:
                if current_seq_score > best_seq_score:
                    best_seq_score = current_seq_score
                    best_seq = possible_seq

            # go to next iteration regardless
            continue

        return best_seq_score, best_seq

    def get_possible_move_count(self):
        return len(self.board.get_all_possible_moves(self.color))