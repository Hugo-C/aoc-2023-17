from copy import deepcopy
from typing import Self, Iterator

from src.exceptions import DeadEndException


class PathElement:
    def __init__(self, x: int, y: int):
        self.position = (x, y)

    def __eq__(self, other: Self):
        return self.position == other.position

    def __repr__(self):
        return repr(self.position)


Path = list[PathElement]


def quick_path(*arg):  # used in tests
    return [PathElement(x, y) for (x, y) in arg]


class Map:
    """
    Map of a lava floor composed of "city block" so that the top left is position 0, 0
       x ->
    y  (0, 0) (1, 0)
    ↓  (0, 1) (1, 1)
    """

    def __init__(self, input: str):
        # we assume all lines have the same number of city blocks
        self._map = []
        for line_value in input.split("\n"):
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
        path = [PathElement(0, 0)]
        if self.width == 1 and self.height == 1:
            return path  # very special case
        return self._resolve(path)

    def _resolve(self, path: Path) -> Path:
        min_heat_loss_count = None
        min_heat_loss_path = None
        for path_element in path_choices(self, path):
            if path_element in path:
                continue  # we already passed there
            new_path = deepcopy(path)
            new_path.append(path_element)
            (x, y) = path_element.position
            if x == self.width - 1 and y == self.height - 1:
                # we found a path to the end
                return new_path

            # else we have to go deeper
            try:
                full_path = self._resolve(new_path)
            except DeadEndException:
                continue
            else:
                heat_loss = compute_heat_loss(self, full_path)
                if min_heat_loss_count is None or heat_loss < min_heat_loss_count:
                    min_heat_loss_count = heat_loss
                    min_heat_loss_path = full_path

        if not min_heat_loss_path:  # this is a dead end with no further choices
            raise DeadEndException()
        return min_heat_loss_path


def path_choices(map_: Map, path: Path) -> Iterator[PathElement]:
    current_path_element = path[-1]
    (current_x, current_y) = current_path_element.position
    if current_x > 0:
        yield PathElement(current_x - 1, current_y)
    if current_y > 0:
        yield PathElement(current_x, current_y - 1)
    if current_x + 1 < map_.width:
        yield PathElement(current_x + 1, current_y)
    if current_y + 1 < map_.height:
        yield PathElement(current_x, current_y + 1)


def compute_heat_loss(map_: Map, path: Path) -> int:
    """Returns the heat loss of all blocks passed, lower is better"""
    heat_loss = 0
    for path_element in path:
        heat_loss += map_[path_element.position]
    return heat_loss
