"""Public API stubs for pyahocorasick 2.3.1 (Unicode C-extension build).

Automaton[Value, Key=str, Store=Literal[30]] is static-only generic notation.
Construct with Automaton(), not Automaton[Value]().
"""

from collections.abc import Callable
from typing import (
    Any,
    Final,
    Generic,
    Literal,
    Protocol,
    Self,
    TypedDict,
    final,
    overload,
)

from typing_extensions import TypeVar

_Value = TypeVar("_Value", default=Any)
_Key = TypeVar("_Key", bound=str | tuple[int, ...], default=str)
_Store = TypeVar("_Store", bound=int, default=Literal[30])
_Default = TypeVar("_Default")
_Result_co = TypeVar("_Result_co", covariant=True)
_Value_co = TypeVar("_Value_co", covariant=True)
_Input_contra = TypeVar("_Input_contra", contravariant=True)

EMPTY: Final = 0
TRIE: Final = 1
AHOCORASICK: Final = 2
STORE_INTS: Final = 10
STORE_LENGTH: Final = 20
STORE_ANY: Final = 30
KEY_STRING: Final = 100
KEY_SEQUENCE: Final = 200
MATCH_EXACT_LENGTH: Final = 0
MATCH_AT_MOST_PREFIX: Final = 1
MATCH_AT_LEAST_PREFIX: Final = 2
unicode: Final = 1

class _Stats(TypedDict):
    nodes_count: int
    words_count: int
    longest_word: int
    links_count: int
    sizeof_node: int
    total_size: int

class _ItemsIterator(Protocol[_Result_co]):
    def __iter__(self) -> Self: ...
    def __next__(self) -> _Result_co: ...

class _SearchIterator(Protocol[_Value_co, _Input_contra]):
    """Structural type of the non-exported search iterator classes."""

    def __iter__(self) -> Self: ...
    def __next__(self) -> tuple[int, _Value_co]: ...
    def set(self, string: _Input_contra, reset: bool = False, /) -> None:  # noqa: PYI048
        """Replace input; reset=False continues the existing search state."""
        ...

@final
class Automaton(Generic[_Value, _Key, _Store]):
    """Trie and Aho-Corasick automaton; add patterns before make_automaton().

    Constructor arguments are positional. Runtime ignores keyword options.
    STORE_ANY requires a value, STORE_INTS permits an omitted integer value,
    and STORE_LENGTH computes the value from key length (ignores supplied value).
    """

    @overload
    def __new__(
        cls: type[Automaton[Any, Any, Any]],
        value_type: Literal[30] = 30,
        key_type: Literal[100] = 100,
        /,
    ) -> Automaton[Any, str, Literal[30]]: ...
    @overload
    def __new__(
        cls: type[Automaton[Any, Any, Any]],
        value_type: Literal[10],
        key_type: Literal[100] = 100,
        /,
    ) -> Automaton[int, str, Literal[10]]: ...
    @overload
    def __new__(
        cls: type[Automaton[Any, Any, Any]],
        value_type: Literal[20],
        key_type: Literal[100] = 100,
        /,
    ) -> Automaton[int, str, Literal[20]]: ...
    @overload
    def __new__(
        cls: type[Automaton[Any, Any, Any]],
        value_type: Literal[30],
        key_type: Literal[200],
        /,
    ) -> Automaton[Any, tuple[int, ...], Literal[30]]: ...
    @overload
    def __new__(
        cls: type[Automaton[Any, Any, Any]],
        value_type: Literal[10],
        key_type: Literal[200],
        /,
    ) -> Automaton[int, tuple[int, ...], Literal[10]]: ...
    @overload
    def __new__(
        cls: type[Automaton[Any, Any, Any]],
        value_type: Literal[20],
        key_type: Literal[200],
        /,
    ) -> Automaton[int, tuple[int, ...], Literal[20]]: ...
    @overload
    def __new__(
        cls: type[Automaton[Any, Any, Any]],
        data: list[bytes],
        kind: Literal[0, 1, 2],
        store: Literal[10, 20, 30],
        key_type: Literal[100, 200],
        word_count: int,
        longest_word: int,
        values: list[Any] | None,
        /,
    ) -> Automaton[Any, Any, Any]:
        """Low-level constructor used by the pickle reconstruction protocol."""

    @property
    def kind(self) -> Literal[0, 1, 2]:
        """Read-only state: EMPTY, TRIE or AHOCORASICK."""

    @property
    def store(self) -> _Store:
        """Read-only associated-value storage mode."""

    @overload
    def add_word(
        self: Automaton[_Value, _Key, Literal[30]],
        key: _Key,
        value: _Value,
        /,
    ) -> bool:
        """Insert/replace a pattern. Return whether a new key was added."""

    @overload
    def add_word(
        self: Automaton[int, _Key, Literal[10]],
        key: _Key,
        value: int = ...,
        /,
    ) -> bool: ...
    @overload
    def add_word(
        self: Automaton[int, _Key, Literal[20]],
        key: _Key,
        value: object = ...,
        /,
    ) -> bool: ...
    def remove_word(self, word: _Key, /) -> bool:
        """Remove a pattern; return False when absent."""

    def pop(self, word: _Key, /) -> _Value:
        """Remove and return a value; raise KeyError when absent."""

    def clear(self) -> None:
        """Remove all keys and invalidate active iterators."""

    def exists(self, key: _Key, /) -> bool:
        """Check an exact stored key (not a text substring search)."""

    def match(self, key: _Key, /) -> bool:
        """Check whether key is a path/prefix in the trie."""

    def longest_prefix(self, string: _Key, /) -> int:
        """Return length of the longest input prefix present in the trie."""

    @overload
    def get(self, key: _Key, /) -> _Value:
        """Return associated value; missing key raises KeyError."""

    @overload
    def get(self, key: _Key, default: _Default, /) -> _Value | _Default: ...
    def keys(
        self,
        prefix: str = ...,
        wildcard: str = ...,
        how: Literal[0, 1, 2] = ...,
        /,
    ) -> _ItemsIterator[str]:
        """Iterate keys as Unicode strings, including for KEY_SEQUENCE.

        A prefix alone selects descendants. Wildcard must have length one;
        with wildcard and no explicit how, matching uses EXACT_LENGTH.
        """

    def values(
        self,
        prefix: str = ...,
        wildcard: str = ...,
        how: Literal[0, 1, 2] = ...,
        /,
    ) -> _ItemsIterator[_Value]:
        """Iterate values using the same filter arguments as keys()."""

    def items(
        self,
        prefix: str = ...,
        wildcard: str = ...,
        how: Literal[0, 1, 2] = ...,
        /,
    ) -> _ItemsIterator[tuple[str, _Value]]:
        """Iterate (Unicode key, value) pairs using keys() filtering."""

    def make_automaton(self) -> None:
        """Finalize failure links before searching; empty trie stays EMPTY."""

    def iter(
        self,
        string: _Key,
        start: int = 0,
        end: int = ...,
        ignore_white_space: bool = False,
    ) -> _SearchIterator[_Value, _Key]:
        """Yield all (inclusive_end_index, value) matches, including overlaps.

        Only this search method accepts named parameters. A search iterator
        supports set() for chunked input. Whitespace skipping applies to
        the runtime search procedure and does not normalize stored keys.
        """

    def iter_long(
        self,
        string: _Key,
        start: int = 0,
        end: int = ...,
        /,
    ) -> _SearchIterator[_Value, _Key]:
        """Yield longest non-overlapping matches; iterator also supports set()."""

    def find_all(
        self,
        string: _Key,
        callback: Callable[[int, _Value], object],
        start: int = 0,
        end: int = ...,
        /,
    ) -> None:
        """Call callback(end_index, value) for each match; ignore its result."""

    @overload
    def save(
        self: Automaton[_Value, _Key, Literal[30]],
        path: str,
        serializer: Callable[[_Value], bytes],
        /,
    ) -> None:
        """Save to a string path; STORE_ANY requires a bytes serializer."""

    @overload
    def save(
        self: Automaton[int, _Key, Literal[10]],
        path: str,
        /,
    ) -> None: ...
    @overload
    def save(
        self: Automaton[int, _Key, Literal[20]],
        path: str,
        /,
    ) -> None: ...
    def get_stats(self) -> _Stats:
        """Return the six integer trie statistics."""

    def dump(
        self,
    ) -> (
        tuple[
            list[tuple[int, int]],
            list[tuple[int, bytes, int]],
            list[tuple[int, int]],
        ]
        | None
    ):
        """Return nodes, edges (bytes labels), failure links; None if empty."""

    def __contains__(self, key: _Key, /) -> bool: ...
    def __iter__(self) -> _ItemsIterator[str]: ...
    def __len__(self) -> int: ...
    def __sizeof__(self) -> int: ...
    def __reduce__(
        self,
    ) -> tuple[Callable[..., Automaton[Any, Any, Any]], tuple[Any, ...]]:
        """Return pickle reconstruction callable and positional arguments."""

def load(
    path: str,
    deserializer: Callable[[bytes], Any],
    /,
) -> Automaton[Any, Any, Any]:
    """Load saved state. Key/store types are determined by the file, not callback.

    Use an explicit cast if the persisted format is known by the caller.
    The deserializer is required even for integer storage modes.
    """
