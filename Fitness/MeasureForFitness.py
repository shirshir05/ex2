from configparser import ConfigParser

import numpy as np

dic_position_box = {1: [(2, 5), (3, 7), (4, 5), (4, 7), (7, 2), (7, 5)],
                    2: [(2, 7), (2, 10), (3, 6), (5, 10), (6, 9), (6, 11), (7, 4), (7, 7), (7, 9), (7, 11)],
                    3: [(2, 10), (2, 12), (3, 10), (3, 13), (4, 10), (4, 12), (5, 10), (6, 10), (6, 13), (7, 9),
                        (7, 12)],
                    4: [(3, 8), (3, 10), (4, 2), (4, 3), (4, 4), (4, 6), (4, 9), (5, 3), (5, 9), (6, 2), (6, 3), (6, 6),
                        (6, 8), (6, 10), (7, 3), (10, 6), (11, 3), (11, 4), (11, 6), (11, 7)],
                    5: [(2, 11), (3, 14), (5, 10), (5, 13), (6, 9), (6, 11), (6, 12), (7, 9), (7, 12), (8, 11), (9, 10),
                        (9, 12)],
                    6: [(3, 8), (3, 9), (4, 9), (5, 9), (6, 5), (6, 8), (7, 6), (7, 9), (8, 5), (8, 8)],
                    7: [(2, 9), (2, 10), (3, 5), (4, 3), (5, 9), (6, 2), (7, 2), (7, 4), (7, 6), (9, 2), (9, 3)],
                    8: [(2, 7), (2, 11), (2, 13), (3, 4), (3, 7), (3, 12), (4, 5), (4, 7), (5, 4), (6, 3), (6, 5),
                        (6, 7), (7, 5), (7, 8), (8, 4), (8, 9), (8, 11), (8, 13)],
                    9: [(7, 7), (7, 8), (7, 9), (8, 8), (8, 10), (9, 6), (9, 8), (10, 3), (10, 6), (10, 11), (10, 14),
                        (11, 7), (11, 8), (11, 10)],
                    10: [(2, 2), (2, 3), (2, 7), (2, 8), (2, 11), (2, 13), (3, 3), (3, 4), (3, 5), (3, 11), (4, 2),
                         (4, 8), (4, 9), (4, 11), (4, 12), (5, 9), (6, 8), (6, 10), (6, 12), (8, 9), (8, 11), (9, 8),
                         (9, 9), (9, 11), (9, 13), (10, 9), (11, 8), (11, 9), (11, 10), (11, 12), (11, 13), (11, 14)],
                    11: [(2, 11), (3, 10), (4, 5), (4, 7), (4, 8), (5, 5), (6, 5), (6, 7), (6, 8), (7, 5), (7, 12),
                         (8, 11), (8, 12), (9, 8)],
                    12: [(3, 5), (3, 7), (3, 9), (3, 11), (4, 6), (4, 8), (5, 5), (5, 7), (5, 9), (6, 6), (6, 8),
                         (7, 5), (7, 6), (7, 7), (7, 9)],
                    13: [(3, 3), (3, 6), (4, 4), (4, 7), (5, 6), (6, 2), (6, 7), (7, 10), (7, 12), (8, 2), (8, 12),
                         (9, 3), (9, 6), (9, 10), (9, 13), (10, 2)],
                    14: [(2, 9), (2, 11), (3, 2), (3, 3), (5, 5), (7, 15), (8, 4), (8, 11), (9, 3), (9, 5), (9, 6),
                         (9, 7), (9, 12), (10, 4), (10, 6), (10, 11), (10, 12), (11, 10)],
                    15: [(2, 6), (3, 6), (4, 4), (4, 9), (5, 8), (5, 12), (6, 11), (7, 8), (8, 3), (9, 4), (9, 11),
                         (12, 2), (12, 3)],
                    16: [(3, 2), (4, 3), (4, 4), (4, 6), (4, 10), (5, 6), (6, 8), (6, 10), (7, 3), (8, 5), (8, 8),
                         (9, 7), (11, 4), (11, 5)],
                    17: [(8, 3), (9, 4), (9, 7), (9, 12), (10, 3), (10, 6)],
                    18: [(5, 2), (5, 11), (5, 16), (7, 4), (7, 7), (7, 10), (8, 11), (8, 13), (8, 14), (9, 5), (9, 14)],
                    19: [(2, 6), (4, 2), (5, 2), (6, 3), (6, 6), (7, 3), (7, 5), (8, 6), (9, 6), (11, 3), (12, 5),
                         (12, 10), (13, 4), (13, 7), (13, 10)],
                    20: [(2, 10), (3, 9), (4, 14), (5, 4), (6, 4), (6, 14), (8, 14), (10, 3), (10, 7), (10, 10),
                         (10, 14), (11, 5), (11, 9), (11, 11), (12, 5), (12, 14), (13, 8), (13, 9)]}


class MeasureForFitness:

    def __init__(self, config):
        self.config = config

    def position(self, game, level):
        """
           return position of boxes,free cell, dock and worker
       """
        list_box = []
        list_free = []
        list_dock = []
        worker = None
        index_row = 0
        for row in game.matrix[level - 1]:
            index_col = 0
            for col in row:
                if col == "$":
                    list_box.append((index_row, index_col))
                elif col == " ":
                    list_free.append((index_row, index_col))
                elif col == "*" or col == "." or "+":
                    list_dock.append((index_row, index_col))
                elif col == "@" or col == "+":
                    worker = (index_row, index_col)
                index_col += 1
            index_row += 1
        return list_box, list_free, list_dock, worker

    def count_left_box(self, game, level, cell_param="$"):
        """
           :Return
               (The number of boxes out of place) * left_box
        """
        counter = 0
        for row in game.matrix[level - 1]:
            for cell in row:
                if cell == cell_param:
                    counter = counter + 1
        return int(self.config.left_box) * counter

    @staticmethod
    def euclidean_distance(game, from_box, level, sum=True):
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
                                d = np.sqrt(((row_pos - target_row_pos) ** 2) + ((col_pos - target_col_pos) ** 2))
                                distances.append(d)
                    min_d = np.min(distances)
                    if min_d != 0:
                        min_distances.append(min_d)
        if sum == True:
            score = np.sum(min_distances)
        else:
            score = np.min(min_distances)

        return score

    def box_deadlock(self, game, level):
        """
            :Return
                The number box in deadlock
        """
        counter = 0
        ind_row = 0
        for row in game.matrix[level - 1]:
            ind_col = 0
            for cell in row:
                if cell == '$':
                    # right top corner
                    if row[ind_col + 1] in ['#', '*', '$'] and game.matrix[level - 1][ind_row - 1][ind_col] in [
                        '#', '*', '$']:
                        counter = counter + 1
                    # left top corner
                    if (row[ind_col - 1] in ['#', '*', '$'] and game.matrix[level - 1][ind_row - 1][ind_col] in [
                        '#', '*', '$']):
                        counter = counter + 1
                    # right bottom corner
                    if (row[ind_col - 1] in ['#', '*', '$'] and game.matrix[level - 1][ind_row + 1][ind_col] in [
                        '#', '*', '$']):
                        counter = counter + 1
                    # right bottom corner
                    if (row[ind_col + 1] in ['#', '*', '$'] and game.matrix[level - 1][ind_row + 1][ind_col] in [
                        '#', '*', '$']):
                        counter = counter + 1
                ind_col = ind_col + 1
            ind_row = ind_row + 1
        return int(self.config.box_deadlock) * counter

    def box_move(self, game, level):
        list_init_box = dic_position_box[level]
        list_current_box = game.position_box(level)
        list_move = set(list_init_box) - set(list_current_box)
        return len(list_move)

