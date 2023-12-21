`# Day1

## Part 1

Part 1 of this problem, at first glance, seems pretty simple. 
The solution will involve searching each line until you find the two numbers,
then concat them together and convert to an integer. Keep a running sum of each number
and you have your answer.

### Assumptions
- the input is all lower case alpha numeric characters only.

### Attempts

#### Attempt 1
I was trying to be lazy, so I thought I could use `strip` to simplify my life by passing 
in all the lower alphabet characters to be stripped, incorrectly assuming `strip` 
stripped all characters from the whole string:

```python
lower_alpha_list = [chr(i) for i in range(ord('a'), ord('z') + 1)]
lower_alphabet = "".join(lower_alpha_list)

test_value = "1abc2"
print(test_value.strip(lower_alphabet))
# Output: 1abc2
```

This was incorrect since `strip` _only strips leading and trailing characters, not the whole string_.
Looks like we are doing it the old fashion way.

#### Attempt 2
Let's loop through each line in the input, where we additionally loop through each character
in for each line. Accumulate each time we see a numeric character and stop once we reach two.
Once we have found our two numbers, combine them as a string and convert into an integer to
and add that integer to our total sum. We then break out of the character loop to save a few
cycles and move on to the next line.

```python
calibration_sum = 0
MIN_INTEGER_ASCII = ord("0")
MAX_INTEGER_ASCII = ord("9")

with open("inputs/intput1.txt", 'r') as file_obj:
    for line in file_obj:
        calibration_numbers = []
        for character in line:
            ascii_char_value = ord(character)
            if MIN_INTEGER_ASCII <= ascii_char_value <= MAX_INTEGER_ASCII:
                calibration_numbers.append(character)
                if len(calibration_numbers) == 2:
                    # we found our two numbers, add to sum
                    calibration_number = int("".join(calibration_numbers))
                    calibration_sum += calibration_number
                    break

print(f"Calibration Number Sum: {calibration_sum}")
```

This was incorrect as well because I missed a key part in the instructions:
It specifically said to find the **first** and **last** digit. And the example gave
a line `treb7uchet` that only had one digit and was considered to be the number `77`.

Second, I did not handle the case where there is more than 2 numbers since I only grab
the first two numbers I find.

Let's fix these issues for our final solution.

### Solution

```python
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

print(f"Calibration Number Sum: {calibration_sum}")
```

## Part 2

Part two seems a bit more of a pain. We now need to match with written out version of 1-9.
Additionally, we need to account for overlapping characters. For example:

`twone` should give you the number `21` where `two` and `one` share the letter `o`.

All of this sounds like a pain to do in code, so this is where I turn to regex.

### Assumptions
- There is no `zero`

### Solution

```python
import re

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
```

## Learnings
- `strip(chars)` removes all **leading** and **trailing** whitespaces, or `chars` if you provide it that. 
I miss remembered it and used it to strip all characters from a string.
- You can shorten
```
if ascii_char_value >= MIN_INTEGER_ASCII and ascii_char_value <= MAX_INTEGER_ASCII:
```
TO
```
if MIN_INTEGER_ASCII <= ascii_char_value <= MAX_INTEGER_ASCII:
```
- Read the instructions carefully! Just because it is the first problem, 
doesn't mean there won't be a curve ball.
- In Regex, if you want to capture overlapping capture groups, you can use `(?=...)`.`