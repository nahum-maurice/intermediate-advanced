from generic_funcs.csp import Constraint, CSP
from typing import Dict, List, Optional


class MapColoringConstraint(Constraint[str, str]):
    def __init__(self, place_1: str, place_2: str):
        super().__init__([place_1, place_2])
        self.place_1: str = place_1
        self.place_2: str = place_2

    def satisfied(self, assignment: Dict[str, str]) -> bool:
        # If either place is not in the assignment, then it is not yet
        # possible for their colors to be conflicting
        if self.place_1 not in assignment or self.place_2 not in assignment:
            return True
        # check the color assigned to place_1 is not the same as the color
        # assigned to place_2
        return assignment[self.place_1] != assignment[self.place_2]


if __name__ == "__main__":
    # the variables
    variables: List[str] = [
        "Western Australia",
        "Northern Territory",
        "South Australia",
        "Queensland",
        "New South Wales",
        "Victoria",
        "Tasmania"
    ]

    # the domains for variables
    domains: Dict[str, List[str]] = {}
    for variable in variables:
        domains[variable] = ["red", "green", "blue"]

    # add binary constraints
    csp: CSP[str, str] = CSP(variables, domains)
    csp.add_constraint(MapColoringConstraint("Western Australia",
                                             "Northern Territory"))
    csp.add_constraint(MapColoringConstraint("Western Australia",
                                             "South Australia"))
    csp.add_constraint(MapColoringConstraint("South Australia",
                                             "Northern Territory"))
    csp.add_constraint(MapColoringConstraint("Queensland",
                                             "Northern Territory"))
    csp.add_constraint(MapColoringConstraint("Queensland", "South Australia"))
    csp.add_constraint(MapColoringConstraint("Queensland", "New South Wales"))
    csp.add_constraint(MapColoringConstraint("New South Wales",
                                             "South Australia"))
    csp.add_constraint(MapColoringConstraint("Victoria", "South Australia"))
    csp.add_constraint(MapColoringConstraint("Victoria", "New South Wales"))
    csp.add_constraint(MapColoringConstraint("Victoria", "Tasmania"))

    # find solution
    solution: Optional[Dict[str, str]] = csp.backtracking_search()
    if solution is None:
        print("No solution found!")
    else:
        print(solution)
