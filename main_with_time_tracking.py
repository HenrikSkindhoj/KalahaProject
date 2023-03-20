import copy
import math
import time

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

    def game_over(self):
        return sum(self.board[:6]) == 0 or sum(self.board[7:13]) == 0

    def find_winner(self):
        if self.board[self.player_1_kalaha_index] > self.board[self.player_2_kalaha_index]:
            self.board[self.player_2_kalaha_index] += sum(self.board[7:13])
            self.board[:6] = [0] * 6
            self.board[7:13] = [0] * 6
        elif self.board[self.player_1_kalaha_index] < self.board[self.player_2_kalaha_index]:
            self.board[self.player_1_kalaha_index] += sum(self.board[:6])
            self.board[:6] = [0] * 6
            self.board[7:13] = [0] * 6



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
            return

        if self.board[pit] == 0:
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
                self.find_winner()

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
    max_depths = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    for max_depth in max_depths:
        game = KalahaGame()
        game.max_depth = max_depth

        # Average time count
        running_times = []

        while not game.game_over():
            if game.current_player == 1:
                # Running time of minimax player 1
                start_counter_ns = time.perf_counter_ns()
                game.minimax(0, game.alpha, game.beta, player_1)
                end_counter_ns = time.perf_counter_ns()
                running_times.append((end_counter_ns - start_counter_ns)/math.pow(10, 6))

                game.play(game.opt_mov, True)
            else:
                # Running time of minimax player 2
                start_counter_ns = time.perf_counter_ns()
                game.minimax(0, game.alpha, game.beta, player_2)
                end_counter_ns = time.perf_counter_ns()
                running_times.append((end_counter_ns - start_counter_ns)/math.pow(10, 6))

                if game.opt_mov != -1 and not game.game_over():
                    game.play(game.opt_mov, True)


            if game.game_over():
                print(f"Game depth: {max_depth}, AVG running time: {round(sum(running_times)/len(running_times), 2)}ms, Search space {math.pow(6,max_depth)+1} ")



if __name__ == '__main__':
    main()
