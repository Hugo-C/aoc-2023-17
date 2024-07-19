from src.floor_is_lava import Map, PathElement, quick_path


def test_path_element_repr():
    assert repr(PathElement(0, 0)) == "(0, 0)"


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
        PathElement(0, 0),
        PathElement(0, 1),
        PathElement(1, 1),
    ]


def test_resolve_rect_map(rect_map):
    assert rect_map.resolve() == quick_path((0, 0), (1, 0), (2, 0), (2, 1), (2, 2))
