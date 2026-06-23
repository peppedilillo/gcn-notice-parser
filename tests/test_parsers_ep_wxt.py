from datetime import datetime
from datetime import timezone
from pathlib import Path

import pytest

from gcn_parser.ep import EinsteinProbeWXT
from gcn_parser.ep import parse_einstein_probe_wxt
from tests._datetime import assert_datetime_fields_timezone_aware

FIXTURES = Path("tests/fixtures/ep/alert")

_BASE = dict(
    instrument="WXT",
    image_energy_range=(0.5, 4.0),
    additional_info=(
        "The net count rate is derived from an accumulated image (up to 20 min) "
        "in 0.5-4 keV, assuming a constant flux. However, it can be significantly "
        "lower than the actual count rate of a burst with a duration much shorter "
        "than 20 min."
    ),
)


def _alert(**overrides) -> EinsteinProbeWXT:
    return EinsteinProbeWXT(**{**_BASE, **overrides})


@pytest.mark.parametrize(
    "filename, expected",
    [
        (
            "alert_247.json",
            _alert(
                trigger_time=datetime(2026, 4, 9, 11, 45, 11, 949000, tzinfo=timezone.utc),
                id=("01709259773",),
                ra=184.664,
                dec=-6.146,
                ra_dec_error=0.05174976,
                net_count_rate=0.07,
                image_snr=7.0,
            ),
        ),
        (
            "alert_258.json",
            _alert(
                trigger_time=datetime(2026, 5, 7, 13, 47, 57, 951000, tzinfo=timezone.utc),
                id=("01709261593",),
                ra=206.895,
                dec=-22.243,
                ra_dec_error=0.05065978,
                net_count_rate=0.07,
                image_snr=10.0,
            ),
        ),
    ],
)
def test_parse_einstein_probe_wxt(filename: str, expected: EinsteinProbeWXT):
    payload = (FIXTURES / filename).read_bytes()
    result = parse_einstein_probe_wxt(payload)
    assert result == expected


def test_parse_einstein_probe_wxt_completes():
    for path in sorted(FIXTURES.glob("*.json")):
        result = parse_einstein_probe_wxt(path.read_bytes())
        assert isinstance(result, EinsteinProbeWXT)
        assert result.instrument == "WXT"


def test_parse_einstein_probe_wxt_datetimes_are_timezone_aware():
    for path in sorted(FIXTURES.glob("*.json")):
        result = parse_einstein_probe_wxt(path.read_bytes())
        assert_datetime_fields_timezone_aware(result)
