import copy
import sys


class KalahaGame:
    def __init__(self):
        self.board = [4] * 6 + [0] + [4] * 6 + [0]
        self.current_player = 1
        self.max_depth = 3
        self.alpha = float('-inf')
        self.beta = float('inf')
        self.opt_mov = -1

    def curr_player_pits(self):
        if self.current_player == 1:
            return range(0, 6)
        else:
            return range(7, 13)

    def print_board(self):
        print("    P12" + "  P11" + "  P10" + "  P9" + "   P8" + "   P7")
        print("------------------------------------")
        print("    " + "    ".join(str(x) for x in self.board[12:6:-1]))
        print("{:02d}".format(self.board[13]), "    " * 7, "{:02d}".format(self.board[6]))
        print("    " + "    ".join(str(x) for x in self.board[:6]))
        print("------------------------------------")
        print("    P0" + "   P1" + "   P2" + "   P3" + "   P4" + "   P5")

    def play_ai(self, pit):
        if self.current_player == 1:
            # Game parms
            pits = range(0, 6)
            kalaha = 6
            opponent_kalaha = 13

            if pit not in pits:
                print("Invalid move")
                return

            if self.board[pit] == 0:
                print("This pit is empty")
                return

            stones = self.board[pit]
            self.board[pit] = 0
            while stones > 0:
                pit = (pit + 1) % 14
                if pit == opponent_kalaha:
                    continue
                self.board[pit] += 1
                stones -= 1

            if (self.board[pit] == 1 and stones == 0) and pit in pits:
                opposite_pit = 12 - pit
                if self.board[opposite_pit] > 0:
                    self.board[kalaha] += self.board[opposite_pit]
                    self.board[opposite_pit] = 0

            if stones == 0:
                if (self.board[pit] == 1 or pit == kalaha) and pit not in pits:
                    self.current_player = self.current_player
                else:
                    self.current_player = 1 if self.current_player == 2 else 2

            if self.game_over():
                self.print_board()
                self.print_winner()
            else:
                self.print_board()
        else:
            print("-------------------")
            print(f"AI made mov {self.opt_mov}")
            print("-------------------")
            self.minimax(0, self.alpha, self.beta)
            self.play(self.opt_mov)


    def play(self, pit):
        if self.current_player == 1:
            pits = range(0, 6)
            kalaha = 6
            opponent_kalaha = 13
        else:
            pits = range(7, 13)
            kalaha = 13
            opponent_kalaha = 6

        if pit not in pits:
            print("Invalid move")
            return

        if self.board[pit] == 0:
            print("This pit is empty")
            return

        stones = self.board[pit]
        self.board[pit] = 0
        while stones > 0:
            pit = (pit + 1) % 14
            if pit == opponent_kalaha:
                continue
            self.board[pit] += 1
            stones -= 1

        if (self.board[pit] == 1 and stones == 0) and pit in pits:
            opposite_pit = 12 - pit
            if self.board[opposite_pit] > 0:
                self.board[kalaha] += self.board[opposite_pit]
                self.board[opposite_pit] = 0

        if stones == 0:
            if (self.board[pit] == 1 or pit == kalaha) and pit not in pits:
                self.current_player = self.current_player
            else:
                self.current_player = 1 if self.current_player == 2 else 2

        if self.game_over():
            self.print_board()
            self.find_winner()
        else:
            self.print_board()

    def game_over(self):
        return sum(self.board[:6]) == 0 or sum(self.board[7:13]) == 0

    def find_winner(self):
        if self.board[6] > self.board[13]:
            self.board[13] += sum(self.board[7:13])
            self.board[:6] = [0] * 6
            self.board[7:13] = [0] * 6
            print("Player 1 wins!")
        elif self.board[6] < self.board[13]:
            self.board[6] += sum(self.board[:6])
            self.board[:6] = [0] * 6
            self.board[7:13] = [0] * 6
            print("Player 2 wins!")
        else:
            print("It's a tie!")

    def minimax(self, depth, alpha, beta):
        # Return game score when game is over or max depth reach, use to evaluate move
        # Simple heuristic function
        if self.game_over() or depth == self.max_depth:
            if self.current_player == 1:
                return self.board[6] - self.board[13]
            else:
                return self.board[13] - self.board[6]

        if self.current_player == 1:
            # Max player functionality
            return self.get_opt_val(depth, alpha, beta, "max")
        else:
            # Min player functionality
            return self.get_opt_val(depth, alpha, beta, "min")

    def get_opt_val(self, depth, alpha, beta, strategy):
        if self.current_player == 1:
            opt_val = float('-inf')
            for pit in self.curr_player_pits():
                if self.board[pit] == 0:
                    continue
                duplicate_game = copy.deepcopy(self)
                duplicate_game.play(pit)
                value = duplicate_game.minimax(depth + 1, alpha, beta)
                if strategy == "max":
                    if value > opt_val:
                        opt_val = value
                        self.opt_mov = pit

                    alpha = max(alpha, opt_val)
                    if beta <= alpha:
                        break
                elif strategy == "min":
                    if value < opt_val:
                        opt_val = value
                        self.opt_mov = pit

                    alpha = min(alpha, opt_val)
                    if beta <= alpha:
                        break
                else:
                    return "error"
            return opt_val


def main():
    game_mode = int(input("Choose 1 to play against yourself and 2 to play against AI "))
    if game_mode == 1:
        game = KalahaGame()
        game.print_board()
        while not game.game_over():
            if game.current_player == 1:
                pit = int(input("Player 1, choose a pit to play (0-5): "))
            else:
                pit = int(input("Player 2, choose a pit to play (7-12): "))
            game.play(pit)
    elif game_mode == 2:
        game = KalahaGame()
        game.print_board()
        while not game.game_over():
            pit = int(input("Player 1, choose a pit to play (0-5): "))
            game.play_ai(pit)

if __name__ == '__main__':
    main()
