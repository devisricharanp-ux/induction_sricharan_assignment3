def parse_coordinate_pair(x_text: str, y_text: str):
    """Returns (x, y) floats if both fields are valid, else None."""
    if not x_text or not y_text:
        return None
    try:
        return float(x_text), float(y_text)
    except ValueError:
        return None
