

def validate_params_count(params, expected_count: int):
    if len(params) != expected_count:
        raise ValueError(
            f'Invalid number of arguments. Expected: {expected_count}; received: {len(params)}.")')