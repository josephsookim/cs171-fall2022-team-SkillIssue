import math
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

        best_seq = self.alpha_beta_pruning()
        # best_seq = self.mcts()
        self.board.make_move(best_seq, self.color)
        return best_seq

    def alpha_beta_pruning(self):
        _, best_seq = self.max_node(7, float("-inf"), float("inf"))
        return best_seq

    def max_node(self, depth, alpha, beta):
        heuristics = self.calculate_heuristics()
        moves = self.board.get_all_possible_moves(self.color)
        best_seq_score = float("-inf")
        best_seq = None

        if depth == 0 or self.board.is_win(self.color) != 0:
            if moves:
                return heuristics, moves[0][0]
            else:
                return heuristics, None

        for possible_move in moves:
            for possible_seq in possible_move:
                self.board.make_move(possible_seq, self.color)

                possible_seq_score, _ = self.min_node(depth - 1, alpha, beta)
                if possible_seq_score > best_seq_score:
                    best_seq_score = possible_seq_score
                    alpha = max(alpha, best_seq_score)
                    best_seq = possible_seq

                    if alpha >= beta:
                        self.board.undo()
                        return best_seq_score, best_seq
                self.board.undo()

        return best_seq_score, best_seq

    def min_node(self, depth, alpha, beta):
        heuristics = self.calculate_heuristics()
        moves = self.board.get_all_possible_moves(self.opponent[self.color])
        worst_seq_score = float("inf")
        worst_seq = None

        if depth == 0 or self.board.is_win(self.color) != 0:
            if moves:
                return heuristics, moves[0][0]
            else:
                return heuristics, None

        for possible_move in moves:
            for possible_seq in possible_move:
                self.board.make_move(possible_seq, self.opponent[self.color])

                possible_seq_score, _ = self.max_node(depth - 1, alpha, beta)
                if possible_seq_score < worst_seq_score:
                    worst_seq_score = possible_seq_score
                    beta = min(beta, worst_seq_score)
                    worst_seq = possible_seq

                    if alpha >= beta:
                        self.board.undo()
                        return worst_seq_score, worst_seq
                self.board.undo()

        return worst_seq_score, worst_seq

    def calculate_heuristics(self) -> int:
        team_val = 0
        enemy_val = 0

        for i in range(self.row):
            for j in range(self.col):
                board_piece = self.board.board[i][j]

                # if team color
                if board_piece.color == self.color:
                    # if king
                    if board_piece.is_king:
                        team_val += 3

                    # if pawn
                    else:
                        team_val += 2

                # if enemy color
                elif board_piece.color == self.opponent[self.color]:
                    # if king
                    if board_piece.is_king:
                        enemy_val += 2

                    # if pawn
                    else:
                        enemy_val += 1

        return team_val - enemy_val


    class Node:
        def __init__(self, parent, move, color):
            self.num_parent_wins = 0
            self.num_simulations = 0
            self.parent = parent
            self.children = []
            self.exploration = math.sqrt(2)
            self.move = move
            self.color = color

        def get_uct_child(self):
            return max(self.children, key = lambda x: x.calculate_uct())

        def calculate_uct(self):
            exploitation = (self.num_parent_wins / self.num_simulations)
            exploration = (self.exploration * math.sqrt(math.log(self.parent.num_simulations / self.num_simulations)))
            return exploitation + exploration

        def get_best_child(self):
            return max(self.children, key = lambda x: (x.num_parent_wins / x.num_simulations))

        def expand(self, move):
            new_node = self.Node(self, move)
            self.children.append(new_node)
            return new_node

    def mcts(self):
        current_node = self.Node(None, None, self.color)

        while current_node.children:
            current_node = current_node.get_uct_children()

        current_node = current_node.expand(self.board.get_all_possible_moves(self.color))
        for i in range(50):
            num_moves = 0