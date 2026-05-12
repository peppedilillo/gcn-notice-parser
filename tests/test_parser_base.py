from pathlib import Path

from pydantic import BaseModel
import pytest

from gcnparser.ep.wxt import parse_einstein_probe_wxt
from gcnparser.exceptions import FieldParseError
from gcnparser.exceptions import ParseError
from gcnparser.fermi.fermi_gbm_alert import parse_fermi_gbm_alert
from gcnparser.fermi.fermi_lat_pos_ini import parse_fermi_lat_pos_ini
from gcnparser.parse_json import parse_json_notice
from gcnparser.parse_xml import param as _param
from gcnparser.parse_xml import parse_voevent_notice

FIXTURES = Path("tests/fixtures/fermi")
EP_FIXTURES = Path("tests/fixtures/ep")


class DummyModel(BaseModel):
    value: int


def test_parse_notice_wraps_missing_field_errors():
    payload = b"<VOEvent><What /></VOEvent>"

    with pytest.raises(FieldParseError) as exc_info:
        parse_voevent_notice(
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
        parse_voevent_notice(
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
        parse_voevent_notice(payload, DummyModel, "dummy_parser", {})

    assert "dummy_parser: failed to parse document" in str(exc_info.value)
    assert isinstance(exc_info.value.__cause__, Exception)


def test_parse_json_notice_wraps_malformed_json():
    payload = b"{"

    with pytest.raises(ParseError) as exc_info:
        parse_json_notice(payload, DummyModel, "dummy_parser")

    assert "dummy_parser: failed to parse document" in str(exc_info.value)
    assert isinstance(exc_info.value.__cause__, Exception)


def test_parse_json_notice_wraps_model_validation_errors():
    payload = b'{"value": "abc"}'

    with pytest.raises(ParseError) as exc_info:
        parse_json_notice(payload, DummyModel, "dummy_parser")

    assert "dummy_parser: model validation failed" in str(exc_info.value)
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


def test_parse_einstein_probe_wxt_wraps_corrupted_fixture():
    payload = (EP_FIXTURES / "alert/alert_247.json").read_bytes()
    broken = payload.replace(b'"ra": 184.664', b'"ra": "not-a-float"', 1)

    with pytest.raises(ParseError) as exc_info:
        parse_einstein_probe_wxt(broken)

    assert "parse_einstein_probe_wxt: model validation failed" in str(exc_info.value)
    assert isinstance(exc_info.value.__cause__, Exception)
