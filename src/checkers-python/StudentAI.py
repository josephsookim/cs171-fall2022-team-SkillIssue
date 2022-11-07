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
        best_seq_score, best_seq = self.minimax(4)

        self.board.make_move(best_seq, self.color)
        return best_seq

    def minimax(self, depth):
        if depth == 0:
            return self.board.black_count - self.board.white_count, None

        if self.board.is_win(self.color):
            return 100, None

        moves = self.board.get_all_possible_moves(self.color)
        best_seq_score = 0
        best_seq = moves[0][0]

        for possible_move in moves:
            for possible_seq in possible_move:
                self.board.make_move(possible_seq, self.color)
                possible_seq_score, _ = self.minimax(depth - 1)
                if possible_seq_score > best_seq_score:
                    best_seq_score = possible_seq_score
                    best_seq = possible_seq
                self.board.undo()

        return best_seq_score, best_seq