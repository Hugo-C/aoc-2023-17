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


@fixture
def map_aoc_example():
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
    return Map(init)
