from functools import partial

from Game import Game


class Player:

    def __init__(self):
        self.game = None
        self.list_move = []
        self.fitness = float("inf")
        self.set_levels = []

    def play(self, routine, game, set_level):
        self.game = game
        self.set_levels = set_level
        self.list_move = []
        # todo change range
        for i in range(0, 500):
            routine()
        return self.list_move

    def progn(self, *args):
        for arg in args:
            arg()

    def prog2(self, out1, out2):
        return partial(self.progn, out1, out2)

    def prog3(self, out1, out2, out3):
        return partial(self.progn, out1, out2, out3)

    def prog4(self, out1, out2, out3, out4):
        return partial(self.progn, out1, out2, out3, out4)

    # def move_up(self):
    #     self.list_move.append("u")
    #
    # def move_down(self):
    #     self.list_move.append("d")

    def if_then_else(self, condition, out1, out2):
        out1() if condition() else out2()

    def if_box_ahead(self, out1, out2):
        return partial(self.if_then_else, self.sense_box, out1, out2)

    def sense_box(self):
        pass
    #
    # def move_right(self):
    #     self.list_move.append("r")
    #
    # def move_left(self):
    #     self.list_move.append("l")

    def update_fitness(self, fitness):
        self.fitness = fitness

    def move_up(self):
        for level in self.set_levels:
            self.game.play(level + 1, ['u'])
        self.list_move.append("u")

    def move_down(self):
        for level in self.set_levels:
            self.game.play(level + 1, ['d'])
        self.list_move.append("d")

    def move_right(self):
        for level in self.set_levels:
            self.game.play(level + 1, ['r'])
        self.list_move.append("r")

    def move_left(self):
        for level in self.set_levels:
            self.game.play(level + 1, ['l'])
        self.list_move.append("l")
