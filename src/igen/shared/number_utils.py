from __future__ import annotations


def clamp(value: float, min_value: float, max_value: float) -> float:
    return min(max(value, min_value), max_value)


def round_to(value: float, precision: int = 0) -> float:
    factor = 10**precision
    return round(value * factor) / factor


def mean(values: list[float]) -> float:
    if not values:
        raise ValueError("Cannot compute mean of an empty list")
    return sum(values) / len(values)


def to_percentage(value: float, digits: int = 2) -> str:
    return f"{value * 100:.{digits}f}%"


__all__ = [
    "clamp",
    "mean",
    "round_to",
    "to_percentage",
]
