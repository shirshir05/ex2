from fitness import *
from deap import tools
from deap import gp

class ParseConfig:

    def __init__(self, file_name):
        # <editor-fold desc="Dictionaries">
        self.fitness_dict = {"AreaLengthFitness": AreaLengthFitness,
                             "AbsDifferenceSolutionLengthFitness": AbsDifferenceSolutionLengthFitness,
                             "SimpleDistanceFitness": SimpleDistanceFitness,
                             "DistanceAndBox": DistanceAndBox,
                             }

        self.crossover_dict = {"cxSemantic": gp.cxSemantic,
                               "cxOnePointLeafBiased": gp.cxOnePointLeafBiased,
                               "cxOnePoint": gp.cxOnePoint}

        self.mutate_dict = {"mutShrink": gp.mutShrink,
                            "mutUniform": gp.mutUniform,
                            "mutNodeReplacement": gp.mutNodeReplacement,
                            "mutEphemeral": gp.mutEphemeral,
                            "mutInsert": gp.mutInsert,
                            "mutSemantic": gp.mutSemantic}
        # </editor-fold>
        self.config_object = ConfigParser()
        self.file_name = file_name
        self.config_object.read(file_name)

        # params
        self.params = self.config_object["PARAMS"]
        self.size_population_init = int(self.params["size_population_init"])
        self.size_feature = int(self.params["size_feature"])  # size_feature >= 253
        self.seed_number = float(self.params["seed_number"])
        self.number_run = int(self.params["number_run"])

        # Probs
        self.probs = self.config_object["PROBS"]
        self.cross_over_prob = float(self.probs["cross_over_prob"])
        self.mutation_prob = float(self.probs["mutation_prob"])

        # operators
        self.operators = self.config_object["OPERATORS"]
        self.fitness = self.fitness_dict[self.operators["fitness"]](self.size_feature, file_name)
        self.crossover = self.crossover_dict[self.operators["mate"]]
        self.mutate = self.mutate_dict[self.operators["mutate"]]
        # endregion

    def get_population_size(self):
        return self.size_population_init

    def get_feature_size(self):
        return self.size_feature

    def get_random_seed(self):
        return self.seed_number

    def get_ngen(self):
        return self.number_run

    def get_crossover_prob(self):
        return self.cross_over_prob

    def get_mutation_prob(self):
        return self.mutation_prob

    def get_fitness(self):
        return self.fitness

    def get_crossover(self):
        return self.crossover

    def get_mutation(self):
        return self.mutate
