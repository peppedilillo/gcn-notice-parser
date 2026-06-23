from datetime import datetime
from datetime import timezone
from typing import Any


def utcify_datetimes(values: dict[str, object]) -> dict[str, object]:
    result = {}
    for key, value in values.items():
        if isinstance(value, datetime) and value.tzinfo is None:
            result[key] = value.replace(tzinfo=timezone.utc)
        else:
            result[key] = value
    return result


def assert_datetime_fields_timezone_aware(model: Any) -> None:
    found = False
    for field_name in type(model).model_fields:
        value = getattr(model, field_name)
        if isinstance(value, datetime):
            found = True
            assert value.tzinfo is not None, f"{field_name} is naive"
            assert value.utcoffset() is not None, f"{field_name} is naive"

    assert found, "model has no datetime fields"
