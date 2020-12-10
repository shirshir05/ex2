from BFS import BFS
from Fitness.MeasureForFitness import MeasureForFitness


class Fitness:

    def __init__(self, config):
        """
            :param gen_length= maximum number of moves allowed- set to a default value
        """
        self.measure = MeasureForFitness(config)

    def evaluate(self, game, level):

        left_boxes = self.measure.count_left_box(game, level)
        # distance_sum = self.measure.euclidean_distance(game, ".", level)
        # box_deadlock = self.measure.box_deadlock(game, level)
        position_worker = game.worker(level)
        bfs_path = 50 * BFS.bfs(game.matrix, level, (position_worker[1], position_worker[0]))
        # print(f"{level} and left_boxes = {left_boxes} and bfs_path =  {bfs_path}")
        return left_boxes + bfs_path









