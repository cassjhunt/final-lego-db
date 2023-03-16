def safe_int(input_value: str, default_value: int) -> int:
    try:
        return int(input_value)
    except:
        return default_value


def within_valid_values(input_value: str, valid_values: set[str], default_value: str) -> str:
    if input_value in valid_values:
        return input_value
    else:
        return default_value


def with_default(input_value: str, default_value: str) -> str:
    if input_value:
        return input_value
    else:
        return default_value
