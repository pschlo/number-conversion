from collections.abc import Sequence
from .prefix_map import *
from .digits import *


"""
DEFINITIONS

- a number is something abstract and cannot be written down directly
- instead, it can be written down using its representation in a specific numeral system
- this representation is also called a numeral
- a positional numeral system is a type of numeral system in which the contribution of a digit to the value
  of a number is the value of the digit multiplied by a factor determined by the position of the digit. (wikipedia)
- numerals in a positional system are thus made of digits
- examples of positional numeral systems:
    binary, with digits 0,1
    decimal, with digits 0,1,2,3,4,5,6,7,8,9
    hexadecimal, with digits 0,1,2,3,4,5,6,7,8,9,A,B,C,D,E,F
- example: in the binary system, the numeral 101 represents the number five
- example: in the decimal system, the numeral 17 represents the number seventeen
"""


## from number to numeral, i.e. int to str

# convert number to digit values in given base
# returns list of digits with value of most significant digit at index 0
def number_to_digitvals(number:int, base:int) -> tuple[int]:
    if not number >= 0: raise ValueError('Input number cannot be negative')
    if not base >= 2: raise ValueError("Base must be at least 2")

    digitvals:list[int] = []
    while True:
        number, digitval = divmod(number, base)
        digitvals.append(digitval)
        if number == 0: break
    return tuple(reversed(digitvals))


def digitvals_to_numeral(digitvals:Sequence[int], digits:Digits=ALNUM_LOWER) -> str:
    if not len(digitvals) > 0: raise ValueError("Cannot convert empty digit value sequence")

    _digits:list[str] = []
    for digitval in digitvals:
        if digitval > digits.max_value: raise ValueError(f"Value '{digitval}' cannot be converted to a digit")
        _digits.append(digits.digit_of(digitval))
    return ''.join(_digits)



## numeral to number, i.e. str to int

# numeral must not have a base prefix
def numeral_to_digitvals(numeral:str, digits_group:Digits|DigitsGroup=ALNUM_ANY) -> tuple[int]:
    if not len(numeral) > 0: raise ValueError("Cannot convert empty numeral")

    digitvals: list[int] = []
    # this is done so that a digit could also be multiple chars wide
    while len(numeral) > 0:
        digit = digits_group.find_prefix(numeral)
        if digit is None:
            raise ValueError(f"Cannot identify digit at beginning of subnumeral '{numeral}'. Are the digits prefix-free and is the numeral valid?")
        digitvals.append(digits_group.value_of(digit))
        numeral = numeral.removeprefix(digit)

    return tuple(digitvals)


def digitvals_to_number(digitvals:Sequence[int], base:int) -> int:
    number = 0
    weight = 1
    for digitval in reversed(digitvals):
        if not digitval < base: raise ValueError(f"Digit value '{digitval}' is too large for base {base}")
        number += weight * digitval
        weight *= base
    return number



## shortcut functions
# numeral must not have a base prefix
def numeral_to_number(numeral:str, base:int, digits_group:Digits|DigitsGroup=ALNUM_ANY) -> int:
    digitvals = numeral_to_digitvals(numeral, digits_group)
    return digitvals_to_number(digitvals, base)

def number_to_numeral(number:int, base:int, digits:Digits=ALNUM_LOWER) -> str:
    digitvals = number_to_digitvals(number, base)
    return digitvals_to_numeral(digitvals, digits)

def convert_base(numeral:str, from_base:int, to_base:int, from_digits:Digits|DigitsGroup=ALNUM_ANY, to_digits:Digits=ALNUM_LOWER) -> str:
    number = numeral_to_number(numeral, from_base, from_digits)
    return number_to_numeral(number, to_base, to_digits)

def convert_digits(numeral:str, from_digits:Digits|DigitsGroup=ALNUM_ANY, to_digits:Digits=ALNUM_LOWER) -> str:
    digitvals = numeral_to_digitvals(numeral, from_digits)
    return digitvals_to_numeral(digitvals, to_digits)


# tries to detect number system base by looking for prefix
# if unsuccessful, base is 0
# returns base and numeral without prefix
def remove_prefix(numeral:str, prefixes:PrefixMap=DEFAULT_PREFIXES) -> tuple[str, int]:
    prefix = prefixes.find_prefix(numeral, reverse=True)
    if prefix is None:
        return numeral, 0
    base = prefixes.get_base(prefix)
    return numeral.removeprefix(prefix), base
