from number_conversion import *


# digits can also be multiple characters wide
# note that to unambiguously convert a numeral to a number, the digits must be prefix-free,
# i.e. no digit may be the prefix of another digit
weird_digits = Digits(['X0X', 'X1X1X1', 'X2X', 'Y3', 'aa4', '55'])

print(to_numeral(14, 10, weird_digits))
print(from_numeral("Y355", 10, weird_digits))

print()
print(from_numeral('1asdfjhdfjkashfdsjfajsfsjfhajsdkfhj', 36))

print()
print(convert_numeral('100000', 2, 2, to_digits=weird_digits))
print(convert_numeral('X1X1X1X0XX0XX0XX0XX0X', 2, 10, from_digits=weird_digits))
