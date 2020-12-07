from Fitness.MeasureForFitness import MeasureForFitness


class Fitness:

    def __init__(self, config):
        """
            :param gen_length= maximum number of moves allowed- set to a default value
        """
        self.measure = MeasureForFitness(config)

    def evaluate(self, game, level):

        left_boxes = self.measure.count_left_box(game, level)
        distance_sum = self.measure.euclidean_distance(game, ".", level)
        box_deadlock = self.measure.box_deadlock(game, level)
        return left_boxes + distance_sum + box_deadlock









