from datetime import datetime
from datetime import timezone


def utcify_datetimes(values: dict[str, object]) -> dict[str, object]:
    result = {}
    for key, value in values.items():
        if isinstance(value, datetime) and value.tzinfo is None:
            result[key] = value.replace(tzinfo=timezone.utc)
        else:
            result[key] = value
    return result
