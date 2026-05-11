"""Shared XML extraction helpers and parser error boundary.

This module contains the small helper surface used by mission-specific
parsers plus the common ``parse_notice`` assembly routine.
"""

from collections.abc import Callable
from xml.etree import ElementTree as ET

from pydantic import ValidationError

Rule = Callable[[ET.Element], object]
SectionRules = dict[str, Rule]
Sections = dict[str, SectionRules]


class ParseError(Exception):
    pass


class FieldParseError(ParseError):
    pass


def parse_notice(value: bytes, model: type, parser_name: str, sections: Sections):
    try:
        root = ET.fromstring(value)
    except ET.ParseError as exc:
        raise ParseError(f"{parser_name}: failed to parse document: {exc}") from exc

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


def opt_text(root: ET.Element, path: str) -> str | None:
    elem = root.find(path)
    return elem.text if elem is not None else None


def group_flag(root: ET.Element, group: str, name: str) -> bool:
    return root.find(f".//What/Group[@name='{group}']/Param[@name='{name}']").get("value") == "true"


def group_param(root: ET.Element, group: str, name: str) -> str | None:
    elem = root.find(f".//What/Group[@name='{group}']/Param[@name='{name}']")
    return elem.get("value") if elem is not None else None
