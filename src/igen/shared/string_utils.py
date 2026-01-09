from __future__ import annotations

import re

_WORD_PATTERN = re.compile(r"[A-Z]+(?![a-z])|[A-Z]?[a-z]+|\d+")


def capitalize(s: str) -> str:
    """Capitalize only the first character of the string."""
    if not s:
        return s
    return s[0].upper() + s[1:]


def _split_words(value: str) -> list[str]:
    trimmed = value.strip()
    if not trimmed:
        return []
    return _WORD_PATTERN.findall(trimmed)


def snake_case(value: str) -> str:
    return "_".join(word.lower() for word in _split_words(value))


def kebab_case(value: str) -> str:
    return "-".join(word.lower() for word in _split_words(value))


def camel_case(value: str) -> str:
    words = _split_words(value)
    if not words:
        return ""
    return words[0].lower() + "".join(capitalize(word.lower()) for word in words[1:])


def truncate(value: str, max_length: int, suffix: str = "...") -> str:
    if max_length < 0:
        raise ValueError("max_length must be non-negative")
    if len(value) <= max_length:
        return value
    available = max(0, max_length - len(suffix))
    return value[:available] + suffix


def strip_prefix(value: str, prefix: str) -> str:
    return value.removeprefix(prefix)


def strip_suffix(value: str, suffix: str) -> str:
    return value.removesuffix(suffix)


def count_occurrences(value: str, search: str) -> int:
    if search == "":
        raise ValueError("search value must not be empty")
    count = 0
    start_index = 0
    while True:
        index = value.find(search, start_index)
        if index == -1:
            break
        count += 1
        start_index = index + len(search)
    return count


def trim(s: str | None) -> str:
    return s.strip() if s is not None else ""


def is_blank(s: str | None) -> bool:
    return s is None or s.strip() == ""


def is_not_blank(s: str | None) -> bool:
    return s is not None and s.strip() != ""


__all__ = [
    "camel_case",
    "capitalize",
    "count_occurrences",
    "is_blank",
    "is_not_blank",
    "kebab_case",
    "snake_case",
    "strip_prefix",
    "strip_suffix",
    "trim",
    "truncate",
]
