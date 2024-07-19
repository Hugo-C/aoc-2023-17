from src.floor_is_lava import Map, PathElement, path_choices, compute_heat_loss


def test_single_block(rect_map):
    path = [PathElement(1, 1)]

    assert compute_heat_loss(rect_map, path) == int(rect_map[1, 1])


def test_multiple_block(rect_map):
    # Path does not have to be correct
    path = [PathElement(0, 0), PathElement(1, 1), PathElement(2, 2)]

    assert compute_heat_loss(rect_map, path) == 2 + 5 + 6
