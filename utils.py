def is_float(input_value):
    try:
        float(input_value)
        return True
    except ValueError:
        return False
    except TypeError:
        return False


def is_int(input_value):
    try:
        int(input_value)
        return int(input_value) == float(input_value)
    except ValueError:
        return False
    except TypeError:
        return False


def is_number(input_value):
    return is_float(input_value) or is_int(input_value)
