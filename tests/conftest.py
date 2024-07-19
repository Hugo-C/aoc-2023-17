from pytest import fixture

from src.floor_is_lava import Map


@fixture
def single_block_map():
    init = (
        "2"
    )
    return Map(init)

@fixture
def rect_map():
    init = (
        "241\n"
        "351\n"
        "326"
    )
    return Map(init)


@fixture
def map_4_by_3_input():
    return (
        "2411\n"
        "3512\n"
        "3263"
    )


@fixture
def map_4_by_3(map_4_by_3_input):
    return Map(map_4_by_3_input)