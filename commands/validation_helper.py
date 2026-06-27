

def validate_params_count(params, expected_count: int):
    if len(params) != expected_count:
        raise ValueError(
            f'Invalid number of arguments. Expected: {expected_count}; received: {len(params)}!')
        
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