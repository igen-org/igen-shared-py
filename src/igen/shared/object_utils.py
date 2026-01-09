from __future__ import annotations

from typing import Iterable, TypeVar

T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")


def clone(source: dict[K, V], props: dict[K, V] | None = None) -> dict[K, V]:
    updated = dict(source)
    if props:
        updated.update(props)
    return updated


def is_shallow_equal(a: dict[object, object], b: dict[object, object]) -> bool:
    if a.keys() != b.keys():
        return False
    return all(a[key] == b[key] for key in a)


def pick(source: dict[K, V], keys: Iterable[K]) -> dict[K, V]:
    return {key: source[key] for key in keys if key in source}


def omit(source: dict[K, V], keys: Iterable[K]) -> dict[K, V]:
    omit_set = set(keys)
    return {key: value for key, value in source.items() if key not in omit_set}


def entries_to_object(entries: Iterable[tuple[K, V]]) -> dict[K, V]:
    return {key: value for key, value in entries}


__all__ = [
    "clone",
    "entries_to_object",
    "is_shallow_equal",
    "omit",
    "pick",
]
