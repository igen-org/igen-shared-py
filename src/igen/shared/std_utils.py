from __future__ import annotations

import inspect
import math
import re
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, Generic, TypeVar

T = TypeVar("T")
E = TypeVar("E")


def is_defined(value: T | None) -> bool:
    return value is not None


def assert_defined(value: T | None, message: str | None = None) -> T:
    if value is None:
        raise ValueError(message or "Value is undefined or null")
    return value


def identity(value: T) -> T:
    return value


def noop() -> None:
    return None


def not_fn(fn: Callable[..., bool]) -> Callable[..., bool]:
    def wrapper(*args: Any, **kwargs: Any) -> bool:
        return not fn(*args, **kwargs)

    return wrapper


def is_string(value: object) -> bool:
    return isinstance(value, str)


def is_number(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def is_boolean(value: object) -> bool:
    return isinstance(value, bool)


def is_function(value: object) -> bool:
    return callable(value)


def is_date(value: object) -> bool:
    return isinstance(value, (date, datetime))


def is_regexp(value: object) -> bool:
    return isinstance(value, re.Pattern)


def is_promise(value: object) -> bool:
    return isinstance(value, Awaitable) or inspect.isawaitable(value)


def is_object(value: object) -> bool:
    return isinstance(value, dict)


def is_array(value: object) -> bool:
    return isinstance(value, (list, tuple))


def is_safe_number(value: object) -> bool:
    return is_number(value) and math.isfinite(value)


def is_empty_object(value: object) -> bool:
    return isinstance(value, dict) and len(value) == 0


def is_plain_object(value: object) -> bool:
    return isinstance(value, dict) and type(value) is dict


@dataclass(frozen=True)
class Ok(Generic[T]):
    ok: bool
    value: T


@dataclass(frozen=True)
class Err(Generic[E]):
    ok: bool
    error: E


def ok(value: T) -> Ok[T]:
    return Ok(ok=True, value=value)


def err(error: E) -> Err[E]:
    return Err(ok=False, error=error)


def from_try(fn: Callable[[], T]) -> Ok[T] | Err[Exception]:
    try:
        return ok(fn())
    except Exception as exc:
        return err(exc)


__all__ = [
    "Err",
    "Ok",
    "assert_defined",
    "err",
    "from_try",
    "identity",
    "is_array",
    "is_boolean",
    "is_date",
    "is_defined",
    "is_empty_object",
    "is_function",
    "is_number",
    "is_object",
    "is_plain_object",
    "is_promise",
    "is_regexp",
    "is_safe_number",
    "is_string",
    "noop",
    "not_fn",
    "ok",
]
