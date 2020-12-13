from functools import partial

from Game import Game


class Player:

    def __init__(self):
        self.game = None
        self.list_move = []
        self.fitness = float("inf")

    def set_game(self, game):
        self.game = game

    def play(self, routine):
        self.list_move = []
        # todo change range
        for i in range(0, 1000):
            routine()
        return self.list_move

    def move_up(self):
        self.list_move.append("u")

    def move_down(self):
        self.list_move.append("d")

    def move_right(self):
        self.list_move.append("r")

    def move_left(self):
        self.list_move.append("l")

    def update_fitness(self, fitness):
        self.fitness = fitness

    # def move_up(self):
    #     self.game.play_up()
    #     self.list_move.append("u")
    #
    # def move_down(self):
    #     self.game.play_down()
    #     self.list_move.append("d")
    #
    # def move_right(self):
    #     self.game.play_right()
    #     self.list_move.append("r")
    #
    # def move_left(self):
    #     self.game.play_left()
    #     self.list_move.append("l")

    # todo level
    # def if_then_else(self, condition, out1, out2):
    #     out1() if condition() else out2()
    #
    # def if_box_ahead(self, out1, out2):
    #     return partial(self.if_then_else, self.game.box_ahead(), out1, out2)
