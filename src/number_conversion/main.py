import string
from collections.abc import Sequence



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

BASE_TO_PREFIX: dict[int, str] = {
    2: '0b',
    8: '0o',
    16: '0x'
}

PREFIX_TO_BASE: dict[str, int] = {
    '0b': 2,
    '0o': 8,
    '0x': 16
}


class Digits:
    digits: set[str]
    val2digit: tuple[str]
    digit2val: dict[str,int]

    # either list of digits or one big string
    def __init__(self, digits:str|list[str]) -> None:
        self.digits = set(digits)
        self.val2digit = tuple(digits)
        self.digit2val = {digit: val for val, digit in enumerate(digits)}

    def value(self, digit: str) -> int:
        return self.digit2val[digit]

    def digit(self, value: int) -> str:
        return self.val2digit[value]


# can be used when converting from numerals/digits to numbers/digitvalues
class DigitsGroup:
    digits: set[str]
    digit2val: dict[str,int]

    def __init__(self, *digits:Digits) -> None:
        self.digits = set()
        self.digit2val = dict()
        for d in digits:
            self.digits.update(d.digits)
            self.digit2val.update(d.digit2val)

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



# takes 'digits' to reference preset digit lists
def digitvals_to_numeral(digitvals:Sequence[int], digits:Digits=ALNUM_LOWER) -> str:
    if not len(digitvals) > 0: raise ValueError("Cannot convert empty digit value sequence")

    _digits:list[str] = []
    for digitval in digitvals:
        if digitval >= len(digits.val2digit): raise ValueError(f"Value '{digitval}' cannot be converted to a digit")
        _digits.append(digits.val2digit[digitval])
    return ''.join(_digits)



## numeral to number, i.e. str to int

# numeral may not have a base prefix
def numeral_to_digitvals(numeral:str, digits_group:Digits|DigitsGroup=ALNUM_ANY) -> tuple[int]:
    if not len(numeral) > 0: raise ValueError("Cannot convert empty numeral")

    digitvals: list[int] = []
    # this is done so that a digit could also be multiple chars wide
    # this loop could be optimized by avoiding new string creation at every loop iteration
    while len(numeral) > 0:
        # get all digits that are prefix of numeral
        prefix_digits = [digit for digit in digits_group.digits if numeral.startswith(digit)]
        if len(prefix_digits) == 0:
            raise ValueError(f"Cannot identify digit at beginning of subnumeral '{numeral}'")
        elif len(prefix_digits) > 1:
            raise ValueError(f"Digit at beginning of subnumeral '{numeral}' is ambiguous")
        digit = prefix_digits[0]
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
# numeral may not have a base prefix
def numeral_to_number( numeral:str, base:int, digits_group:Digits|DigitsGroup=ALNUM_ANY) -> int:
    digitvals = numeral_to_digitvals(numeral, digits_group)
    return digitvals_to_number(digitvals, base)

def number_to_numeral(number:int, base:int, digits:Digits=ALNUM_LOWER) -> str:
    digitvals = number_to_digitvals(number, base)
    return digitvals_to_numeral(digitvals, digits)



# tries to detect number system base by looking for prefix
# returns base if unambiguously detected, else 0
def detect_base(numeral:str) -> int:
    matching_bases = [base for prefix, base in PREFIX_TO_BASE.items() if numeral.startswith(prefix)]
    if not len(matching_bases) == 1: return 0
    return matching_bases[0]

# removes prefix if there is any
def remove_prefix(numeral:str, base:int=0) -> str:
    if not base:
        base = detect_base(numeral)
    if base in BASE_TO_PREFIX:
        return numeral.removeprefix(BASE_TO_PREFIX[base])
    else:
        # unknown base
        return numeral
