import random
from datetime import datetime

from boto import sns
from networkx.drawing.tests.test_pylab import plt
from numpy.random._generator import default_rng

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
        self.game = None
        self.list_move = []
        self.fitness = float("inf")

    def set_game(self, game):
        self.game = game

    def play(self, routine):
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

# todo remove constant train and test? seed= 42
rng = default_rng(42)
all_levels = range(0, 20)
train_set = rng.choice(20, size=14, replace=False)
test_set = [item for item in all_levels if item not in train_set]


def evalPlayer(individual):
    def euclidean_distance(game, from_box, level, sum=False):
        """
            :Return
                The minimum distance for box from the dock * self.Measure["euclidean_distance"]
        """
        min_distances = []
        row_pos = -1
        for row in game.matrix[level - 1]:
            row_pos = row_pos + 1
            col_pos = -1
            for cell in row:
                col_pos = col_pos + 1
                if cell == '$':
                    distances = []
                    target_row_pos = -1
                    for row_target in game.matrix[level - 1]:
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
        if sum:
            score = numpy.sum(min_distances)
        else:
            score = numpy.min(min_distances)

        return score

    # Transform the tree expression to functionnal Python code
    routine = gp.compile(individual, pset)
    # Run the generated routine
    list_move = player.play(routine)
    fitness = 0
    player.set_game(Game("input.txt", 20))
    for level in train_set:
        player.game.play(level + 1, list_move)
        fitness += euclidean_distance(player.game, ".", level + 1)
    player.update_fitness(fitness)
    return player.fitness,


toolbox.register("evaluate", evalPlayer)
toolbox.register("select", tools.selTournament, tournsize=7)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)


def create_plot(logbook):
    maxFitnessValues, meanFitnessValues, minFitnessValues, medianFitnessValues, stdFitnessValues = \
        logbook.select("max", "avg", "min", "median", "std")
    plt.plot(maxFitnessValues, color='red', label="Best Fitness")
    plt.plot(meanFitnessValues, color='green', label="Mean Fitness")
    plt.plot(minFitnessValues, color='orange', label="Worst Fitness")
    plt.plot(medianFitnessValues, color='blue', label="Avg. Fitness")
    plt.plot(stdFitnessValues, color='pink', label="Std. Fitness")

    plt.xlabel('Generation')
    plt.ylabel('Max / Average / Min / Median/ Std Fitness')
    plt.title('Max, Average, Min, Median and Std Fitness over Generations')
    plt.legend(loc='lower right')
    plt.savefig("currentRun.png")
    plt.close()


def main():
    random.seed(42)
    pop = toolbox.population(n=2)

    #todo config number to HallOfFame
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("med", numpy.median)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)

    # 1.2 todo number level - shir - DONE!
    # 1.3 todo add config - amit
    # 1.4 todo name file - config param + time - amit
    # 1.4 todo fitness - shir - DONE!
    # 1.5 todo train and test - train each level ot as a group? - DONE!
    # 1.1 todo graph

    time_before = datetime.now()
    # ngen = The number of generation
    pop, logbook = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=5, stats=stats, halloffame=hof)
    time = time_before.minute - datetime.now().minute

    # numpy.pickle.dump(logbook, open(f"File/logbook_{time}_{todo config}", 'wb'))
    create_plot(logbook)

    return pop, hof, stats


if __name__ == "__main__":
    main()
