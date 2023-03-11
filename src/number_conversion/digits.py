import string


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
