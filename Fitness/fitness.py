from BFS import BFS
from Fitness.MeasureForFitness import MeasureForFitness


class Fitness:

    def __init__(self, config):
        """
            :param gen_length= maximum number of moves allowed- set to a default value
        """
        self.measure = MeasureForFitness(config)

    def evaluate(self, game, level, list_move):
        # n_patterns = 5 * self.measure.pattern(list_move)  # 0 <= 0 - 60 <= 300
        box_in_dock = self.measure.count_left_box(game, level, "*")  # 0<= 0 - 100 <= count*100
        # position_worker = game.worker(level)
        # bfs_path = 20 * BFS.bfs(game.matrix, level, (position_worker[1], position_worker[0]))
        number_box_move = 150 * self.measure.box_move(game, level)  # 0 <= 0 - 20 <= 200
        # box_deadlock = self.measure.box_deadlock(game, level)   # 0 <= 0 - 20 < = 20 * 2 = 40
        return -number_box_move - box_in_dock #+ n_patterns
        # distance_sum = self.measure.euclidean_distance(game, ".", level)
