from pathlib import Path

from pydantic import BaseModel
import pytest

from gcnparser.fermi.fermi_gbm_alert import parse_fermi_gbm_alert
from gcnparser.fermi.fermi_lat_pos_ini import parse_fermi_lat_pos_ini
from gcnparser.parse_xml import FieldParseError
from gcnparser.parse_xml import param as _param
from gcnparser.parse_xml import parse_notice
from gcnparser.parse_xml import ParseError

FIXTURES = Path("tests/fixtures/fermi")


class DummyModel(BaseModel):
    value: int


def test_parse_notice_wraps_missing_field_errors():
    payload = b"<VOEvent><What /></VOEvent>"

    with pytest.raises(FieldParseError) as exc_info:
        parse_notice(
            payload,
            DummyModel,
            "dummy_parser",
            {"What": {"value": lambda root: int(_param(root, "Value"))}},
        )

    assert "dummy_parser: failed to parse What.value" in str(exc_info.value)
    assert isinstance(exc_info.value.__cause__, AttributeError)


def test_parse_notice_wraps_type_conversion_errors():
    payload = b'<VOEvent><What><Param name="Value" value="abc" /></What></VOEvent>'

    with pytest.raises(FieldParseError) as exc_info:
        parse_notice(
            payload,
            DummyModel,
            "dummy_parser",
            {"What": {"value": lambda root: int(_param(root, "Value"))}},
        )

    assert "dummy_parser: failed to parse What.value" in str(exc_info.value)
    assert isinstance(exc_info.value.__cause__, ValueError)


def test_parse_notice_wraps_malformed_xml():
    payload = b"<VOEvent"

    with pytest.raises(ParseError) as exc_info:
        parse_notice(payload, DummyModel, "dummy_parser", {})

    assert "dummy_parser: failed to parse document" in str(exc_info.value)
    assert isinstance(exc_info.value.__cause__, Exception)


def test_parse_fermi_gbm_alert_wraps_corrupted_fixture():
    payload = (FIXTURES / "fermi_gbm_alert/fermi_gbm_alert_3785.xml").read_bytes()
    broken = payload.replace(b'name="LightCurve_URL"', b'name="Missing_LightCurve_URL"', 1)

    with pytest.raises(FieldParseError) as exc_info:
        parse_fermi_gbm_alert(broken)

    assert "parse_fermi_gbm_alert: failed to parse What.lightcurve_url" in str(exc_info.value)
    assert isinstance(exc_info.value.__cause__, AttributeError)


def test_parse_fermi_lat_pos_ini_wraps_corrupted_fixture():
    payload = (FIXTURES / "fermi_lat_pos_ini/fermi_lat_pos_ini_0.xml").read_bytes()
    broken = payload.replace(b'value="120"', b'value="not-an-int"', 1)

    with pytest.raises(FieldParseError) as exc_info:
        parse_fermi_lat_pos_ini(broken)

    assert "parse_fermi_lat_pos: failed to parse What.packet_type" in str(exc_info.value)
    assert isinstance(exc_info.value.__cause__, ValueError)
