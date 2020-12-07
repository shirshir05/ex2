import sys
from configparser import ConfigParser

import numpy as np
from MeasureForFitness import MeasureForFitness
from Game import Game


class Fitness:

    def __init__(self, gen_length, name_file):
        """
            :param gen_length= maximum number of moves allowed- set to a default value
        """
        self.gen_length = gen_length
        self.measure = MeasureForFitness()
        self.config_object = ConfigParser()
        self.name_file = name_file
        self.config_object.read(name_file)
        self.Measure = self.config_object["Measure"]


    def evaluate(self, game, level):

        left_boxes = self.measure.count_left_box(level)
        distance_sum = self.measure.euclidean_distance(game,".", level, True)



        return 0









