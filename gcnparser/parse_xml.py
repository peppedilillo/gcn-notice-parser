"""Shared XML extraction helpers and error handling.

This module contains the small helpers used by mission-specific parsers
 plus the common ``parse_notice`` assembly routine.
"""

from collections.abc import Callable
from datetime import datetime
from datetime import timezone
from xml.etree import ElementTree as ET

from pydantic import ValidationError

from gcnparser.exceptions import FieldParseError
from gcnparser.exceptions import ParseError

Rule = Callable[[ET.Element], object]
SectionRules = dict[str, Rule]
Sections = dict[str, SectionRules]


def parse_utc_datetime(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def parse_voevent_root(value: bytes, parser_name: str) -> ET.Element:
    try:
        return ET.fromstring(value)
    except ET.ParseError as exc:
        raise ParseError(f"{parser_name}: failed to parse document: {exc}") from exc


def parse_voevent_notice(value: bytes, model: type, parser_name: str, sections: Sections):
    root = parse_voevent_root(value, parser_name)

    data = {}
    for section_name, rules in sections.items():
        for field_name, rule in rules.items():
            try:
                data[field_name] = rule(root)
            except Exception as exc:
                raise FieldParseError(f"{parser_name}: failed to parse {section_name}.{field_name}: {exc}") from exc

    try:
        return model(**data)
    except ValidationError as exc:
        raise ParseError(f"{parser_name}: model validation failed: {exc}") from exc


def param(root: ET.Element, name: str) -> str:
    return root.find(f".//What/Param[@name='{name}']").get("value")


def text(root: ET.Element, path: str) -> str:
    return root.find(path).text


def attr(root: ET.Element, path: str, attr_name: str) -> str:
    return root.find(path).get(attr_name)


def root_attr(root: ET.Element, attr_name: str) -> str:
    return root.get(attr_name)


def group_flag(root: ET.Element, group: str, name: str) -> bool:
    return root.find(f".//What/Group[@name='{group}']/Param[@name='{name}']").get("value") == "true"


def group_param(root: ET.Element, group: str, name: str) -> str | None:
    elem = root.find(f".//What/Group[@name='{group}']/Param[@name='{name}']")
    return elem.get("value") if elem is not None else None


def opt_position_float(root: ET.Element, path: str) -> float | None:
    elem = root.find(path)
    return float(elem.text) if elem is not None else None


def opt_text(root: ET.Element, path: str) -> str | None:
    elem = root.find(path)
    return elem.text if elem is not None else None


def opt_group_datetime(root: ET.Element, group: str, name: str) -> datetime | None:
    value = group_param(root, group, name)
    return parse_utc_datetime(value) if value is not None else None


def opt_group_float(root: ET.Element, group: str, name: str) -> float | None:
    value = group_param(root, group, name)
    return float(value) if value is not None else None


def citations(root: ET.Element, cite: str) -> tuple[str, ...]:
    return tuple(elem.text for elem in root.findall(f"Citations/EventIVORN[@cite='{cite}']"))


def description(root: ET.Element) -> str | None:
    return opt_text(root, "How/Description") or opt_text(root, "Citations/Description")
