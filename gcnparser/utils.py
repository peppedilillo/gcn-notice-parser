from xml.etree import ElementTree as ET


def param(root: ET.Element, name: str) -> str:
    return root.find(f".//What/Param[@name='{name}']").get("value")


def text(root: ET.Element, path: str) -> str:
    return root.find(path).text


def attr(root: ET.Element, path: str, attr_name: str) -> str:
    return root.find(path).get(attr_name)


def opt_text(root: ET.Element, path: str) -> str | None:
    elem = root.find(path)
    return elem.text if elem is not None else None


def group_flag(root: ET.Element, group: str, name: str) -> bool:
    return root.find(f".//What/Group[@name='{group}']/Param[@name='{name}']").get("value") == "true"


def group_param(root: ET.Element, group: str, name: str) -> str | None:
    elem = root.find(f".//What/Group[@name='{group}']/Param[@name='{name}']")
    return elem.get("value") if elem is not None else None
