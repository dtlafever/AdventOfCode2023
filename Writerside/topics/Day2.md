# Day 2

## Part 1

This problem seemed focused on string splitting and parsing. I orginally thought
of building regex for getting each game number, sets, and individual colors for each set, but
after playing around with regex for about 45 minutes and not quite getting what I wanted,
I realized that a more traditional programming approach was probably best for my
sanity.

### Assumptions
- each line has at least one color
- each line has exactly 1 game number

### Attempts

#### Attempt 1

I decided to break this problem up into a few different functions to solve it:
- `get_line_data` to get the game number and the individual color counts
- `is_valid_game` to validate each game given the output of `get_line_data`.

I would loop through each line in the input file and extract the game number, and 
extract each color-number pair while ignoring the different sets. Since this problem
is only focused on if a value pulled out of the bag is greater than the given
color value (12 for red, 13 for green, 14 for blue), differentiating the sets doesn't
matter. As long as the color-number pair is less than our given color values, add the
game number to our running total and return the result.

### Solution

```python
import re

def get_line_data(line: str):
    # assuming format: Game \d+: (\d+ (red|blue|green))+.*;
    line = line.strip()  # remove new line characters
    game_str, line = line.split(":")
    game_num = game_str.split(" ")[1]
    color_counts = re.split(';|,', line)
    color_counts = [color_count.strip() for color_count in color_counts]
    return game_num, color_counts

def is_valid_game(num_red: int, num_green: int, num_blue: int, color_counts: list[str]) -> bool:
    for color_count in color_counts:
        count, color = color_count.split(" ")
        count = int(count)
        if color == "red":
            if count > num_red:
                return False
        elif color == "green":
            if count > num_green:
                return False
        elif color == "blue":
            if count > num_blue:
                return False
    return True


def part1():
    RED_CUBES   = 12
    GREEN_CUBES = 13
    BLUE_CUBES  = 14

    game_sum = 0

    with open("inputs/input2.txt") as file_obj:
        for line in file_obj:
            game_num, game_sets = get_line_data(line)
            if is_valid_game(RED_CUBES, GREEN_CUBES, BLUE_CUBES, game_sets):
                game_sum += int(game_num)
        print(f"Game Sum: {game_sum}")
```

## Part 2

This second part seems fairly easy. I will reuse the same `get_line_data` function
and create a new function called `get_maximum_for_each_color` that will calculate
the max for each color for a given game. Then I take each of those maxes and multiply
them together and add the result to my total sum.

### Assumptions
No additional assumptions.

### Solution

```python
import re

def get_line_data(line: str) -> tuple[int, list[str]]:
    line = line.strip()  # remove new line characters
    game_str, line = line.split(":")
    game_num = game_str.split(" ")[1]
    color_counts = re.split(';|,', line)
    color_counts = [color_count.strip() for color_count in color_counts]
    return int(game_num), color_counts

def get_maximum_for_each_color(color_counts: list[str]) -> tuple[int, int, int]:
    red_max   = 0
    green_max = 0
    blue_max  = 0

    for color_count in color_counts:
        count, color = color_count.split(" ")
        count = int(count)
        if color == "red":
            if count > red_max:
                red_max = count
        if color == "green":
            if count > green_max:
                green_max = count
        if color == "blue":
            if count > blue_max:
                blue_max = count

    return red_max, green_max, blue_max
def part2():
    power_sum = 0

    with open("inputs/input2.txt") as file_obj:
        for line in file_obj:
            game_num, game_sets = get_line_data(line)
            red_max, green_max, blue_max = get_maximum_for_each_color(game_sets)
            power_sum += red_max * green_max * blue_max
        print(f"Power Sum: {power_sum}")
```

## Learnings
- there is `split` function in the `re` library that allows you to split on multiple characters at once.