"""Internal SVOM-specific XML helpers."""

from datetime import datetime
from xml.etree import ElementTree as ET

from gcnparser.parse_xml import group_param
from gcnparser.parse_xml import opt_text
from gcnparser.parse_xml import parse_utc_datetime as parse_datetime


def opt_group_datetime(root: ET.Element, group: str, name: str) -> datetime | None:
    value = group_param(root, group, name)
    return parse_datetime(value) if value is not None else None


def opt_group_float(root: ET.Element, group: str, name: str) -> float | None:
    value = group_param(root, group, name)
    return float(value) if value is not None else None


def opt_position_float(root: ET.Element, path: str) -> float | None:
    elem = root.find(path)
    return float(elem.text) if elem is not None else None


def citations(root: ET.Element, cite: str) -> tuple[str, ...]:
    return tuple(elem.text for elem in root.findall(f"Citations/EventIVORN[@cite='{cite}']"))


def description(root: ET.Element) -> str | None:
    return opt_text(root, "How/Description") or opt_text(root, "Citations/Description")
