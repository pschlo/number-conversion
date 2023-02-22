# number-conversion

*Note: When developing, type checking should be set to `strict`!*

## Installation

The
[GitHub API](https://docs.github.com/en/rest/repos/contents?apiVersion=2022-11-28#download-a-repository-archive-tar)
allows to fetch a repository as a `tar` archive. The
[source archive](https://packaging.python.org/en/latest/glossary/#term-Source-Archive) 
can thereby be downloaded from
```
https://api.github.com/repos/pschlo/number-conversion/tarball/{REF}
```
where `REF` is a branch, commit or tag name (e.g. `v0.0.3` or `main`).

A
[source distribution](https://packaging.python.org/en/latest/glossary/#term-Source-Distribution-or-sdist)
or
[built distribution](https://packaging.python.org/en/latest/glossary/#term-Built-Distribution)
can then be created manually, e.g. with [`build`](https://pypa-build.readthedocs.io) from PyPA. `pip`, however, can automatically build from source archives. It is also good style to prepend a [direct reference](https://peps.python.org/pep-0440/#direct-references). For example, the install command for the latest patch of version 1.0 is:
```
$ python -m pip install number-conversion@https://api.github.com/repos/pschlo/number-conversion/tarball/v1.0.x
```

## Examples

### Example customization 1:

```python3
# define custom digits
# same as arabic digits except that the digit 4 is replaced by a bracket
# digits can be defined either as one big string, or as a list of digits
class BracketDigits(BaseDigits):
    ROUND = ['0', '1', '2', '3', '(', '5', '6', '7', '8', '9']
    SQUARE = '0123[56789ABCDEF'

# define digit group
class BracketGroups(BaseGroups):
    ANY = [BracketDigits.ROUND, BracketDigits.SQUARE]

# create NumberConverter
conv = NumberConverter(BracketDigits, BracketGroups)

# number to numeral conversion
print(conv.number_to_numeral(42, 10, BracketDigits.ROUND))
print(conv.number_to_numeral(42, 10, BracketDigits.SQUARE))
print(conv.number_to_numeral(42, 10, BracketGroups.ANY))  # raises error

# numeral to number conversion
print(conv.numeral_to_number("123(5", 10, BracketGroups.ANY))
print(conv.numeral_to_number("123[5", 10, BracketGroups.ANY))
print(conv.numeral_to_number("123[5", 10, BracketDigits.SQUARE))
print(conv.numeral_to_number("123[5", 10, BracketDigits.ROUND))  # raises error
```

### Example customization 2:

```python3
# digits can also be multiple characters wide
# note that to unambiguously convert a numeral to a number, the digits must be prefix-free,
# i.e. no digit may be the prefix of another digit

class WeirdDigits(BaseDigits):
    DIGITS = ['X0X', 'X1X1X1', 'X2X', 'Y3', 'aa4', '55']

conv = NumberConverter(WeirdDigits, default_to_numeral=WeirdDigits.DIGITS)

print(conv.number_to_numeral(14, 10))
print(conv.numeral_to_number("Y355", 10, WeirdDigits.DIGITS))
```
