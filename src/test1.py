from number_conversion import *

MY_PREFIXES = PrefixMap({
    '0B': 2,
    '0BB': 2,
    'jo': 2
})



numeral, base = remove_prefix('0ZB123', MY_PREFIXES)
print(numeral, base)

# digits can also be multiple characters wide
# note that to unambiguously convert a numeral to a number, the digits must be prefix-free,
# i.e. no digit may be the prefix of another digit
weird_digits = Digits(['X0X', 'X1X1X1', 'X2X', 'Y3', 'aa4', '55', '5'])

print(to_numeral(14, 10, weird_digits))
print(from_numeral("Y355", 10, weird_digits))


print(remove_prefix('jo11', MY_PREFIXES))
