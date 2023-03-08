# import string
# from enum import Enum, EnumMeta
from collections.abc import Sequence


__all__ = [
    'BASE_TO_PREFIX',
    'PREFIX_TO_BASE',
    'Digits',
    'number_to_numeral',
    'numeral_to_number'
]


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


# class DigitsMeta(EnumMeta):
#     pass

# class DigitGroupsMeta(EnumMeta):
#     pass

# class Digits(Enum, metaclass=DigitsMeta):
#     pass

# class DigitGroups(Enum, metaclass=DigitGroupsMeta):
#     pass


class Digits:
    val2digit: tuple[str]
    digit2val: dict[str,int]

    def __init__(self, digits:str|list[str]) -> None:
        self.val2digit = tuple(digits)
        self.digit2val = {digit: val for val, digit in enumerate(digits)}





# class AlnumDigits(Digits):
#     LOWER = string.digits + string.ascii_lowercase
#     UPPER = string.digits + string.ascii_uppercase

# class AlnumGroups(DigitGroups):
#     ANY = [AlnumDigits.LOWER, AlnumDigits.UPPER]






# # digits can be either list of digits or one big string
# # digitgroups can be used when converting from numerals/digits to numbers/digitvalues
# # if check is True, it is verified that
# #   a) every digit list is prefix-free
# #   b) for each group, the contained digit lists do not contradict each other
# def __init__(self, *digits:DigitsMeta|DigitGroupsMeta, check:bool=True,
#              default_to_numeral:Digits|None=None, default_from_numeral:Digits|DigitGroups|None=None) -> None:

#     self.digit2val = dict()
#     self.val2digit = dict()

#     if (isinstance(default_to_numeral, str)):
#         pass


#     # parse arguments
#     digit_enums:set[DigitsMeta] = set()
#     group_enums:set[DigitGroupsMeta] = set()
#     for d in digits:
#         if isinstance(d, DigitsMeta):
#             digit_enums.add(d)
#         else:
#             group_enums.add(d)
    

#     # convert enum to dict
#     digitdict:dict[Digits, str|list[str]]
#     # always contains AlnumDigits
#     digitdict = {member: member.value for member in AlnumDigits}
#     digitdict |= {member: member.value for digit_enum in digit_enums for member in digit_enum}  # type: ignore

#     # get digit-to-digitvalue and digitvalue-to-digit mappings
#     for digitsname, digitlist in digitdict.items():
#         # ensure digitlist type
#         # if not isinstance(digitlist, Sequence):
#         #     raise ValueError("Digit list must be a Sequence, e.g. str or int")
#         val2digit:list[str] = list(digitlist)
#         # # check that every digit appears at most once
#         # if check and not len(val2digit) == len(set(val2digit)):
#         #     raise ValueError(f"Digits '{digitsname}' are ambiguous")
#         # check that digits are prefix-free, i.e. that no digit is the prefix of another digit
#         if check and any(i != j and di.startswith(dj) for i, di in enumerate(val2digit) for j, dj in enumerate(val2digit)):
#             raise ValueError(f"Digits '{digitsname}' are ambiguous")
#         self.val2digit[digitsname] = val2digit
#         # reverse digit mapping
#         self.digit2val[digitsname] = {digit: val for val, digit in enumerate(val2digit)}
    

#     groupdict:dict[DigitGroups, list[Digits]]
#     # always contains AlnumGroups
#     groupdict = {member: member.value for member in AlnumGroups}
#     groupdict |= {member: member.value for group_enum in group_enums for member in group_enum}  # type: ignore

#     # resolve groups
#     # optionally check that no group members contradict each other
#     for groupname, digitsnames in groupdict.items():
#         groupmap: dict[str,int] = dict()
#         for digitsname in digitsnames:
#             if digitsname not in self.digit2val:
#                 raise ValueError(f"Could not find digits '{digitsname}'")
#             digit2val = self.digit2val[digitsname]
#             # check that every key that is already in groupmap maps to the same in new map
#             if check and not all(groupmap[i] == digit2val[i] for i in digit2val if i in groupmap):
#                 raise ValueError(f"Digits '{digitsname}' contradict with another digit list from group '{groupname}'")
#             groupmap |= digit2val
#         self.digit2val[groupname] = groupmap


#     # set default digit-to-digitvalue map
#     if default_from_numeral is None:
#         if len(digit_enums) + len(group_enums) == 0:
#             # use default alnum digits
#             self.default_digit2val = AlnumGroups.ANY
#         else:
#             self.default_digit2val = None
#     elif default_from_numeral in self.digit2val:
#         self.default_digit2val = default_from_numeral
#     else:
#         raise ValueError(f"Default digit list '{default_from_numeral}' for numeral-to-number conversion is invalid")

#     # set default digitvalue-to-digit map
#     if default_to_numeral is None:
#         if len(digit_enums) + len(group_enums) == 0:
#             # use default alnum digits
#             self.default_val2digit = AlnumDigits.LOWER
#         else:
#             self.default_val2digit = None
#     elif default_to_numeral in self.val2digit:
#         self.default_val2digit = default_to_numeral
#     else:
#         raise ValueError(f"Default digit list '{default_to_numeral}' for number-to-numeral conversion is invalid")



## from number to numeral, i.e. int to str

# convert number to digit values in given base
# returns list of digits with value of most significant digit at index 0
# assume base 10 if none given
def number_to_digitvals(number:int, base:int=10) -> tuple[int]:
    if not number >= 0: raise ValueError('Input number cannot be negative')
    if not base >= 2: raise ValueError("Base must be at least 2")

    digitvals:list[int] = []
    while True:
        number, digitval = divmod(number, base)
        digitvals.append(digitval)
        if number == 0: break
    return tuple(reversed(digitvals))



# takes 'digits' to reference preset digit lists
def digitvals_to_numeral(digitvals:Sequence[int], digits:Digits) -> str:
    if not len(digitvals) > 0: raise ValueError("Cannot convert empty digit value sequence")

    _digits:list[str] = []
    for digitval in digitvals:
        if digitval >= len(digits.val2digit): raise ValueError(f"Value '{digitval}' cannot be converted to a digit")
        _digits.append(digits.val2digit[digitval])
    return ''.join(_digits)



## numeral to number, i.e. str to int

# numeral may not have a base prefix
def numeral_to_digitvals(numeral:str, digits:set[Digits]) -> tuple[int]:
    if not len(numeral) > 0: raise ValueError("Cannot convert empty numeral")

    # combine digit mappings
    digit2val:dict[str,int] = dict()
    for digitlist in digits:
        digit2val |= digitlist.digit2val

    digitvals: list[int] = []
    # this is done so that a digit could also be multiple chars wide
    # this loop could be optimized by avoiding new string creation at every loop iteration
    while len(numeral) > 0:
        # get all digits that are prefix of numeral
        prefix_digits = [digit for digit in digit2val if numeral.startswith(digit)]
        if len(prefix_digits) == 0:
            raise ValueError(f"Cannot identify digit at beginning of subnumeral '{numeral}'")
        elif len(prefix_digits) > 1:
            raise ValueError(f"Digit at beginning of subnumeral '{numeral}' is ambiguous")
        digit = prefix_digits[0]
        digitvals.append(digit2val[digit])
        numeral = numeral.removeprefix(digit)

    return tuple(digitvals)



# assume base 10 if none given
def digitvals_to_number(digitvals:Sequence[int], base:int=10) -> int:
    number = 0
    weight = 1
    for digitval in reversed(digitvals):
        if not digitval < base: raise ValueError(f"Digit value '{digitval}' is too large for base {base}")
        number += weight * digitval
        weight *= base
    return number



## shortcut functions
# assume base 10 if none given
# numeral may not have a base prefix
def numeral_to_number( numeral:str, digits:set[Digits], base:int=10) -> int:
    digitvals = numeral_to_digitvals(numeral, digits)
    return digitvals_to_number(digitvals, base)

# assume base 10 if none given
def number_to_numeral(number:int, digits:Digits, base:int=10) -> str:
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




# TODO: make functions that check if base/input is OK

