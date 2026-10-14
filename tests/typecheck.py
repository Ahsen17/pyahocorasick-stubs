"""Static checks against the installed stub-only wheel."""

from __future__ import annotations

from typing import Any, Literal, assert_type, cast

import ahocorasick as aho

words: aho.Automaton[str] = aho.Automaton()
assert_type(words.add_word("cheat", "cheat"), bool)
assert_type(words.get("cheat"), str)
assert_type(words.get("missing", None), str | None)
assert_type(words.get("missing", 1), str | int)
assert_type(words.store, Literal[30])
words.make_automaton()
for end, value in words.iter(string="selling cheats", start=0, ignore_white_space=True):
    assert_type(end, int)
    assert_type(value, str)
words.iter("").set("cheat", True)
words.iter_long("").set("cheat", True)
assert_type(next(words.keys()), str)
assert_type(next(iter(words)), str)
assert_type(next(words.values()), str)
assert_type(next(words.items()), tuple[str, str])
assert_type(words.get_stats()["nodes_count"], int)
words.find_all("cheat", lambda end, value: len(value) + end)
words.save("words.bin", lambda value: value.encode())

numbers = aho.Automaton(aho.STORE_INTS)
assert_type(numbers.get("x"), int)
assert_type(numbers.store, Literal[10])
numbers.add_word("x")
numbers.add_word("y", 2)
numbers.save("numbers.bin")

lengths = aho.Automaton(aho.STORE_LENGTH)
assert_type(lengths.get("x"), int)
lengths.add_word("x")
lengths.save("lengths.bin")

sequence = aho.Automaton(aho.STORE_INTS, aho.KEY_SEQUENCE)
sequence.add_word((1, 2))
sequence.make_automaton()
assert_type(next(sequence.iter((0, 1, 2))), tuple[int, int])
assert_type(next(sequence.keys()), str)

metadata: aho.Automaton[tuple[int, str]] = aho.Automaton()
metadata.add_word("x", (1, "x"))
assert_type(metadata.get("x"), tuple[int, str])


def decode(data: bytes) -> str:
    return data.decode()


assert_type(aho.load("words.bin", decode), aho.Automaton[Any, Any, Any])
restored = cast("aho.Automaton[str]", aho.load("words.bin", decode))
assert_type(restored.get("cheat"), str)
