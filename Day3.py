"""
--- Part 1 ---

You and the Elf eventually reach a gondola lift station; he says the gondola lift will take you up to the water source, but this is as far as he can bring you. You go inside.

It doesn't take long to find the gondolas, but there seems to be a problem: they're not moving.

"Aaah!"

You turn around to see a slightly-greasy Elf with a wrench and a look of surprise. "Sorry, I wasn't expecting anyone! The gondola lift isn't working right now; it'll still be a while before I can fix it." You offer to help.

The engineer explains that an engine part seems to be missing from the engine, but nobody can figure out which one. If you can add up all the part numbers in the engine schematic, it should be easy to work out which part is missing.

The engine schematic (your puzzle input) consists of a visual representation of the engine. There are lots of numbers and symbols you don't really understand, but apparently any number adjacent to a symbol, even diagonally, is a "part number" and should be included in your sum. (Periods (.) do not count as a symbol.)

Here is an example engine schematic:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..

In this schematic, two numbers are not part numbers because they are not adjacent to a symbol: 114 (top right) and 58 (middle right). Every other number is adjacent to a symbol and so is a part number; their sum is 4361.

Of course, the actual engine schematic is much larger. What is the sum of all of the part numbers in the engine schematic?

"""

"""
# Assumptions

# Learnings
- we can get start and end indices using regex library (see `get_number_locations_from_string`)
- be careful of `elif`s when having multiple if statements return values.
- `match.end()` from regex library returns the index after the last index. So this needs to be
`match.end() - 1`

# Notes:
After I fixed some of my checks for surrounding symbols, I was confused why I still was not getting
the right answer. It kept saying I was too low. I decided to check for the "-" character in the 
puzzle input, and found out there is a few instances where there is the character "-" next to a number.
My guess is I am matching on negative numbers that should not be considered negative and therefore
adding negative numbers to my sum. However, doing some testing with regex, it appear "\d" only
returns digits, and ignores the "-" character.

After creating a test case for the 8 cases (top left, top, top right, left, right, bot left, bot, bot right),
I discovered that I had an `elif` statement for the top right check. If the code did check the top left,
it would ignore the `elif` and move on to the next if statement. In the future I need to be careful of this.

Finally, I realized that `match.end()` from regex library returns the index after the last index. So this needs to be
`match.end() - 1`.
"""

import re

IGNORE_CHARACTERS = [chr(num) for num in range(ord('0'), ord('9') + 1)] + ['.']


def get_number_locations_from_string(string: str) -> list[tuple[int, int, int]]:
    """
    Given a string, return a list of tuples corresponding to the number found,
    and the start and end index of each number.
    """
    indices = list()
    for match in re.finditer('\d+', string):
        start = match.start()
        end = match.end() - 1
        number = int(match.group())
        indices.append((number, start, end))
    return indices


def is_symbol(char: str) -> bool:
    return char not in IGNORE_CHARACTERS


def is_number_adjacent_to_part(lines: list[str], line_index: int, num_indexes: tuple[int, int]) -> bool:
    cur_line = lines[line_index]
    start_index = num_indexes[0]
    end_index = num_indexes[1]

    # left
    if start_index > 0:
        if is_symbol(cur_line[start_index - 1]):
            return True
    # right
    if end_index < len(cur_line) - 1:
        if is_symbol(cur_line[end_index + 1]):
            return True

    # above (including top left and right diagonals)
    if line_index > 0:
        prev_line = lines[line_index - 1]
        # top left
        if start_index > 0:
            if is_symbol(prev_line[start_index - 1]):
                return True
        # top right
        if end_index < len(prev_line) - 1:
            if is_symbol(prev_line[end_index + 1]):
                return True
        # top
        if any(is_symbol(char) for char in prev_line[start_index:end_index + 1]):
            return True

    # below (including bot left and right diagonals
    if line_index < len(lines) - 1:
        next_line = lines[line_index + 1]
        # bot left
        if start_index > 0:
            if is_symbol(next_line[start_index - 1]):
                return True
        # bot right
        if end_index < len(next_line) - 1:
            if is_symbol(next_line[end_index + 1]):
                return True
        # bot
        if any(is_symbol(char) for char in next_line[start_index:end_index + 1]):
            return True

    # default
    return False


def part1(filename: str) -> int:
    part_sum = 0
    with open(filename, 'r') as file_obj:
        lines = file_obj.readlines()

        for line_index in range(len(lines)):
            number_locations = get_number_locations_from_string(lines[line_index])
            for number_location in number_locations:
                number = number_location[0]
                start = number_location[1]
                end = number_location[2]
                if is_number_adjacent_to_part(lines, line_index, (start, end)):
                    part_sum += number

    return part_sum
    # first attempt: 463835 is too low
    # second attempt: fixed left and right test; 473719 is too low
    # third attempt: fixed below `line_index < len(cur_line)`;  473719
    # fixed elif: 476132 not the right answer
    # fixed match.end() off by one error: 511007 not the right answer

    # Correct answer: 509115


def test_is_number_adjacent_to_part():
    # top left
    lines = [
        "*....",
        ".123.",
        ".....",
    ]
    line_index = 1
    assert is_number_adjacent_to_part(lines, line_index, (1, 3)) is True
    # top
    lines = [
        "..*..",
        ".123.",
        ".....",
    ]
    line_index = 1
    assert is_number_adjacent_to_part(lines, line_index, (1, 3)) is True
    # top right
    lines = [
        "....*",
        ".123.",
        ".....",
    ]
    line_index = 1
    assert is_number_adjacent_to_part(lines, line_index, (1, 3)) is True
    # left
    lines = [
        ".....",
        "*123.",
        ".....",
    ]
    line_index = 1
    assert is_number_adjacent_to_part(lines, line_index, (1, 3)) is True
    # right
    lines = [
        ".....",
        ".123*",
        ".....",
    ]
    line_index = 1
    assert is_number_adjacent_to_part(lines, line_index, (1, 3)) is True
    # bot left
    lines = [
        ".....",
        ".123.",
        "*....",
    ]
    line_index = 1
    assert is_number_adjacent_to_part(lines, line_index, (1, 3)) is True
    # bot
    lines = [
        ".....",
        ".123.",
        ".*...",
    ]
    line_index = 1
    assert is_number_adjacent_to_part(lines, line_index, (1, 3)) is True
    # bot right
    lines = [
        ".....",
        ".123.",
        "....*",
    ]
    line_index = 1
    assert is_number_adjacent_to_part(lines, line_index, (1, 3)) is True

    # single digit
    lines = [
        ".....",
        "...1.",
        "....-",
    ]
    line_index = 1
    assert is_number_adjacent_to_part(lines, line_index, (3, 3)) is True

    # not ajacient single digit
    lines = [
        ".....",
        "..1..",
        "....*",
    ]
    line_index = 1
    assert is_number_adjacent_to_part(lines, line_index, (2, 2)) is False

    lines = [
        "....*",
        "..1..",
        ".....",
    ]
    line_index = 1
    assert is_number_adjacent_to_part(lines, line_index, (2, 2)) is False

    lines = [
        ".....",
        "..1..",
        "*....",
    ]
    line_index = 1
    assert is_number_adjacent_to_part(lines, line_index, (2, 2)) is False

    lines = [
        "*....",
        "..1..",
        ".....",
    ]
    line_index = 1
    assert is_number_adjacent_to_part(lines, line_index, (2, 2)) is False

    # Number on first line
    lines = [
        ".123.",
        "....*",
        ".....",
    ]
    line_index = 0
    assert is_number_adjacent_to_part(lines, line_index, (1, 3)) is True

    lines = [
        ".123.",
        "..*..",
        ".....",
    ]
    line_index = 0
    assert is_number_adjacent_to_part(lines, line_index, (1, 3)) is True

    lines = [
        ".123.",
        "*....",
        ".....",
    ]
    line_index = 0
    assert is_number_adjacent_to_part(lines, line_index, (1, 3)) is True

    lines = [
        "*123.",
        ".....",
        ".....",
    ]
    line_index = 0
    assert is_number_adjacent_to_part(lines, line_index, (1, 3)) is True

    lines = [
        ".123*",
        ".....",
        ".....",
    ]
    line_index = 0
    assert is_number_adjacent_to_part(lines, line_index, (1, 3)) is True

    # Number on last line
    lines = [
        ".....",
        "....*",
        ".123.",
    ]
    line_index = 2
    assert is_number_adjacent_to_part(lines, line_index, (1, 3)) is True

    lines = [
        ".....",
        "..*..",
        ".123.",
    ]
    line_index = 2
    assert is_number_adjacent_to_part(lines, line_index, (1, 3)) is True

    lines = [
        ".....",
        "*....",
        ".123.",
    ]
    line_index = 2
    assert is_number_adjacent_to_part(lines, line_index, (1, 3)) is True

    lines = [
        ".....",
        ".....",
        "*123.",
    ]
    line_index = 2
    assert is_number_adjacent_to_part(lines, line_index, (1, 3)) is True

    lines = [
        ".....",
        ".....",
        ".123*",
    ]
    line_index = 2
    assert is_number_adjacent_to_part(lines, line_index, (1, 3)) is True

    # Number on far left
    lines = [
        ".....",
        "...*.",
        "123..",
    ]
    line_index = 2
    assert is_number_adjacent_to_part(lines, line_index, (0, 2)) is True

    lines = [
        ".....",
        "..*..",
        "123..",
    ]
    line_index = 2
    assert is_number_adjacent_to_part(lines, line_index, (0, 2)) is True

    lines = [
        ".....",
        ".*...",
        "123..",
    ]
    line_index = 2
    assert is_number_adjacent_to_part(lines, line_index, (0, 2)) is True

    lines = [
        ".....",
        "*....",
        "123..",
    ]
    line_index = 2
    assert is_number_adjacent_to_part(lines, line_index, (0, 2)) is True

    lines = [
        ".....",
        ".....",
        "123*.",
    ]
    line_index = 2
    assert is_number_adjacent_to_part(lines, line_index, (0, 2)) is True


def test_get_number_locations_from_string():
    string = "467..114..."
    assert get_number_locations_from_string(string) == [(467, 0, 2), (114, 5, 7)]

    string = "-467..114.."
    assert get_number_locations_from_string(string) == [(467, 1, 3), (114, 6, 8)]

    string = "12345678901"
    assert get_number_locations_from_string(string) == [(12345678901, 0, 10)]

    string = ".....114..."
    assert get_number_locations_from_string(string) == [(114, 5, 7)]

    string = "..........."
    assert get_number_locations_from_string(string) == []

    string = "...*......"
    assert get_number_locations_from_string(string) == []

    string = "1.35..633."
    assert get_number_locations_from_string(string) == [(1, 0, 0), (35, 2, 3), (633, 6, 8)]


def test_is_symbol():
    # digit
    char = "1"
    assert is_symbol(char) is False

    # dot
    char = "."
    assert is_symbol(char) is False

    # symbols
    char = "-"
    assert is_symbol(char) is True
    char = "*"
    assert is_symbol(char) is True
    char = "&"
    assert is_symbol(char) is True


def part2():
    pass


test_is_number_adjacent_to_part()
test_get_number_locations_from_string()
test_is_symbol()
assert part1("inputs/test_input3.txt") == 4361
print(f"Part 1: {part1('inputs/input3.txt')}")
part2()
