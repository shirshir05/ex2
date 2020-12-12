from Game import Game


class Player:
    game = Game("input.txt", 20)
    number_move = 0

    def __init__(self):
        # self.game = Game("input.txt", 20)
        self.list_move = []
        self.fitness = float("inf")

    def set_game(self, game):
        self.game = game

    def play(self, routine):
        self.list_move = []
        self.game = Game("input.txt", 20)
        while self.number_move < 10000:
            routine()
        return self.list_move

    def move_up(self):
        self.number_move += 1
        for level in range(1, 21):
            self.game.play_up(level)
        self.list_move.append("u")

    def move_down(self):
        self.number_move += 1
        for level in range(1, 21):
            self.game.play_down(level)
        self.list_move.append("d")

    def move_right(self):
        self.number_move += 1
        for level in range(1, 21):
            self.game.play_right(level)
        self.list_move.append("r")

    def move_left(self):
        self.number_move += 1
        for level in range(1, 21):
            self.game.play_left(level)
        self.list_move.append("l")

    def update_fitness(self, fitness):
        self.fitness = fitness



