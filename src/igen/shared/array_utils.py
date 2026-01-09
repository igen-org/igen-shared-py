from __future__ import annotations

from collections.abc import Callable
from typing import TypeVar

T = TypeVar("T")
K = TypeVar("K")


def unique(items: list[T]) -> list[T]:
    return list(dict.fromkeys(items))


def is_empty(items: list[T] | None) -> bool:
    return items is not None and len(items) == 0


def without(items: list[T], value: T) -> list[T]:
    return [item for item in items if item != value]


def without_all(items: list[T], values: list[T]) -> list[T]:
    values_set = set(values)
    return [item for item in items if item not in values_set]


def compact(items: list[T | None]) -> list[T]:
    return [item for item in items if item is not None]


def intersection(a: list[T], b: list[T]) -> list[T]:
    b_set = set(b)
    return [item for item in a if item in b_set]


def difference(a: list[T], b: list[T]) -> list[T]:
    b_set = set(b)
    return [item for item in a if item not in b_set]


def chunk(items: list[T], size: int) -> list[list[T]]:
    if size <= 0:
        raise ValueError("chunk size must be greater than 0")
    return [items[i : i + size] for i in range(0, len(items), size)]


def group_by(items: list[T], key_fn: Callable[[T], K]) -> dict[K, list[T]]:
    grouped: dict[K, list[T]] = {}
    for item in items:
        key = key_fn(item)
        grouped.setdefault(key, []).append(item)
    return grouped


def partition(items: list[T], predicate: Callable[[T], bool]) -> tuple[list[T], list[T]]:
    truthy: list[T] = []
    falsy: list[T] = []
    for item in items:
        (truthy if predicate(item) else falsy).append(item)
    return truthy, falsy


def flatten(items: list[list[T]]) -> list[T]:
    return [item for sublist in items for item in sublist]


def count(items: list[T], predicate: Callable[[T], bool]) -> int:
    return sum(1 for item in items if predicate(item))


__all__ = [
    "chunk",
    "compact",
    "count",
    "difference",
    "flatten",
    "group_by",
    "intersection",
    "is_empty",
    "partition",
    "range_list",
    "unique",
    "without",
    "without_all",
    "zip_lists",
]
