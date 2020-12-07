from Game import Game


class Player:

    def __init__(self):
        self.game = Game("one_input.txt", 1)
        self.list_move = []
        self.fitness = float("inf")

    def play(self, routine):
        #todo change range
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