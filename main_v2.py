import copy


class KalahaGame:
    def __init__(self):
        self.board = [4] * 6 + [0] + [4] * 6 + [0]
        self.current_player = 1
        self.max_depth = 8
        self.alpha = float('-inf')
        self.beta = float('inf')
        self.opt_mov = -1
        self.player_1_kalaha_index = 6
        self.player_2_kalaha_index = 13

    def print_board(self):
        print("++++++++++++++++++++++++++++++++++++++")
        print("|    P12" + "  P11" + "  P10" + "  P9" + "   P8" + "   P7     |")
        print("--------------------------------------")
        print("|     " + "    ".join(str(x) for x in self.board[12:6:-1]) + "     |")
        print("| {:02d}".format(self.board[13]), "    " * 7, "{:02d}".format(self.board[6]) + " |")
        print("|     " + "    ".join(str(x) for x in self.board[:6]) + "     |")
        print("--------------------------------------")
        print("|    P0" + "   P1" + "   P2" + "   P3" + "   P4" + "   P5     |")
        print("++++++++++++++++++++++++++++++++++++++")

    def game_over(self):
        return sum(self.board[:6]) == 0 or sum(self.board[7:13]) == 0

    def find_winner(self):
        if self.board[self.player_1_kalaha_index] > self.board[self.player_2_kalaha_index]:
            self.board[self.player_2_kalaha_index] += sum(self.board[7:13])
            self.board[:6] = [0] * 6
            self.board[7:13] = [0] * 6
            self.end_game_prompt("Player 1 won the game !!!")
        elif self.board[self.player_1_kalaha_index] < self.board[self.player_2_kalaha_index]:
            self.board[self.player_1_kalaha_index] += sum(self.board[:6])
            self.board[:6] = [0] * 6
            self.board[7:13] = [0] * 6
            self.end_game_prompt("Player 2 won the game !!!")
        else:
            self.end_game_prompt("Tied game, what a nail bidder :D")

    def end_game_prompt(self, text):
        print()
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        print("####################################")
        print("------------------------------------")
        print(f"     {text}")
        print("------------------------------------")
        print("####################################")
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        print()

    def helper_text(self, text):
        print(f"{text}")

    def input_divider(self):
        print("++++++++++++++++++++++++++++++++++++")

    def play(self, pit, should_print):
        if self.current_player == 1:
            pits = self.curr_player_pits()
            kalaha = self.player_1_kalaha_index
            opponent_kalaha = self.player_2_kalaha_index
        else:
            pits = self.curr_player_pits()
            kalaha = self.player_2_kalaha_index
            opponent_kalaha = self.player_1_kalaha_index

        if pit not in pits:
            self.helper_text("Invalid move")
            return

        if self.board[pit] == 0:
            self.helper_text("This pit is empty")
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
                return self.board[self.player_1_kalaha_index] - self.board[self.player_2_kalaha_index]
            else:
                return self.board[self.player_2_kalaha_index] - self.board[self.player_1_kalaha_index]

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
    player_1 = 1
    player_2 = 2
    game = KalahaGame()

    game.input_divider()
    game_mode = int(input("Choose game mode: \n 1) Player vs. Player \n 2) Player vs. AI \n 3) AI vs. AI "))
    # Player vs. Player
    if game_mode == 1:
        game.print_board()
        while not game.game_over():
            if game.current_player == 1:
                pit = int(input("Player 1, choose a pit to play (0-5): "))
            else:
                pit = int(input("Player 2, choose a pit to play (7-12): "))
            game.play(pit, True)
    # Player vs. AI
    elif game_mode == 2:
        game.input_divider()
        difficulty = int(input("Choose difficulty: \n 1) Easy \n 2) Medium \n 3) Hard "))
        match difficulty:
            case 1:
                game.max_depth = 2
            case 2:
                game.max_depth = 5
            case 3:
                game.max_depth = 8

        game.print_board()
        while not game.game_over():
            if game.current_player == 1:
                pit = int(input("Player 1, choose a pit to play (0-5): "))
                game.play(pit, True)
            else:
                game.minimax(0, game.alpha, game.beta, player_2)
                game.play(game.opt_mov, True)
                if not game.game_over():
                    game.helper_text(f"Player 2 chose {game.opt_mov}")
                    game.print_board()
    # AI vs. AI
    elif game_mode == 3:
        game.input_divider()
        depth = int(input("Choose please select a game depth:"))
        game.max_depth = depth
        game.print_board()
        while not game.game_over():
            if game.current_player == 1:
                game.minimax(0, game.alpha, game.beta, player_1)
                game.play(game.opt_mov, True)
            else:
                game.minimax(0, game.alpha, game.beta, player_2)
                if game.opt_mov != -1 and not game.game_over():
                    game.helper_text(f"Player 2 chose {game.opt_mov}")
                    game.play(game.opt_mov, True)


if __name__ == '__main__':
    main()
