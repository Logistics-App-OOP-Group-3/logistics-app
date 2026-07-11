from enums.city import City
import re
import calendar
from datetime import datetime

def validate_params_count(params, expected_count: int, source: str):
    if len(params) != expected_count:
        raise ValueError(
            f'Invalid number of parameters passed to: {source}\n'
            f'  Expected: {expected_count}; received: {len(params)}!')
        

_CITY_LOOKUP = {
    **{m.name.lower(): m for m in City},
    **{m.value.lower(): m for m in City},
}

def try_parse_city(city_value_or_name: str):
    member = _CITY_LOOKUP.get(city_value_or_name.strip().lower())
    if member is None:
        raise ValueError(f"Can\'t parse {city_value_or_name} to City enum object.")
    return member
 
_ORDINAL_SUFFIX_RE = re.compile(r'(\d+)(st|nd|rd|th)', re.IGNORECASE)

_LEAP_YEAR_PLACEHOLDER = 2000  # any known leap year works here

def try_parse_date_time(value: str) -> datetime:
    """
    Parses a date/time string like 'Sep-12th-06:00h' (no year given).

    The current year is assumed. If it's currently December and the
    parsed month is January, the date is treated as rolling into next
    year (e.g. parsing "Jan 3rd 08:00h" while it's December) — this
    is the only case where a date that looks "earlier" is allowed.

    Raises ValueError if:
      - the string doesn't match the expected format
      - Feb 29th is given for a year that isn't a leap year
      - the resulting date/time is in the past, UNLESS it's the
        December -> January rollover
    """
    if not value or not value.strip():
        raise ValueError("Date/time value cannot be empty.")

    # remove the suffix of days(1st => 1, 12th => 12)
    cleaned = _ORDINAL_SUFFIX_RE.sub(r'\1', value.strip())

    try:
        parsed = datetime.strptime(f"{_LEAP_YEAR_PLACEHOLDER}-{cleaned}", "%Y-%b-%d-%H:%Mh")
    except ValueError:
        raise ValueError(
            f"Invalid date/time format: '{value}'. "
            f"Expected something like 'Sep-12th-06:00h'."
        )

    now = datetime.now()

    is_dec_to_jan_rollover = (now.month == 12 and parsed.month == 1)
    year = now.year + 1 if is_dec_to_jan_rollover else now.year

    if parsed.month == 2 and parsed.day == 29 and not calendar.isleap(year):
        raise ValueError(
            f"Invalid date: 'Feb 29th' does not exist in {year} (not a leap year)."
        )

    result = parsed.replace(year=year)

    if result < now and not is_dec_to_jan_rollover:
        raise ValueError(
            f"Invalid date/time: [{result}] is in the past (current time is [{now}])."
        )

    return result


def try_parse_float(float_string: str):
    try:
        return float(float_string)
    except:
        raise ValueError(f'Can\'t parse {float_string} to float!')
    
def try_parse_int(int_string: str):
    try:
        return int(int_string)
    except:
        raise ValueError(f'Can\'t parse {int_string} to int!')