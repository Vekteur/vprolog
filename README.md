## VProlog

A non-extensive implementation of the Prolog programming language made for fun.
The language is parsed using [Lark](https://github.com/lark-parser/lark).
Example input files can be found in [examples](/examples).

### Example

```
$ python src/vprolog.py examples/example1.pl
?- cousin(bernard, X).
X = pierre
X = veronique
```

```
$ python src/vprolog.py examples/example5.pl
?- inverse([1, 2, 3], L).
L = [3, 2, 1]
```

```
$ python src/vprolog.py examples/example7.pl
?- gcd2(8, 12, X).
X = 4
```