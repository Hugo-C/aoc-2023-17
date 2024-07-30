from src.floor_is_lava import Map, PathElement, path_choices, compute_heat_loss, quick_path


def test_single_block(rect_map):
    path = [PathElement(1, 1)]

    assert compute_heat_loss(rect_map, path) == int(rect_map[1, 1])


def test_single_block_corner(rect_map):
    path = [PathElement(2, 0)]

    assert compute_heat_loss(rect_map, path) == 1


def test_multiple_block(rect_map):
    # Path does not have to be correct
    path = [PathElement(0, 0), PathElement(1, 1), PathElement(2, 2)]

    assert compute_heat_loss(rect_map, path) == 2 + 5 + 6


def test_multiple_block_corner(rect_map):
    # Path does not have to be correct
    path = [PathElement(0, 0), PathElement(0, 1), PathElement(0, 2), PathElement(1, 2), PathElement(2, 2)]

    assert compute_heat_loss(rect_map, path) == 2 + 3 + 3 + 2 + 6


def test_other_map():
    init = (
        "53\n"
        "87\n"
        "53\n"
        "63\n"
        "35\n"
        "33"
    )
    map_ = Map(init)
    path = quick_path((0, 0), (1, 0), (1, 1), (1, 2), (1, 3), (0, 3), (0, 4), (0, 5), (1, 5))
    assert compute_heat_loss(map_, path) == 36


def test_map_aoc_example(map_aoc_example):
    path = quick_path(
        (0, 0),
        (1, 0),
        (2, 0),
        (2, 1),
        (3, 1),
        (4, 1),
        (5, 1),
        (5, 0),
        (6, 0),
        (7, 0),
        (8, 0),
        (8, 1),
        (8, 2),
        (9, 2),
        (10, 2),
        (10, 3),
        (10, 4),
        (11, 4),
        (11, 5),
        (11, 6),
        (11, 7),
        (12, 7),
        (12, 8),
        (12, 9),
        (12, 10),
        (11, 10),
        (11, 11),
        (11, 12),
        (12, 12),
    )
    assert compute_heat_loss(map_aoc_example, path[1:]) == 102
