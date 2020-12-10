import collections


class BFS:

    @staticmethod
    def bfs(grid, level, start):
        queue = collections.deque([[start]])
        seen = {start}
        while queue:
            path = queue.popleft()
            x, y = path[-1]
            if grid[level-1][y][x] == ".":
                return 0
            for x2, y2 in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if 0 <= x2 < len(grid[level-1][0]) and 0 <= y2 < len(grid[level-1]) and grid[level-1][y2][x2] != "$" \
                        and grid[level-1][y2][x2] != "#" and (x2, y2) not in seen:
                    queue.append(path + [(x2, y2)])
                    seen.add((x2, y2))
        return 1