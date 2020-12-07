import random
from datetime import datetime

from Player import Player
from numpy.random._generator import default_rng



from functools import partial
import numpy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp
from ParseConfig import ParseConfig

config = ParseConfig("File/config.ini")
pop_size = config.get_population_size()
seed_num = config.get_random_seed()
ngen = config.get_ngen()
crosover_prob = config.get_crossover_prob()
mutation_prob = config.get_mutation_prob()
fitness = config.get_fitness()
mate = config.get_crossover()
mutate = config.get_mutation()


def progn(*args):
    for arg in args:
        arg()


def prog2(out1, out2):
    return partial(progn, out1, out2)


def prog3(out1, out2, out3):
    return partial(progn, out1, out2, out3)


def if_then_else(condition, out1, out2):
    out1() if condition() else out2()



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
    fitness = 0
    player.set_game(Game("input.txt", 20))
    for level in train_set:
        player.game.play(level + 1, list_move)
        fitness += euclidean_distance(player.game, ".", level + 1)
    player.update_fitness(fitness)
    return player.fitness,


toolbox.register("evaluate", evalPlayer)
toolbox.register("select", tools.selTournament, tournsize=7)
toolbox.register("mate", mate)
toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
toolbox.register("mutate", mutate, expr=toolbox.expr_mut, pset=pset)


def main():
    random.seed(42)
    pop = toolbox.population(n=pop_size)
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
    pop, logbook = algorithms.eaSimple(pop, toolbox,
                                       cxpb=crosover_prob,
                                       mutpb=mutation_prob,
                                       ngen=ngen,
                                       stats=stats,
                                       halloffame=hof)

    time = time_before.minute - datetime.now().minute

    # numpy.pickle.dump(logbook, open(f"File/logbook_{time}_{todo config}", 'wb'))

    return pop, hof, stats


if __name__ == "__main__":
    main()
