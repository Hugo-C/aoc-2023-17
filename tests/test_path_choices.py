from src.floor_is_lava import Map, PathElement, path_choices, Direction


def test_no_choice(single_block_map):
    path = [PathElement(0, 0)]
    assert [choice for choice in path_choices(single_block_map, path)] == []


def test_all_choices(rect_map):
    path = [PathElement(1, 1)]
    assert [choice for choice in path_choices(rect_map, path)] == [
        PathElement(0, 1, previous_directions=[Direction.X_MINUS]),
        PathElement(1, 0, previous_directions=[Direction.Y_MINUS]),
        PathElement(2, 1, previous_directions=[Direction.X_PLUS]),
        PathElement(1, 2, previous_directions=[Direction.Y_PLUS]),
    ]


def test_middle_bottom_choices(rect_map):
    path = [PathElement(1, 2)]
    assert [choice for choice in path_choices(rect_map, path)] == [
        PathElement(0, 2, previous_directions=[Direction.X_MINUS]),
        PathElement(1, 1, previous_directions=[Direction.Y_MINUS]),
        PathElement(2, 2, previous_directions=[Direction.X_PLUS]),
    ]


def test_inverse_direction_is_excluded_from_choices(rect_map):
    path = [PathElement(1, 1, previous_directions=[Direction.Y_PLUS])]
    assert [choice for choice in path_choices(rect_map, path)] == [
        PathElement(0, 1, previous_directions=[Direction.Y_PLUS, Direction.X_MINUS]),
        # PathElement(1, 0),  # excluded as this would be an u turn
        PathElement(2, 1, previous_directions=[Direction.Y_PLUS, Direction.X_PLUS]),
        PathElement(1, 2, previous_directions=[Direction.Y_PLUS, Direction.Y_PLUS]),
    ]


def test_same_direction_is_excluded_on_the_4th_time(rect_map):
    previous_directions = [Direction.Y_PLUS] * 3
    path = [PathElement(1, 1, previous_directions=[Direction.Y_PLUS] * 3)]
    assert [choice for choice in path_choices(rect_map, path)] == [
        PathElement(0, 1, previous_directions=previous_directions + [Direction.X_MINUS]),
        # PathElement(1, 0),  # u turn
        PathElement(2, 1, previous_directions=previous_directions + [Direction.X_PLUS]),
        # PathElement(1, 2),  # not proposed as we already moved to Y_PLUS 3 times
    ]


def test_same_direction_is_included_on_the_3rd_time(rect_map):
    previous_directions = [Direction.Y_PLUS] * 2
    path = [PathElement(1, 1, previous_directions=previous_directions)]
    assert [choice for choice in path_choices(rect_map, path)] == [
        PathElement(0, 1, previous_directions=previous_directions + [Direction.X_MINUS]),
        # PathElement(1, 0),  # u turn
        PathElement(2, 1, previous_directions=previous_directions + [Direction.X_PLUS]),
        PathElement(1, 2, previous_directions=previous_directions + [Direction.Y_PLUS]),
    ]
