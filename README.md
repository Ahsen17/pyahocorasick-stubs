**English** | [简体中文](README_cn.md)

# pyahocorasick-stubs

Independent [PEP 561](https://peps.python.org/pep-0561/) stub-only package for the
Unicode build of [pyahocorasick](https://github.com/WojciechMula/pyahocorasick).
It gives type checkers (mypy, pyright) a precise picture of the `ahocorasick` C
extension — the `Automaton` class, its storage and key modes, and the module-level
`load()`. Types only, no runtime code. Requires Python 3.12+.

## Installation

The package is distributed directly from GitHub (not yet published to PyPI):

```bash
pip install git+https://github.com/Ahsen17/pyahocorasick-stubs.git
```

or with [uv](https://docs.astral.sh/uv/):

```bash
uv add git+https://github.com/Ahsen17/pyahocorasick-stubs.git
```

Installing the package pulls in a compatible `pyahocorasick` automatically (it is
declared as a dependency). Both mypy and pyright pick the stubs up without any
configuration.

## Quick start

```python
from ahocorasick import Automaton

# The subscription is static-only notation: annotate with Automaton[str],
# but always construct a plain Automaton().
words: Automaton[str] = Automaton()  # default store: STORE_ANY (values required)
words.add_word("he", "he")
words.add_word("her", "her")
words.add_word("here", "here")
words.make_automaton()

for end_index, value in words.iter("here"):
    print(end_index, value)  # 1 he / 2 her / 3 here
```

Storage and key modes are selected through positional constructor arguments:

```python
from ahocorasick import KEY_SEQUENCE, STORE_INTS, STORE_LENGTH, Automaton

integers = Automaton(STORE_INTS)  # Automaton[int, str, Literal[10]]
integers.add_word("x", 42)

lengths = Automaton(STORE_LENGTH)  # value derived from the key length
lengths.add_word("abc")  # get("abc") == 3

sequence = Automaton(STORE_ANY, KEY_SEQUENCE)  # tuple[int, ...] keys
sequence.add_word((1, 2), "one-two")
```

Behaviors worth knowing, all enforced statically by the stubs:

- `add_word()` requires a value under `STORE_ANY`, permits an omitted integer under
  `STORE_INTS`, and ignores supplied values under `STORE_LENGTH`.
- `iter()` is the only method that accepts keyword arguments; search iterators expose
  `set()` for chunked input.
- Constructor keyword arguments do not configure the runtime mode — the C extension
  is positional-only there.

## Version policy

Stub versions mirror the upstream release they target plus a stub revision: `2.3.1.0`
tracks `pyahocorasick` 2.3.1, and the trailing component bumps when the stubs change
without a new upstream release. The declared runtime dependency is pinned to
compatible upstream versions (`pyahocorasick>=2.3.1,<2.4`); upgrade the stub package
and `pyahocorasick` together.

## Validation

These stubs are validated against the real pyahocorasick C extension: runtime
integration tests exercise the complete public API, and mypy and pyright both run in
strict mode against the type-level test suite.

## License

[MIT](LICENSE)
