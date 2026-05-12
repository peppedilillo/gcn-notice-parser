"""Shared JSON parser error handling."""

import json

from pydantic import ValidationError

from gcnparser.exceptions import ParseError


def parse_json_notice(value: bytes, model: type, parser_name: str):
    try:
        data = json.loads(value)
    except json.JSONDecodeError as exc:
        raise ParseError(f"{parser_name}: failed to parse document: {exc}") from exc

    try:
        return model(**data)
    except ValidationError as exc:
        raise ParseError(f"{parser_name}: model validation failed: {exc}") from exc
