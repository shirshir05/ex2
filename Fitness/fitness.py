from BFS import BFS
from Fitness.MeasureForFitness import MeasureForFitness

# todo think if ok
dic_push = {1: 97, 2: 133, 3: 138, 4: 365, 5: 143, 6: 110, 7: 124, 8: 245, 9: 239, 11: 526,
            17: 213, 19: 302, }
dic_move = {1: 253, 2: 508, 3: 375, 4: 939, 5: 406, 6: 328, 7: 369, 8: 724, 9: 610, 11: 1476,
            17: 213, 19: 302, }


class Fitness:

    def __init__(self, config):
        """
            :param gen_length= maximum number of moves allowed- set to a default value
        """
        self.measure = MeasureForFitness(config)

    def evaluate(self, game, level, number_push=0):
        # left_boxes = self.measure.count_left_box(game, level)
        boxes_in_place = self.measure.count_left_box(game, level, "*")
        # distance_sum = self.measure.euclidean_distance(game, ".", level)
        # box_deadlock = self.measure.box_deadlock(game, level)
        position_worker = game.worker(level)
        bfs_path = 50 * BFS.bfs(game.matrix, level, (position_worker[1], position_worker[0]))
        # print(f"bfs_path = {bfs_path} boxes_in_place = {boxes_in_place}")
        # print(f"{level} and left_boxes = {left_boxes} and bfs_path =  {bfs_path}")
        return bfs_path - boxes_in_place
