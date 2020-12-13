from BFS import BFS
from Fitness.MeasureForFitness import MeasureForFitness


class Fitness:

    def __init__(self, config):
        """
            :param gen_length= maximum number of moves allowed- set to a default value
        """
        self.measure = MeasureForFitness(config)

    def evaluate(self, game, level, list_move):
        n_patterns = 1 * self.measure.pattern(list_move)
        box_in_dock = self.measure.count_left_box(game, level, "*")
        position_worker = game.worker(level)
        bfs_path = 20 * BFS.bfs(game.matrix, level, (position_worker[1], position_worker[0]))
        number_box_move = 20 * self.measure.box_move(game, level)
        box_deadlock = self.measure.box_deadlock(game, level)
        return bfs_path + number_box_move - box_in_dock + box_deadlock + n_patterns
        # distance_sum = self.measure.euclidean_distance(game, ".", level)
