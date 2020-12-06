import random
from datetime import datetime

from game import Game

from functools import partial
import numpy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp


def progn(*args):
    for arg in args:
        arg()


def prog2(out1, out2):
    return partial(progn, out1, out2)


def prog3(out1, out2, out3):
    return partial(progn, out1, out2, out3)


def if_then_else(condition, out1, out2):
    out1() if condition() else out2()


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


player = Player()


pset = gp.PrimitiveSet("MAIN", 0)

# todo change
# pset.addPrimitive(ant.if_food_ahead, 2)
pset.addPrimitive(prog2, 2)
pset.addPrimitive(prog3, 3)

pset.addTerminal(player.move_left)
pset.addTerminal(player.move_right)
pset.addTerminal(player.move_down)
pset.addTerminal(player.move_up)

creator.create("FitnessMin", base.Fitness, weights=(1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin)

toolbox = base.Toolbox()

# Attribute generator
toolbox.register("expr_init", gp.genFull, pset=pset, min_=1, max_=2)

# Structure initializers
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr_init)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)


def evalPlayer(individual):
    def count_left_box(level, game):
        """
           :Return
               (The number of boxes out of place) * left_box
        """
        counter = 0
        for row in game.matrix[level - 1]:
            for cell in row:
                if cell == '$':
                    counter = counter + 1
        return counter
    def euclidean_distance(game, from_box, sum=False):
        """
            :Return
                The minimum distance for box from the dock * self.Measure["euclidean_distance"]
        """
        min_distances = []
        row_pos = -1
        for row in game.matrix[0]:
            row_pos = row_pos + 1
            col_pos = -1
            for cell in row:
                col_pos = col_pos + 1
                if cell == '$':
                    distances = []
                    target_row_pos = -1
                    for row_target in game.matrix[0]:
                        target_row_pos = target_row_pos + 1
                        target_col_pos = -1
                        for cell_target in row_target:
                            target_col_pos = target_col_pos + 1
                            if cell_target == from_box:
                                d = numpy.sqrt(((row_pos - target_row_pos) ** 2) + ((col_pos - target_col_pos) ** 2))
                                distances.append(d)
                    min_d = numpy.min(distances)
                    if min_d != 0:
                        min_distances.append(min_d)
        if sum == True:
            score = numpy.sum(min_distances)
        else:
            score = numpy.min(min_distances)

        return score
    # Transform the tree expression to functionnal Python code
    routine = gp.compile(individual, pset)
    # Run the generated routine
    list_move = player.play(routine)
    player.game.play(1, list_move)
    fitness = count_left_box(1, player.game) + euclidean_distance(player.game, ".")
    player.update_fitness(fitness)
    return player.fitness,

toolbox.register("evaluate", evalPlayer)
toolbox.register("select", tools.selTournament, tournsize=7)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)


def main():
    random.seed(69)


    pop = toolbox.population(n=5)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("med", numpy.median)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)

    # 1.2 todo number level - shir
    # 1.3 todo add config - amit
    # 1.4 todo name file - config param + time - amit
    # 1.4 todo fitness - shir
    # 1.5 todo train and test - train each level ot as a group?
    # 1.1 todo graph
    #
    time_before = datetime.now()
    # ngen = The number of generation
    pop, logbook = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=150, stats=stats, halloffame=hof)
    time = time_before.minute - datetime.now().minute

    # numpy.pickle.dump(logbook, open(f"File/logbook_{time}_{todo config}", 'wb'))

    return pop, hof, stats


if __name__ == "__main__":
    main()