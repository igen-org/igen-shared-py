from __future__ import annotations

from calendar import monthrange
from datetime import date, datetime, time, timedelta, timezone
from typing import Literal

DateUnit = Literal[
    "millisecond",
    "second",
    "minute",
    "hour",
    "day",
    "week",
    "month",
    "year",
]


def _normalize_datetime(value: datetime | date, use_utc: bool) -> datetime:
    if isinstance(value, date) and not isinstance(value, datetime):
        value = datetime.combine(value, time.min)
    if use_utc and value.tzinfo is not None:
        return value.astimezone(timezone.utc)
    return value


def _parse_date_string(value: str, use_utc: bool) -> datetime:
    trimmed = value.strip()
    if not trimmed:
        raise ValueError("date string must not be empty")

    if trimmed.endswith("Z"):
        trimmed = trimmed[:-1] + "+00:00"

    if use_utc and "T" in trimmed and "+" not in trimmed and "-" not in trimmed[10:]:
        trimmed = f"{trimmed}+00:00"

    parsed = datetime.fromisoformat(trimmed) if "T" in trimmed else date.fromisoformat(trimmed)
    if isinstance(parsed, date) and not isinstance(parsed, datetime):
        parsed = datetime.combine(parsed, time.min)

    if use_utc and parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    elif use_utc and parsed.tzinfo is not None:
        parsed = parsed.astimezone(timezone.utc)

    return parsed


def now() -> datetime:
    return datetime.now()


def parse_date(value: str | int | float | date | datetime, *, utc: bool = False) -> datetime:
    if isinstance(value, datetime):
        return _normalize_datetime(value, utc)
    if isinstance(value, date):
        return _normalize_datetime(value, utc)
    if isinstance(value, (int, float)):
        seconds = value / 1000 if value > 1_000_000_000_000 else value
        tz = timezone.utc if utc else None
        return datetime.fromtimestamp(seconds, tz=tz)
    return _parse_date_string(value, utc)


def _shift_month(value: datetime, months: int) -> datetime:
    total_months = value.year * 12 + (value.month - 1) + months
    new_year, new_month_index = divmod(total_months, 12)
    new_month = new_month_index + 1
    max_day = monthrange(new_year, new_month)[1]
    new_day = min(value.day, max_day)
    return value.replace(year=new_year, month=new_month, day=new_day)


def modify_date(amount: int, unit: DateUnit, base: datetime | date | None = None) -> datetime:
    current = parse_date(base or now())
    return _shift_date(current, amount, unit)


def _shift_date(value: datetime, amount: int, unit: DateUnit) -> datetime:
    if unit == "millisecond":
        return value + timedelta(milliseconds=amount)
    if unit == "second":
        return value + timedelta(seconds=amount)
    if unit == "minute":
        return value + timedelta(minutes=amount)
    if unit == "hour":
        return value + timedelta(hours=amount)
    if unit == "day":
        return value + timedelta(days=amount)
    if unit == "week":
        return value + timedelta(weeks=amount)
    if unit == "month":
        return _shift_month(value, amount)
    if unit == "year":
        return _shift_month(value, amount * 12)
    raise ValueError("Unsupported DateUnit")


def _diff_in_months(start: datetime, end: datetime) -> float:
    if start == end:
        return 0.0

    sign = 1 if end > start else -1
    months = (end.year - start.year) * 12 + (end.month - start.month)
    anchor = _shift_date(start, months, "month")

    if (sign > 0 and end < anchor) or (sign < 0 and end > anchor):
        months -= sign

    adjusted_anchor = _shift_date(start, months, "month")
    next_anchor = _shift_date(adjusted_anchor, sign, "month")
    interval = (next_anchor - adjusted_anchor).total_seconds()

    if interval == 0:
        return float(months)

    return months + ((end - adjusted_anchor).total_seconds() / interval) * sign


def date_diff(start: datetime | date, end: datetime | date, unit: DateUnit) -> float:
    start_dt = _normalize_datetime(start, False)
    end_dt = _normalize_datetime(end, False)
    diff = end_dt - start_dt
    if unit == "millisecond":
        return diff.total_seconds() * 1000
    if unit == "second":
        return diff.total_seconds()
    if unit == "minute":
        return diff.total_seconds() / 60
    if unit == "hour":
        return diff.total_seconds() / 3600
    if unit == "day":
        return diff.total_seconds() / 86400
    if unit == "week":
        return diff.total_seconds() / (86400 * 7)
    if unit == "month":
        return _diff_in_months(start_dt, end_dt)
    if unit == "year":
        return _diff_in_months(start_dt, end_dt) / 12
    raise ValueError("Unsupported DateUnit")


def start_of(value: datetime | date, unit: DateUnit, *, utc: bool = False, week_starts_on: int = 0) -> datetime:
    current = _normalize_datetime(value, utc)
    if unit == "millisecond":
        return current
    if unit == "second":
        return current.replace(microsecond=0)
    if unit == "minute":
        return current.replace(second=0, microsecond=0)
    if unit == "hour":
        return current.replace(minute=0, second=0, microsecond=0)
    if unit == "day":
        return current.replace(hour=0, minute=0, second=0, microsecond=0)
    if unit == "week":
        start_day = start_of(current, "day", utc=utc, week_starts_on=week_starts_on)
        day_index = (start_day.weekday() + 1) % 7
        offset = (day_index - week_starts_on + 7) % 7
        return start_day - timedelta(days=offset)
    if unit == "month":
        return current.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    if unit == "year":
        return current.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    raise ValueError("Unsupported DateUnit")


def end_of(value: datetime | date, unit: DateUnit, *, utc: bool = False, week_starts_on: int = 0) -> datetime:
    if unit == "millisecond":
        return _normalize_datetime(value, utc)
    next_start = _shift_date(start_of(value, unit, utc=utc, week_starts_on=week_starts_on), 1, unit)
    return next_start - timedelta(microseconds=1)


def is_same(a: datetime | date, b: datetime | date, unit: DateUnit, *, utc: bool = False, week_starts_on: int = 0) -> bool:
    return start_of(a, unit, utc=utc, week_starts_on=week_starts_on) == start_of(
        b, unit, utc=utc, week_starts_on=week_starts_on
    )


__all__ = [
    "DateUnit",
    "date_diff",
    "end_of",
    "is_same",
    "modify_date",
    "now",
    "parse_date",
    "start_of",
]
