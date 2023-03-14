import sys


class KalahaGame:
    def __init__(self):
        self.board = [4] * 6 + [0] + [4] * 6 + [0]
        self.current_player = 1

    def print_board(self):
        print("    P12" + "  P11" + "  P10" + "  P9" + "   P8" + "   P7")
        print("------------------------------------")
        print("    " + "    ".join(str(x) for x in self.board[12:6:-1]))
        print("{:02d}".format(self.board[13]), "    " * 7, "{:02d}".format(self.board[6]))
        print("    " + "    ".join(str(x) for x in self.board[:6]))
        print("------------------------------------")
        print("    P0" + "   P1" + "   P2" + "   P3" + "   P4" + "   P5")

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

        if pit == kalaha:
            self.current_player = 1 if self.current_player == 2 else 2
        elif self.board[pit] == 1 and pit in pits:
            opposite_pit = 12 - pit
            if self.board[opposite_pit] > 0:
                self.board[kalaha] += self.board[opposite_pit] + 1
                self.board[opposite_pit] = 0
                self.board[pit] = 0

        if self.game_over():
            self.print_board()
            self.print_winner()
        else:
            self.print_board()

    def game_over(self):
        return sum(self.board[:6]) == 0 or sum(self.board[7:13]) == 0

    def print_winner(self):
        if self.board[6] > self.board[13]:
            print("Player 1 wins!")
        elif self.board[6] < self.board[13]:
            print("Player 2 wins!")
        else:
            print("It's a tie!")


def main():
    game = KalahaGame()
    game.print_board()
    while not game.game_over():
        if game.current_player == 1:
            pit = int(input("Player 1, choose a pit to play (0-5): "))
        else:
            pit = int(input("Player 2, choose a pit to play (7-12): "))
        game.play(pit)


if __name__ == '__main__':
    main()