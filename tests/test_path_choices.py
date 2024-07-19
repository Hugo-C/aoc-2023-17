from src.floor_is_lava import Map, PathElement, path_choices


def test_no_choice(single_block_map):
    path = [PathElement(0, 0)]
    assert [choice for choice in path_choices(single_block_map, path)] == []


def test_all_choices(rect_map):
    path = [PathElement(1, 1)]
    assert [choice for choice in path_choices(rect_map, path)] == [
        PathElement(0, 1),
        PathElement(1, 0),
        PathElement(2, 1),
        PathElement(1, 2),
    ]


def test_middle_bottom_choices(rect_map):
    path = [PathElement(1, 2)]
    assert [choice for choice in path_choices(rect_map, path)] == [
        PathElement(0, 2),
        PathElement(1, 1),
        PathElement(2, 2),
    ]
