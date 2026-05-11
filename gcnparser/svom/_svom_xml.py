"""Internal SVOM-specific XML helpers.

These helpers keep small conversion and fallback logic out of the mission
parser rule maps.
"""

from datetime import datetime
from xml.etree import ElementTree as ET

from gcnparser.parse_xml import group_param
from gcnparser.parse_xml import opt_text


def parse_datetime(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


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
