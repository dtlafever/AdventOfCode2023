"""
--- Part 1 ---

Something is wrong with global snow production, and you've been selected to take a look. The Elves have even given
you a map; on it, they've used stars to mark the top fifty locations that are likely to be having problems.

You've been doing this long enough to know that to restore snow operations, you need to check all fifty stars by
December 25th.

Collect stars by solving puzzles. Two puzzles will be made available on each day in the Advent calendar; the second
puzzle is unlocked when you complete the first. Each puzzle grants one star. Good luck!

You try to ask why they can't just use a weather machine ("not powerful enough") and where they're even sending you (
"the sky") and why your map looks mostly blank ("you sure ask a lot of questions") and hang on did you just say the
sky ("of course, where do you think snow comes from") when you realize that the Elves are already loading you into a
trebuchet ("please hold still, we need to strap you in").

As they're making the final adjustments, they discover that their calibration document (your puzzle input) has been
amended by a very young Elf who was apparently just excited to show off her art skills. Consequently, the Elves are
having trouble reading the values on the document.

The newly-improved calibration document consists of lines of text; each line originally contained a specific
calibration value that the Elves now need to recover. On each line, the calibration value can be found by combining
the first digit and the last digit (in that order) to form a single two-digit number.

For example:

1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet

In this example, the calibration values of these four lines are 12, 38, 15, and 77. Adding these together produces 142.

Consider your entire calibration document. What is the sum of all of the calibration values?

--- Part 2 ---

Your calculation isn't quite right. It looks like some of the digits are actually spelled out with letters: one, two, three, four, five, six, seven, eight, and nine also count as valid "digits".

Equipped with this new information, you now need to find the real first and last digit on each line. For example:

two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen

In this example, the calibration values are 29, 83, 13, 24, 42, 14, and 76. Adding these together produces 281.

What is the sum of all of the calibration values?

"""
import re

def part1():
    calibration_sum = 0
    MIN_INTEGER_ASCII = ord("0")
    MAX_INTEGER_ASCII = ord("9")

    with open("inputs/input1.txt", 'r') as file_obj:
        for line in file_obj:
            calibration_numbers = []
            for character in line:
                ascii_char_value = ord(character)
                if MIN_INTEGER_ASCII <= ascii_char_value <= MAX_INTEGER_ASCII:
                    if len(calibration_numbers) < 2:
                        # we haven't found more than two numbers, just append
                        calibration_numbers.append(character)
                    else:
                        # we found more than two numbers, overwrite the last one
                        calibration_numbers[1] = character
            if len(calibration_numbers) == 1:
                # Special case: we only found 1 number.
                calibration_number = int(f"{calibration_numbers[0]}{calibration_numbers[0]}")
                calibration_sum += calibration_number
            elif len(calibration_numbers) == 2:
                calibration_number = int("".join(calibration_numbers))
                calibration_sum += calibration_number
            else:
                # didn't find any numbers, do nothing
                pass

        print(f"Part One Calibration Number Sum: {calibration_sum}")

def part2():
    number_lookup = {
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
    }

    calibration_sum = 0

    # `(?=...)` matches if `...` matches next, but doesn't consume any of the string.
    # This is called a lookahead.
    reg_pattern = re.compile(r"(?=([0-9]|one|two|three|four|five|six|seven|eight|nine))", re.I)

    with open("inputs/input1.txt", 'r') as file_obj:
        for line in file_obj:
            reg_pattern_instances = reg_pattern.findall(line)
            if len(reg_pattern_instances) == 0:
                # no numbers found
                continue

            first_number = reg_pattern_instances[0]
            second_number = reg_pattern_instances[-1]
            if first_number in number_lookup.keys():
                first_number = number_lookup[first_number]
            if second_number in number_lookup.keys():
                second_number = number_lookup[second_number]

            calibration_number = int("".join([first_number, second_number]))
            calibration_sum += calibration_number

        print(f"Part Two Calibration Number Sum: {calibration_sum}")


part1()
part2()