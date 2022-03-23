import random
from enum import Enum
from math import sqrt
from typing import \
    Dict, \
    List, \
    NamedTuple, \
    Callable, \
    Optional
from generic_funcs.generic_search import \
    dfs, \
    bfs, \
    astar, \
    node_to_path, \
    Node


class Cell(str, Enum):
    EMPTY = " "
    BLOCKED = "X"
    START = "S"
    GOAL = "G"
    PATH = "*"


class MazeLocation(NamedTuple):
    row: int
    column: int


class Maze:
    def __init__(self,
                 rows: int = 10,
                 columns: int = 10,
                 sparseness: float = 0.2,
                 start: MazeLocation = MazeLocation(0, 0),
                 goal: MazeLocation = MazeLocation(9, 9)
                 ) -> None:
        # initialize basic instance variables 
        self._rows: int = rows
        self._columns: int = columns
        self.start: MazeLocation = start
        self.goal: MazeLocation = goal
        # fill the grid with empty cells 
        self._grid: List[List[Cell]] = [[Cell.EMPTY for _ in range(columns)]
                                        for _ in range(rows)]
        # populate the grid with blocked cells 
        self._randomly_fill(rows, columns, sparseness)
        # fill the start and goal locations in
        self._grid[start.row][start.column] = Cell.START
        self._grid[goal.row][goal.column] = Cell.GOAL

    def _randomly_fill(self, rows: int, columns: int, sparseness: float):
        for row in range(rows):
            for column in range(columns):
                if random.uniform(0, 1.0) < sparseness:
                    self._grid[row][column] = Cell.BLOCKED

    def __str__(self) -> str:
        output: str = ""
        for row in self._grid:
            output += "".join([c.value for c in row]) + "\n"
        return output

    def goal_test(self, ml: MazeLocation) -> bool:
        return ml == self.goal

    def successors(self, ml: MazeLocation) -> List[MazeLocation]:
        # noinspection PyCompatibility
        locations: List[MazeLocation] = []
        if ml.row + 1 < self._rows and self._grid[ml.row + 1][ml.column] != \
                Cell.BLOCKED:
            locations.append(MazeLocation(ml.row + 1, ml.column))
        if ml.row - 1 >= 0 and self._grid[ml.row - 1][ml.column] != \
                Cell.BLOCKED:
            locations.append(MazeLocation(ml.row - 1, ml.column))
        if ml.column + 1 < self._columns and \
                self._grid[ml.row][ml.column + 1] != Cell.BLOCKED:
            locations.append(MazeLocation(ml.row, ml.column + 1))
        if ml.column - 1 >= 0 and self._grid[ml.row][ml.column - 1] != \
                Cell.BLOCKED:
            locations.append(MazeLocation(ml.row, ml.column - 1))
        return locations

    def mark(self, path: List[MazeLocation]) -> None: 
        for maze_location in path:
            self._grid[maze_location.row][maze_location.column] = Cell.PATH
        self._grid[self.start.row][self.start.column] = Cell.START
        self._grid[self.goal.row][self.goal.column] = Cell.GOAL

    def clear(self, path: List[MazeLocation]) -> None:
        for maze_location in path:
            self._grid[maze_location.row][maze_location.column] = Cell.EMPTY
        self._grid[self.start.row][self.start.column] = Cell.START
        self._grid[self.goal.row][self.goal.column] = Cell.GOAL


def euclidean_distance(goal: MazeLocation) -> Callable[[MazeLocation], float]:
    def _distance(ml: MazeLocation) -> float:
        xdist: int = ml.column - goal.column
        ydist: int = ml.row - goal.column
        return sqrt((xdist * xdist) + (ydist * ydist))
    return _distance


def manhattan_distance(goal: MazeLocation) -> Callable[[MazeLocation], float]:
    def _distance(ml: MazeLocation) -> float:
        xdist: int = abs(ml.column - goal.column)
        ydist: int = abs(ml.row - goal.row)
        return xdist + ydist
    return _distance


if __name__ == "__main__":
    dfs_results: Dict[str, int] = {"path_length": 0}
    bfs_results: Dict[str, int] = {"path_length": 0}
    astar_results: Dict[str, int] = {"path_length": 0}

    # Test DFS
    m: Maze = Maze()
    solution_1: Optional[Node[MazeLocation]] = dfs(m.start, m.goal_test,
                                                   m.successors)
    if solution_1 is None:
        print(m)
        print("No solution found using depth-first search!")
    else:
        path1: List[MazeLocation] = node_to_path(solution_1)
        m.mark(path1)
        print(m)
        dfs_results["path_length"] = len(path1) 
        m.clear(path1)

    # Test BFS
    solution_2: Optional[Node[MazeLocation]] = bfs(m.start, m.goal_test,
                                                   m.successors)
    if solution_2 is None:
        print(m)
        print("No solution found using breadth-first search!")
    else:
        path2: List[MazeLocation] = node_to_path(solution_2)
        m.mark(path2)
        print(m)
        bfs_results["path_length"] = len(path2)
        m.clear(path2)

    # Test A*
    distance: Callable[[MazeLocation], float] = manhattan_distance(m.goal)
    solution_3: Optional[Node[MazeLocation]] = astar(m.start, m.goal_test,
                                                     m.successors, distance)
    if solution_3 is None:
        print(m)
        print("No solution found using A*!")
    else:
        path3: List[MazeLocation] = node_to_path(solution_3)
        m.mark(path3)
        print(m)
        astar_results["path_length"] = len(path3)
        m.clear(path3)

    # printing results
    print("Depth-first Algorithm: ", dfs_results['path_length'])
    print("Breadth-first Algorithm: ", bfs_results['path_length'])
    print("A* Algorithm: ", astar_results['path_length'])
