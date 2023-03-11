import string
from collections.abc import Sequence
from typing import overload


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


PREFIX_TO_BASE: dict[str, int] = dict()
PREFIXES: list[str] = []  # sorted by length in descending order

@overload
def add_prefix(prefix:str, base:int, /): ...

@overload
def add_prefix(dict: dict[str,int], /): ...

def add_prefix(*args:str|int|dict[str,int]):
    if isinstance(args[0], dict):
        _add_prefix_dict(args[0])
    else:
        assert isinstance(args[0], str) and isinstance(args[1], int)
        _add_prefix_single(args[0], args[1])
    PREFIXES.sort(key=len, reverse=True)

def _add_prefix_dict(dict: dict[str,int]):
    for prefix, base in dict.items():
        _add_prefix_single(prefix, base)

def _add_prefix_single(prefix:str, base:int):
    if prefix in PREFIX_TO_BASE:
        raise ValueError(f"Prefix '{prefix}' already exists")
    PREFIXES.append(prefix)
    PREFIX_TO_BASE[prefix] = base


add_prefix({
    '0b': 2,
    '0o': 8,
    '0x': 16,
})


class Digits:
    digits: set[str]
    digit_lengths: list[int]
    val2digit: tuple[str]
    digit2val: dict[str,int]

    # either list of digits or one big string
    def __init__(self, digits:str|list[str]) -> None:
        if not len(digits) > 0: raise ValueError("Cannot create empty digit list")

        self.digits = set(digits)
        self.val2digit = tuple(digits)
        self.digit2val = dict()

        digit_lengths: set[int] = set()
        for val, digit in enumerate(digits):
            self.digit2val[digit] = val
            digit_lengths.add(len(digit))
        self.digit_lengths = list(sorted(digit_lengths))

    def value(self, digit: str) -> int:
        return self.digit2val[digit]

    def digit(self, value: int) -> str:
        return self.val2digit[value]


# can be used when converting from numerals/digits to numbers/digitvalues
class DigitsGroup:
    digits: set[str]
    digit_lengths: list[int]
    digit2val: dict[str,int]

    def __init__(self, *digits:Digits) -> None:
        if not len(digits) > 0: raise ValueError("Cannot create empty digits group")

        self.digits = set()
        self.digit2val = dict()

        digit_lengths: set[int] = set()
        for d in digits:
            self.digits.update(d.digits)
            self.digit2val.update(d.digit2val)
            digit_lengths.update(d.digit_lengths)
        self.digit_lengths = list(sorted(digit_lengths))

    def value(self, digit: str) -> int:
        return self.digit2val[digit]


ALNUM_LOWER = Digits(string.digits + string.ascii_lowercase)
ALNUM_UPPER = Digits(string.digits + string.ascii_uppercase)
ALNUM_ANY = DigitsGroup(ALNUM_LOWER, ALNUM_UPPER)


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
        if digitval >= len(digits.val2digit): raise ValueError(f"Value '{digitval}' cannot be converted to a digit")
        _digits.append(digits.val2digit[digitval])
    return ''.join(_digits)



## numeral to number, i.e. str to int

# numeral must not have a base prefix
def numeral_to_digitvals(numeral:str, digits_group:Digits|DigitsGroup=ALNUM_ANY) -> tuple[int]:
    if not len(numeral) > 0: raise ValueError("Cannot convert empty numeral")

    digitvals: list[int] = []
    # this is done so that a digit could also be multiple chars wide
    while len(numeral) > 0:
        # find shortest digit prefix
        # only take possible prefixes and check if they are digits
        # runs not more than len(digits) times, because len(digits_lengths) <= len(digits)
        # runs not more that len(numeral) times, because every iteration i increases by at least one, and i>len(numeral) is checked
        # NOTE: could also use sentinel digit, but inserting into list is O(n)

        digit = ''
        is_found = False
        for i in digits_group.digit_lengths:
            if i > len(numeral): break
            digit = numeral[:i]
            if digit in digits_group.digits:
                is_found = True
                break
        if not is_found:
            raise ValueError(f"Cannot identify digit at beginning of subnumeral '{numeral}'. Are the digits prefix-free and is the numeral valid?")

        digitvals.append(digits_group.value(digit))
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
def remove_prefix(numeral:str) -> tuple[str, int]:
    # match longest prefix
    prefix = ''
    for prefix in PREFIXES:
        if numeral.startswith(prefix): break
    else:
        return numeral, 0
    
    # remove prefix
    base = PREFIX_TO_BASE[prefix]
    return numeral.removeprefix(prefix), base
