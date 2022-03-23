from __future__ import annotations
from typing import List, Optional
from generic_funcs.generic_search import bfs, Node, node_to_path

MAX_NUM: int = 3


class MCState:
    def __init__(self, missionaries: int, cannibals: int, boat: bool) -> None:
        self.wm: int = missionaries  # west missionaries
        self.wc: int = cannibals
        self.em: int = MAX_NUM - self.wm  # east missionaries
        self.ec: int = MAX_NUM - self.wc
        self.boat: bool = boat

    def __str__(self) -> str:
        place = "west" if self.boat else "east"
        return (
            f"Missionaries at west: {self.wm}\n"
            f"Missionaries at east: {self.em}\n"
            f"Cannibals at west: {self.wc}\n"
            f"Cannibals at east: {self.ec}\n"
            f"The boat is at the {place} bank"
        )

    def goal_test(self) -> bool:
        return self.is_legal and self.em == MAX_NUM and self.ec == MAX_NUM

    @property
    def is_legal(self) -> bool:
        if self.wc > self.wm > 0:
            return False
        if self.ec > self.em > 0:
            return False
        return True

    def successors(self) -> List[MCState]:
        sucs: List[MCState] = []
        if self.boat:  # boat on the west
            if self.wm > 1:
                sucs.append(MCState(self.wm - 2, self.wc, not self.boat))
            if self.wm > 0:
                sucs.append(MCState(self.wm - 1, self.wc, not self.boat))
            if self.wc > 1:
                sucs.append(MCState(self.wm, self.wc - 2, not self.boat))
            if self.wc > 0:
                sucs.append(MCState(self.wm, self.wc - 1, not self.boat))
            if (self.wc > 0) and (self.wm > 0):
                sucs.append(MCState(self.wm - 1, self.wc - 1, not self.boat))
        else:  # boat on the east
            if self.em > 1:
                sucs.append(MCState(self.wm + 2, self.wc, not self.boat))
            if self.em > 0:
                sucs.append(MCState(self.wm + 1, self.wc, not self.boat))
            if self.ec > 1:
                sucs.append(MCState(self.wm, self.wc + 2, not self.boat))
            if self.ec > 0:
                sucs.append(MCState(self.wm, self.wc + 1, not self.boat))
            if (self.ec > 0) and (self.em > 0):
                sucs.append(MCState(self.wm + 1, self.wc + 1, not self.boat))
        return [x for x in sucs if x.is_legal]


def display_solution(path_to_display: List[MCState]):
    if len(path_to_display) == 0:  # sanity check
        return
    old_state: MCState = path_to_display[0]
    print(old_state)
    for current_state in path_to_display[1:]:
        if current_state.boat:
            print(f"{old_state.em - current_state.em} missionaries "
                  f"and {old_state.ec - current_state.ec} cannibals "
                  f"moved from the east to west.")
        else:
            print(f"{old_state.wm - current_state.wm} missionaries "
                  f"and {old_state.wc - current_state.wc} cannibals "
                  f"moved from the west to east.")
        # print(current_state)
        old_state = current_state


if __name__ == "__main__":
    start: MCState = MCState(MAX_NUM, MAX_NUM, True)
    solution: Optional[Node[MCState]] = bfs(start, MCState.goal_test,
                                            MCState.successors)
    if solution is None:
        print("No solution found!")
    else:
        path: List[MCState] = node_to_path(solution)
        display_solution(path)
