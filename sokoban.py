import random
from copy import copy
from datetime import datetime

from networkx.drawing.tests.test_pylab import plt
from Game import Game
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
from MeasureForFitness import MeasureForFitness


class GP:
    def progn(self, *args):
        for arg in args:
            arg()

    def prog2(self, out1, out2):
        return partial(self.progn, out1, out2)

    def prog3(self, out1, out2, out3):
        return partial(self.progn, out1, out2, out3)

    def if_then_else(self, condition, out1, out2):
        out1() if condition() else out2()

    def evalPlayer(self, set_level, individual):
        # Transform the tree expression to functionnal Python code
        routine = gp.compile(individual, self.pset)
        # Run the generated routine
        list_move = self.player.play(routine)
        fitness = 0
        self.player.set_game(Game("input.txt", 20))
        for level in set_level:
            self.player.game.play(level + 1, list_move)
            fitness += MeasureForFitness.euclidean_distance(self.player.game, ".", level + 1)
        self.player.update_fitness(fitness)
        return self.player.fitness,

    def __init__(self):
        config = ParseConfig("File/config.ini")
        self.pop_size = config.get_population_size()
        self.seed_num = config.get_random_seed()
        self.ngen = config.get_ngen()
        self.crossover_prob = config.get_crossover_prob()
        self.mutation_prob = config.get_mutation_prob()
        self.fitness = config.get_fitness()
        self.mate = config.get_crossover()
        self.mutate = config.get_mutation()

        self.player = Player()
        self.pset = gp.PrimitiveSet("MAIN", 0)

        # todo change
        # pset.addPrimitive(ant.if_food_ahead, 2)
        self.pset.addPrimitive(self.prog2, 2)
        self.pset.addPrimitive(self.prog3, 3)
        self.pset.addTerminal(self.player.move_left)
        self.pset.addTerminal(self.player.move_right)
        self.pset.addTerminal(self.player.move_down)
        self.pset.addTerminal(self.player.move_up)

        creator.create("FitnessMin", base.Fitness, weights=(1.0,))
        creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin)

        self.toolbox = base.Toolbox()

        # Attribute generator
        self.toolbox.register("expr_init", gp.genFull, pset=self.pset, min_=1, max_=2)

        # Structure initializers
        self.toolbox.register("individual", tools.initIterate, creator.Individual, self.toolbox.expr_init)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)

        rng = default_rng(int(self.seed_num))
        all_levels = range(0, 20)
        self.train_set = rng.choice(20, size=14, replace=False)
        self.test_set = [item for item in all_levels if item not in self.train_set]

        self.toolbox.register("evaluate", self.evalPlayer, self.train_set)
        self.toolbox.register("select", tools.selTournament, tournsize=7)
        self.toolbox.register("mate", self.mate)
        self.toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
        self.toolbox.register("mutate", self.mutate, expr=self.toolbox.expr_mut, pset=self.pset)

    @staticmethod
    def create_plot(logbook):
        maxFitnessValues, meanFitnessValues, minFitnessValues, medianFitnessValues, stdFitnessValues = \
            logbook.select("max", "avg", "min", "median", "std")
        plt.plot(maxFitnessValues, color='red', label="Worst Fitness")
        plt.plot(meanFitnessValues, color='green', label="Mean Fitness")
        plt.plot(minFitnessValues, color='orange', label="Best Fitness")
        plt.plot(medianFitnessValues, color='blue', label="Avg. Fitness")
        plt.plot(stdFitnessValues, color='pink', label="Std. Fitness")

        plt.xlabel('Generation')
        plt.ylabel('Max / Average / Min / Median/ Std Fitness')
        plt.title('Max, Average, Min, Median and Std Fitness over Generations')
        plt.legend(loc='lower right')
        plt.savefig("currentRun.png")
        plt.close()

    def run(self):
        random.seed(self.seed_num)
        pop = self.toolbox.population(n=self.pop_size)
        hof = tools.HallOfFame(1)
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        # stats_size = tools.Statistics(key=self.stats_key_1)
        # mstats = tools.MultiStatistics(fitness=stats, size=stats_size)

        stats.register("avg", numpy.mean)
        stats.register("std", numpy.std)
        stats.register("med", numpy.median)
        stats.register("min", numpy.min)
        stats.register("max", numpy.max)

        # 1.4 todo name file - config param + time - amit

        time_before = datetime.now()
        # ngen = The number of generation
        pop, logbook = algorithms.eaSimple(pop, self.toolbox,
                                           cxpb=self.crossover_prob,
                                           mutpb=self.mutation_prob,
                                           ngen=self.ngen,
                                           stats=stats,
                                           halloffame=hof)

        # ngen = The number of generation
        time = time_before.minute - datetime.now().minute

        # numpy.pickle.dump(logbook, open(f"File/logbook_{time}_{todo config}", 'wb'))
        GP.create_plot(logbook)
        dic_inv = {}
        for ind in pop:
            dic_inv[ind] = self.evalPlayer(ind, self.test_set)
        print(dic_inv.values())

        return pop, hof, stats


if __name__ == "__main__":
    gp_sokoban = GP()
    gp_sokoban.run()
