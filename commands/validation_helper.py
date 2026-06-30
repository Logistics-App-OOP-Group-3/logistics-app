from enums.city import City

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