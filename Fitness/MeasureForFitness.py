from configparser import ConfigParser

import numpy as np



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

    def count_left_box(self, game,  level):
        """
           :Return
               (The number of boxes out of place) * left_box
        """
        counter = 0
        for row in game.matrix[level - 1]:
            for cell in row:
                if cell == '$':
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
        for row in game.matrix[level-1]:
            row_pos = row_pos + 1
            col_pos = -1
            for cell in row:
                col_pos = col_pos + 1
                if cell == '$':
                    distances = []
                    target_row_pos = -1
                    for row_target in game.matrix[level-1]:
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

