## VProlog

An implementation of a subset of the Prolog programming language made for fun.
The language is parsed using [Lark](https://github.com/lark-parser/lark).

### Installation

```
pip install vprolog
```

### Usage

To run vprolog, use
```
vprolog [<input_file>]
```
where the argument is an optional input file containing facts and rules.

Example input files can be found in [examples](/examples).

### Example

To run the examples, just clone the repository first:
```
git clone https://github.com/Vekteur/vprolog.git
cd vprolog/examples/
```

```
$ vprolog example1.pl
?- cousin(bernard, X).
X = pierre
X = veronique
```

```
$ vprolog example5.pl
?- inverse([1, 2, 3], L).
L = [3, 2, 1]
```

```
$ vprolog example7.pl
?- gcd2(8, 12, X).
X = 4
```