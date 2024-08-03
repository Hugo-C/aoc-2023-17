import pytest

from src.exceptions import DeadEndException
from src.floor_is_lava import Map, PathElement, quick_path, Direction, compute_heat_loss


def test_path_element_repr():
    assert repr(PathElement(0, 0)) == "(0, 0)"


def test_path_element_debug_display():
    assert PathElement(0, 0, previous_directions=[Direction.X_PLUS] * 3).debug_display == "(0, 0)>>>"


def test_path_element_previous_directions_is_truncated_to_3():
    newest_directions = [Direction.X_PLUS] * 2 + [Direction.Y_MINUS]
    directions = [Direction.X_MINUS] + newest_directions
    assert PathElement(0, 0, previous_directions=directions) == PathElement(0, 0, previous_directions=newest_directions)


def test_simplest_path(single_block_map):
    path = single_block_map.resolve()
    assert path == [PathElement(0, 0)]


def test_is_element_in_path_true():
    path = [PathElement(0, 0), PathElement(1, 0)]
    assert PathElement(1, 0) in path


def test_is_element_in_path_false():
    path = [PathElement(0, 0), PathElement(1, 0)]
    assert PathElement(0, 1) not in path


def test_quick_path():
    assert quick_path((0, 0), (0, 1), (1, 1)) == [
        PathElement(0, 0, previous_directions=[]),
        PathElement(0, 1, previous_directions=[Direction.Y_PLUS]),
        PathElement(1, 1, previous_directions=[Direction.Y_PLUS, Direction.X_PLUS]),
    ]


def test_quick_path_2():
    assert quick_path((2, 0), (2, 1)) == [
        PathElement(2, 0, previous_directions=[]),
        PathElement(2, 1, previous_directions=[Direction.Y_PLUS]),
    ]


def test_resolve_rect_map(rect_map):
    result = rect_map.resolve()
    expected_result = quick_path((0, 0), (1, 0), (2, 0), (2, 1), (2, 2))
    assert result == expected_result, [path_element.debug_display for path_element in expected_result]


def test_resolve_with_no_more_than_3_blocks_in_the_same_direction():
    init = (
        "155\n"
        "155\n"
        "155\n"
        "155\n"
        "111"
    )
    map_ = Map(init)
    assert map_.resolve() == quick_path((0, 0), (0, 1), (0, 2), (0, 3), (1, 3), (1, 4), (2, 4))


def test_resolve_with_no_u_turn():
    init = (
        "1\n"
        "1\n"
        "1\n"
        "1\n"
        "1"
    )
    map_ = Map(init)
    with pytest.raises(DeadEndException):
        map_.resolve()


def test_resolve_special_bug():
    init = (
        "36\n"
        "54\n"
        "66\n"
        "53\n"
        "87\n"
        "53\n"
        "63\n"
        "35\n"
        "33"
    )
    map_ = Map(init)
    result = map_.resolve()
    expected_path = quick_path((0, 0), (0, 1), (0, 2), (0, 3), (1, 3), (1, 4), (1, 5), (1, 6), (0, 6), (0, 7), (0, 8),
                               (1, 8))
    assert result == expected_path
    assert compute_heat_loss(map_, expected_path) == compute_heat_loss(map_, result)
    assert compute_heat_loss(map_, expected_path) == 50


def test_resolve_map_aoc_example(map_aoc_example):
    result = map_aoc_example.resolve()
    heat_loss = compute_heat_loss(map_aoc_example, result[1:])
    assert heat_loss <= 102, [path_element.debug_display for path_element in result]
