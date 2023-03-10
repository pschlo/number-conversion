# number-conversion

*Note: When developing, type checking should be set to `strict`!*

## Installation
This package is not currently uploaded to PyPI. Install as follows:

1. Find your release of choice [here](https://github.com/pschlo/number-conversion/releases)
2. Copy the link to `number_conversion-x.x.x.tar.gz`
3. Run `python -m pip install {link}`

You may also prepend a [direct reference](https://peps.python.org/pep-0440/#direct-references), which might be desirable for a `requirements.txt`.


## Building
The `.tar.gz` file in a release is the
[source distribution](https://packaging.python.org/en/latest/glossary/#term-Source-Distribution-or-sdist), which was created from the source code with `python3 -m build --sdist`.
[Built distributions](https://packaging.python.org/en/latest/glossary/#term-Built-Distribution)
are not provided.


## Examples

### Example customization 1:

```python3
# define custom digits
# same as arabic digits except that the digit 4 is replaced by a bracket
# digits can be defined either as one big string, or as a list of digits
class BracketDigits:
    ROUND = Digits(['0', '1', '2', '3', '(', '5', '6', '7', '8', '9'])
    SQUARE = Digits('0123[56789ABCDEF')

# define digit group
class BracketGroups:
    ANY = DigitsGroup(BracketDigits.ROUND, BracketDigits.SQUARE)

# number to numeral conversion
print(number_to_numeral(42, 10, BracketDigits.ROUND))
print(number_to_numeral(42, 10, BracketDigits.SQUARE))
print(number_to_numeral(42, 10, BracketGroups.ANY))  # raises error

# numeral to number conversion
print(numeral_to_number("123(5", 10, BracketGroups.ANY))
print(numeral_to_number("123[5", 10, BracketGroups.ANY))
print(numeral_to_number("123[5", 10, BracketDigits.SQUARE))
print(numeral_to_number("123[5", 10, BracketDigits.ROUND))  # raises error
```

### Example customization 2:

```python3
# digits can also be multiple characters wide
# note that to unambiguously convert a numeral to a number, the digits must be prefix-free,
# i.e. no digit may be the prefix of another digit
weird_digits = Digits(['X0X', 'X1X1X1', 'X2X', 'Y3', 'aa4', '55'])

print(number_to_numeral(14, 10))
print(numeral_to_number("Y355", 10, weird_digits))
```
