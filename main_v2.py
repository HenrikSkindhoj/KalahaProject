import copy


class KalahaGame:
    def __init__(self):
        self.board = [4] * 6 + [0] + [4] * 6 + [0]
        self.current_player = 1
        self.max_depth = 15
        self.alpha = float('-inf')
        self.beta = float('inf')
        self.opt_mov = -1

    def curr_player_pits(self):
        if self.current_player == 1:
            return range(0, 5)
        else:
            return range(7, 12)

    def print_board(self):
        print("    P12" + "  P11" + "  P10" + "  P9" + "   P8" + "   P7")
        print("------------------------------------")
        print("    " + "    ".join(str(x) for x in self.board[12:6:-1]))
        print("{:02d}".format(self.board[13]), "    " * 7, "{:02d}".format(self.board[6]))
        print("    " + "    ".join(str(x) for x in self.board[:6]))
        print("------------------------------------")
        print("    P0" + "   P1" + "   P2" + "   P3" + "   P4" + "   P5")

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

    def play(self, pit, should_print):
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
            if should_print:
                self.print_board()
                self.find_winner()
        elif should_print:
            self.print_board()

    def curr_player_pits(self):
        if self.current_player == 1:
            return range(0, 6)
        else:
            return range(7, 13)

    def minimax(self, depth, alpha, beta, maximizing_player):
        # Check if game over or depth reached
        if depth == self.max_depth or self.game_over():
            if self.current_player == 1:
                return self.board[6] - self.board[13]
            else:
                return self.board[13] - self.board[6]

        else:
            # Max value player
            if self.current_player == maximizing_player:
                opt_val = float('-inf')
                for pit in self.curr_player_pits():
                    # If pit empty iterate to next pit
                    if self.board[pit] == 0:
                        continue

                    # Make max player move
                    duplicate_game = copy.deepcopy(self)
                    duplicate_game.play(pit, should_print=False)
                    value = duplicate_game.minimax(depth + 1, alpha, beta, maximizing_player)

                    # Update optimal value for max player
                    if value > alpha:
                        opt_val = value
                        self.opt_mov = pit

                    # Update beta
                    alpha = max(alpha, opt_val)
                    if beta <= alpha:
                        break

                # Return optimal value
                return opt_val
            else:
                opt_val = float('inf')
                for pit in self.curr_player_pits():
                    # If pit empty iterate to next pit
                    if self.board[pit] == 0:
                        continue

                    # Make max player move
                    duplicate_game = copy.deepcopy(self)
                    duplicate_game.play(pit, should_print=False)
                    value = duplicate_game.minimax(depth + 1, alpha, beta, maximizing_player)

                    # Update optimal value for min player
                    if value < beta:
                        opt_val = value
                        self.opt_mov = pit

                    # Update beta
                    beta = min(beta, opt_val)
                    if beta <= alpha:
                        break

                # Return optimal value
                return opt_val




def main():
    game = KalahaGame()
    game.print_board()
    while not game.game_over():
        if game.current_player == 1:
            pit = int(input("Player 1, choose a pit to play (0-5): "))
            game.play(pit, True)
        else:
            game.minimax(0, game.alpha, game.beta, 2)
            if game.opt_mov != -1:
                print("-------------")
                print(f"Player 2 chose {game.opt_mov}")
                print("-------------")
                game.play(game.opt_mov, True)
            else:
                print("Wrong opt_mov")


if __name__ == '__main__':
    main()
