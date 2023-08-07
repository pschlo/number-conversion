import string
from abc import ABC, abstractmethod


class AbstractKV(ABC):
    _keys: frozenset[str]
    _key_lengths: tuple[int]  # sorted in ascending order
    _key_to_value: dict[str,int]

    @abstractmethod
    def __init__(self, keys:frozenset[str], key_lengths: tuple[int], key_to_value:dict[str,int]) -> None:
        self._keys = keys
        self._key_lengths = key_lengths
        self._key_to_value = key_to_value

    # finds either the longest or shortest matching prefix from _keys in given string
    # runs not more than len(_keys) times, because len(_key_lengths) <= len(_keys)
    # returns prefix or None
    # NOTE: could also use sentinel digit, but inserting into list is O(n)
    def find_prefix(self, string:str, reverse:bool=False) -> str|None:
        prefix = ''
        for i in self._key_lengths if not reverse else reversed(self._key_lengths):
            prefix = string[:i]
            if prefix in self._keys:
                break
        else:
            return None
        return prefix
    


class MyAbstractDigits(AbstractKV):
    @property
    def digits(self):
        return self._keys
    @property
    def digit2val(self):
        return self._key_to_value.items()
    @property
    def digit_lengths(self):
        return self._key_lengths
    
    def value_of(self, digit:str):
        return self._key_to_value[digit]



class Digits(MyAbstractDigits):
    _val2digit: tuple[str]

    def __init__(self, digits:str|list[str]) -> None:
        if not len(digits) > 0: raise ValueError("Cannot create empty digit list")

        _digits = frozenset(digits)
        self._val2digit = tuple(digits)
        _digit2val: dict[str,int] = dict()
        _digit_lengths: set[int] = set()

        for val, digit in enumerate(digits):
            _digit2val[digit] = val
            _digit_lengths.add(len(digit))

        super().__init__(_digits, tuple(sorted(_digit_lengths)), _digit2val)

    def digit_of(self, value: int) -> str:
        return self._val2digit[value]

    @property
    def max_value(self) -> int:
        return self.max_base-1
    
    @property
    def max_base(self) -> int:
        return len(self._val2digit)


class DigitsGroup(MyAbstractDigits):
    def __init__(self, *digits:Digits) -> None:
        if not len(digits) > 0: raise ValueError("Cannot create empty digits group")

        _digit2val: dict[str,int] = dict()
        _digits: set[str] = set()
        _digit_lengths: set[int] = set()

        for d in digits:
            _digits.update(d.digits)
            _digit2val.update(d.digit2val)
            _digit_lengths.update(d.digit_lengths)

        super().__init__(frozenset(_digits), tuple(sorted(_digit_lengths)), _digit2val)






# class AbstractDigits(ABC):
#     _digits: frozenset[str]
#     _digit_lengths: tuple[int]  # sorted in ascending order
#     _digit2val: dict[str,int]

#     @abstractmethod
#     def __init__(self) -> None:
#         pass

#     def value_of(self, digit: str) -> int:
#         return self._digit2val[digit]

#     @property
#     def digit2val(self):
#         return self._digit2val.items()
#     @property
#     def digits(self):
#         return self._digits
#     @property
#     def digit_lengths(self):
#         return self._digit_lengths


# class Digits(AbstractDigits):
#     _val2digit: tuple[str]

#     # either list of digits or one big string
#     def __init__(self, digits:str|list[str]) -> None:
#         if not len(digits) > 0: raise ValueError("Cannot create empty digit list")

#         self._digits = frozenset(digits)
#         self._val2digit = tuple(digits)
#         self._digit2val = dict()
#         digit_lengths: set[int] = set()

#         for val, digit in enumerate(digits):
#             self._digit2val[digit] = val
#             digit_lengths.add(len(digit))

#         self._digit_lengths = tuple(sorted(digit_lengths))

#     def digit_of(self, value: int) -> str:
#         return self._val2digit[value]

#     @property
#     def max_value(self) -> int:
#         return self.max_base-1
    
#     @property
#     def max_base(self) -> int:
#         return len(self._val2digit)


# # can be used when converting from numerals/digits to numbers/digitvalues
# class DigitsGroup(AbstractDigits):
#     def __init__(self, *digits:Digits) -> None:
#         if not len(digits) > 0: raise ValueError("Cannot create empty digits group")

#         self._digit2val = dict()
#         digits_list: set[str] = set()
#         digit_lengths: set[int] = set()

#         for d in digits:
#             digits_list.update(d.digits)
#             self._digit2val.update(d.digit2val)
#             digit_lengths.update(d.digit_lengths)

#         self._digit_lengths = tuple(sorted(digit_lengths))
#         self._digits = frozenset(digits_list)


ALNUM_LOWER = Digits(string.digits + string.ascii_lowercase)
ALNUM_UPPER = Digits(string.digits + string.ascii_uppercase)
ALNUM_ANY = DigitsGroup(ALNUM_LOWER, ALNUM_UPPER)
