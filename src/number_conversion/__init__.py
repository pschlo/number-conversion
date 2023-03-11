
# do not import prefix dicts and digitval functions
# also rename long function names
from .core import (
    Digits as Digits,
    DigitsGroup as DigitsGroup,
    ALNUM_ANY as ALNUM_ANY,
    ALNUM_LOWER as ALNUM_LOWER,
    ALNUM_UPPER as ALNUM_UPPER,

    numeral_to_number as from_numeral,      # type: ignore
    number_to_numeral as to_numeral,        # type: ignore
    convert_base as convert_base,
    convert_digits as convert_digits,
    remove_prefix as remove_prefix,

    PrefixMap as PrefixMap,
    DEFAULT_PREFIXES as DEFAULT_PREFIXES,
)
