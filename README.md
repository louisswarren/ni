# Ni!

## Installation
```sh
cp ni.py ~/bin/ni
```

## Usage
```sh
ni [EXPR1] [EXPR2] ...
```
Take lines from stdin as an iterator, and execute ni-expressions EXPR1, EXPR2 etc on this iterator.
If the final result is a string, it is printed. Otherwise, the resulted is iterated over and printed line by line

### Line mode
```
ni -l [EXPR1] [EXPR2] ...
```
In line mode, the ni-expressions are applied to each line instead of to the iterator containing all lines.
