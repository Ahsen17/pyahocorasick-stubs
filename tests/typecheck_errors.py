"""Expected failures; excluded from normal positive typecheck runs."""

from __future__ import annotations

from pathlib import Path

import ahocorasick as aho

words: aho.Automaton[str] = aho.Automaton()
words.add_word("x")  # STORE_ANY requires a value
words.add_word("x", 42)  # value must be str
words.get("x", default=None)  # positional-only
words.keys(prefix="x")  # positional-only
words.iter_long(string="x")  # positional-only
words.save(Path("x.bin"), lambda value: value.encode())  # path must be str
words.iter("x").set("x", reset=True)  # positional-only
words.kind = 1  # readonly
words.store = aho.STORE_INTS  # readonly
numbers = aho.Automaton(aho.STORE_INTS)
numbers.add_word("x", "bad")  # integer value required
numbers.save(
    "x.bin", lambda value: str(value).encode()
)  # integer save takes one argument
sequence = aho.Automaton(aho.STORE_INTS, aho.KEY_SEQUENCE)
sequence.add_word("x", 1)  # tuple key required
