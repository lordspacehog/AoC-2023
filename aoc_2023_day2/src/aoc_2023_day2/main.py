"""
aoc day 2 implementation
"""
from functools import reduce

import click

GAME_ID_SPLIT = ": "
RESULTS_SPLIT = "; "
CUBE_COUNT_SPLIT = ", "

PART1_CUBE_COUNTS = {"red": 12, "green": 13, "blue": 14}


def part1_solve(file_handle):
    out = 0

    for line in file_handle:
        (game_id_part, results_part) = line.strip().split(GAME_ID_SPLIT)
        game_id = int(game_id_part.split(" ")[-1])

        cubes_seen = [
            cube_val.split(" ")
            for result in results_part.split(RESULTS_SPLIT)
            for cube_val in result.split(CUBE_COUNT_SPLIT)
        ]

        cube_count = reduce(
            lambda a, counts: {
                k: max(a.get(k, 0), int(counts[0])) if k == counts[1] else a.get(k, 0)
                for k in set([counts[1]]).union(a.keys())
            },
            cubes_seen,
            {},
        )

        out += (
            game_id
            if not any(
                [
                    True
                    for k in PART1_CUBE_COUNTS.keys()
                    if cube_count.get(k, 0) > PART1_CUBE_COUNTS.get(k)
                ]
            )
            else 0
        )

    print(f"Game ID sum: {out}")


def part2_solve(file_handle):
    out = 0

    for line in file_handle:
        (_, results_part) = line.strip().split(GAME_ID_SPLIT)

        cubes_seen = [
            cube_val.split(" ")
            for result in results_part.split(RESULTS_SPLIT)
            for cube_val in result.split(CUBE_COUNT_SPLIT)
        ]

        cube_count = reduce(
            lambda a, counts: {
                k: max(a.get(k, 0), int(counts[0])) if k == counts[1] else a.get(k, 0)
                for k in set([counts[1]]).union(a.keys())
            },
            cubes_seen,
            {},
        )

        out += reduce(lambda a, b: b * a, cube_count.values())

    print(f"Game power sum: {out}")


@click.command()
@click.option("--part", default=1, type=click.IntRange(1, 2))
@click.argument("puzzle_input", type=click.Path(exists=True, dir_okay=False))
def main(puzzle_input, part):
    with open(puzzle_input) as f:
        match part:
            case 1:
                part1_solve(f)
            case 2:
                part2_solve(f)
            case _:
                return


if __name__ == "__main__":
    main()
