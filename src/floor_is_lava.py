import sys
from enum import StrEnum
from typing import Self, Iterator
from itertools import groupby

from line_profiler import profile

from src.exceptions import DeadEndException
from src.memoize import memoize

MAX_MOVE_IN_THE_SAME_DIRECTION = 3

# We need to increase the max recursion for big maps
current_recursion_limit = sys.getrecursionlimit()
sys.setrecursionlimit(max(current_recursion_limit, 100_000))


class Direction(StrEnum):
    X_PLUS = ">"
    X_MINUS = "<"
    Y_PLUS = "v"
    Y_MINUS = "^"

    def inverse(self) -> Self:
        match self:
            case self.X_PLUS:
                return self.X_MINUS
            case self.X_MINUS:
                return self.X_PLUS
            case self.Y_PLUS:
                return self.Y_MINUS
            case self.Y_MINUS:
                return self.Y_PLUS


class PathElement:
    def __init__(self, x: int, y: int, previous_directions=None):
        """directions are from oldest to newest"""
        self.position = (x, y)
        self.previous_directions = previous_directions or []
        self.previous_directions = self.previous_directions[-MAX_MOVE_IN_THE_SAME_DIRECTION:]

    def __eq__(self, other: Self):
        return self.position == other.position and self.previous_directions == other.previous_directions

    def __hash__(self):
        return hash(self.position)

    def __repr__(self):
        return repr(self.position)

    @property
    def debug_display(self):  # usefull in debugger
        return repr(self) + "".join([str(direction) for direction in self.previous_directions])


Path = list[PathElement]


def quick_path(*arg):  # used in tests
    path = []
    previous_x = None
    previous_y = None
    previous_directions = []
    for (x, y) in arg:
        direction = None
        if previous_x is not None and previous_x + 1 == x:
            direction = Direction.X_PLUS
        elif previous_x is not None and previous_x - 1 == x:
            direction = Direction.X_MINUS
        elif previous_y is not None and previous_y + 1 == y:
            direction = Direction.Y_PLUS
        elif previous_y is not None and previous_y - 1 == y:
            direction = Direction.Y_MINUS
        if direction:
            previous_directions.append(direction)
        path.append(PathElement(x, y, previous_directions=previous_directions))
        previous_x = x
        previous_y = y
    return path


class Map:
    """
    Map of a lava floor composed of "city block" so that the top left is position 0, 0
       x ->
    y  (0, 0) (1, 0)
    ↓  (0, 1) (1, 1)
    """

    def __init__(self, text_input: str):
        # we assume all lines have the same number of city blocks
        self._map = []
        for line_value in text_input.split("\n"):
            line = []
            for block_value in line_value:
                line.append(int(block_value))
            self._map.append(line)

    @property
    def width(self):
        return len(self._map[0])

    @property
    def height(self):
        return len(self._map)

    def __getitem__(self, position: tuple) -> int:
        (x, y) = position
        return self._map[y][x]

    def __repr__(self):
        lines = []
        for y in range(self.height):
            line = ""
            for x in range(self.width):
                line += str(self[x, y])
            lines.append(line)
        return "\n".join(lines)

    def resolve(self) -> Path:
        start_path = [PathElement(0, 0)]
        if self.width == 1 and self.height == 1:
            return start_path  # very special case
        result_path, _result_heat_loss = self._resolve(start_path)
        return result_path

    @memoize
    @profile
    def _resolve(self, path: Path) -> tuple[Path, int]:
        start_path_element = path[-1]
        min_heat_loss_count = None
        min_heat_loss_path = None
        for path_element in path_choices(self, start_path_element):
            (x, y) = path_element.position
            if x == self.width - 1 and y == self.height - 1:
                # we found a path to the end
                return [start_path_element, path_element], self[path_element.position]

            # else we have to go deeper
            try:
                rest_of_the_path, heat_loss = self._resolve(path + [path_element])
            except DeadEndException:
                continue
            else:
                heat_loss += self[path_element.position]
                if min_heat_loss_count is None or heat_loss < min_heat_loss_count:
                    min_heat_loss_count = heat_loss
                    min_heat_loss_path = rest_of_the_path

        if not min_heat_loss_path:  # this is a dead end with no further choices
            raise DeadEndException()
        return [start_path_element] + min_heat_loss_path, min_heat_loss_count


def all_equal(list_to_check: list) -> bool:  # a bit faster than using all(x == l[0] for x in l)
    g = groupby(list_to_check)
    return next(g, True) and not next(g, False)


def path_element_excluded_directions(path_element: PathElement) -> set[Direction]:
    excluded_directions = set()
    previous_directions = path_element.previous_directions
    if previous_directions:
        excluded_directions.add(previous_directions[-1].inverse())
    # we use the fact that PathElement truncate to this value
    if len(previous_directions) == MAX_MOVE_IN_THE_SAME_DIRECTION:
        if all_equal(previous_directions):
            excluded_directions.add(previous_directions[0])
    return excluded_directions


def path_choices(map_: Map, path_element: PathElement) -> Iterator[PathElement]:
    excluded_direction = path_element_excluded_directions(path_element)
    (current_x, current_y) = path_element.position
    previous_directions = path_element.previous_directions
    if current_x > 0 and Direction.X_MINUS not in excluded_direction:
        yield PathElement(current_x - 1, current_y, previous_directions=previous_directions + [Direction.X_MINUS])
    if current_y > 0 and Direction.Y_MINUS not in excluded_direction:
        yield PathElement(current_x, current_y - 1, previous_directions=previous_directions + [Direction.Y_MINUS])
    if current_x + 1 < map_.width and Direction.X_PLUS not in excluded_direction:
        yield PathElement(current_x + 1, current_y, previous_directions=previous_directions + [Direction.X_PLUS])
    if current_y + 1 < map_.height and Direction.Y_PLUS not in excluded_direction:
        yield PathElement(current_x, current_y + 1, previous_directions=previous_directions + [Direction.Y_PLUS])


def compute_heat_loss(map_: Map, path: Path) -> int:
    """Returns the heat loss of all blocks passed, lower is better"""
    heat_loss = 0
    for path_element in path:
        heat_loss += map_[path_element.position]
    return heat_loss


if __name__ == '__main__':
    # to run with profiler on, set LINE_PROFILE=1
    init = (
        "2413432311323\n"
        "3215453535623\n"
        "3255245654254\n"
        "3446585845452\n"
        "4546657867536\n"
        "1438598798454\n"
        "4457876987766\n"
        "3637877979653\n"
        "4654967986887\n"
        "4564679986453\n"
        "1224686865563\n"
        "2546548887735\n"
        "4322674655533"
    )
    some_map = Map(init)
    result_path = some_map.resolve()
    print("result path:")
    print(result_path)
    print("heat loss incurred:")
    print(compute_heat_loss(some_map, result_path[1:]))  # starting block is not counted
    print("result path in details:")
    print([path_element.debug_display for path_element in result_path])
