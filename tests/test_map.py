import pytest
from pytest import fixture

from src.floor_is_lava import Map


def test_init_map(rect_map):
    assert rect_map[0, 0] == 2
    assert rect_map[1, 0] == 4
    assert rect_map[0, 1] == 3
    assert rect_map[1, 1] == 5
    assert rect_map[2, 2] == 6


def test_rect_map_length(rect_map):
    assert rect_map.width == 3
    assert rect_map.height == 3


def test_map_4_by_3_length(map_4_by_3):
    assert map_4_by_3.width == 4
    assert map_4_by_3.height == 3


def test_repr_map_4_by_3(map_4_by_3, map_4_by_3_input):
    assert repr(map_4_by_3) == map_4_by_3_input


def test_rect_map_index_error(rect_map):
    with pytest.raises(IndexError):
        _ = rect_map[10, 10]


def test_rect_map_index_error_on_limit(map_4_by_3):
    with pytest.raises(IndexError):
        _ = map_4_by_3[map_4_by_3.width, map_4_by_3.height]
