from number_conversion import *
import string


alnum_lower = Digits(string.digits + string.ascii_lowercase)
alnum_upper = Digits(string.digits + string.ascii_uppercase)

# numeral = NumberConverter.number_to_numeral(-1, alnum_lower, 16)

number = numeral_to_number('Aa', {alnum_upper, alnum_lower}, 16)

print(number)