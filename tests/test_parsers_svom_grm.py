from datetime import datetime
from datetime import timezone
from pathlib import Path
from xml.etree import ElementTree

import pytest

from gcnparser.svom import parse_svom_grm_trigger
from gcnparser.svom import SvomGrm
from tests._datetime import utcify_datetimes

FIXTURES = Path("tests/fixtures/svom/grm")

_BASE = dict(
    author_contact_name="Henri Louvin",
    author_email="svom-contact@cea.fr",
    packet_type=201,
    pkt_ser_num=1,
    instrument="GRM",
    notice_level="N1g",
    description="N1g notice, data from GRM",
    reference_uri="https://www.svom.eu/en/grm-gamma-ray-burst-monitor-en/",
)


def _trigger(**overrides) -> SvomGrm:
    return SvomGrm(**utcify_datetimes({**_BASE, **overrides}))


@pytest.mark.parametrize(
    "filename, expected",
    [
        (
            "grm_284.xml",
            _trigger(
                ivorn="ivo://org.svom/fsc#sb26020401_grm-trigger",
                alert_datetime=datetime(2026, 2, 4, 10, 11, 54, tzinfo=timezone.utc),
                burst_id="sb26020401",
                alert_seq_t0=None,
                snr=91.40,
                timescale=1.0,
                time_window_start=datetime(2026, 2, 4, 10, 11, 30, tzinfo=timezone.utc),
                time_window_end=datetime(2026, 2, 4, 10, 11, 31, tzinfo=timezone.utc),
                lower_energy_bound=8.539406,
                upper_energy_bound=17.078812,
                triggered_grds="101",
                galactic_lon=None,
                galactic_lat=None,
                moon_angle=None,
                sun_angle=None,
                attitude_ra=26.59,
                attitude_dec=61.75,
                attitude_roll=116.03,
                sat_longitude=40.54,
                sat_latitude=29.12,
                sat_altitude=615.22,
                burst_datetime=datetime(2026, 2, 4, 10, 11, 30),
                ra=None,
                dec=None,
                error_radius=None,
            ),
        ),
        (
            "grm_285.xml",
            _trigger(
                ivorn="ivo://org.svom/fsc#sb26020402_grm-trigger",
                alert_datetime=datetime(2026, 2, 4, 12, 8, 39, tzinfo=timezone.utc),
                burst_id="sb26020402",
                alert_seq_t0=None,
                snr=8.90,
                timescale=1.0,
                time_window_start=datetime(2026, 2, 4, 12, 8, 18, tzinfo=timezone.utc),
                time_window_end=datetime(2026, 2, 4, 12, 8, 19, tzinfo=timezone.utc),
                lower_energy_bound=8.539406,
                upper_energy_bound=17.078812,
                triggered_grds="110",
                galactic_lon=None,
                galactic_lat=None,
                moon_angle=None,
                sun_angle=None,
                attitude_ra=192.97,
                attitude_dec=20.38,
                attitude_roll=264.84,
                sat_longitude=86.32,
                sat_latitude=7.01,
                sat_altitude=614.40,
                burst_datetime=datetime(2026, 2, 4, 12, 8, 18),
                ra=None,
                dec=None,
                error_radius=None,
            ),
        ),
        (
            "grm_288.xml",
            _trigger(
                ivorn="ivo://org.svom/fsc#sb26020404_grm-trigger",
                alert_datetime=datetime(2026, 2, 4, 16, 50, 53, tzinfo=timezone.utc),
                burst_id="sb26020404",
                alert_seq_t0=None,
                snr=7.40,
                timescale=4.0,
                time_window_start=datetime(2026, 2, 4, 16, 50, 17, tzinfo=timezone.utc),
                time_window_end=datetime(2026, 2, 4, 16, 50, 21, tzinfo=timezone.utc),
                lower_energy_bound=51.236435,
                upper_energy_bound=264.7216,
                triggered_grds="011",
                galactic_lon=None,
                galactic_lat=None,
                moon_angle=None,
                sun_angle=None,
                attitude_ra=205.23,
                attitude_dec=1.98,
                attitude_roll=253.29,
                sat_longitude=-16.02,
                sat_latitude=20.87,
                sat_altitude=613.74,
                burst_datetime=datetime(2026, 2, 4, 16, 50, 17),
                ra=None,
                dec=None,
                error_radius=None,
            ),
        ),
        (
            "grm_330.xml",
            _trigger(
                ivorn="ivo://org.svom/fsc#sb26042101_grm-trigger",
                alert_datetime=datetime(2026, 4, 21, 0, 24, 33, tzinfo=timezone.utc),
                burst_id="sb26042101",
                alert_seq_t0=datetime(2026, 4, 21, 0, 24, 3, tzinfo=timezone.utc),
                snr=16.70,
                timescale=1.0,
                time_window_start=datetime(2026, 4, 21, 0, 24, 2, tzinfo=timezone.utc),
                time_window_end=datetime(2026, 4, 21, 0, 24, 3, tzinfo=timezone.utc),
                lower_energy_bound=8.539406,
                upper_energy_bound=17.078812,
                triggered_grds="111",
                galactic_lon=286.02,
                galactic_lat=19.10,
                moon_angle=110.30,
                sun_angle=136.37,
                attitude_ra=186.66,
                attitude_dec=-62.77,
                attitude_roll=153.21,
                sat_longitude=132.20,
                sat_latitude=-22.66,
                sat_altitude=620.66,
                burst_datetime=datetime(2026, 4, 21, 0, 24, 2),
                ra=171.5201,
                dec=-40.9497,
                error_radius=-1.0,
            ),
        ),
        (
            "grm_344.xml",
            _trigger(
                ivorn="ivo://org.svom/fsc#sb26050401_grm-trigger",
                alert_datetime=datetime(2026, 5, 4, 7, 10, 33, tzinfo=timezone.utc),
                burst_id="sb26050401",
                alert_seq_t0=datetime(2026, 5, 4, 7, 10, 6, 600000, tzinfo=timezone.utc),
                snr=8.70,
                timescale=0.1,
                time_window_start=datetime(2026, 5, 4, 7, 10, 6, 500000, tzinfo=timezone.utc),
                time_window_end=datetime(2026, 5, 4, 7, 10, 6, 600000, tzinfo=timezone.utc),
                lower_energy_bound=51.236435,
                upper_energy_bound=264.7216,
                triggered_grds="111",
                galactic_lon=332.78,
                galactic_lat=2.24,
                moon_angle=22.51,
                sun_angle=142.80,
                attitude_ra=14.62,
                attitude_dec=-72.38,
                attitude_roll=334.62,
                sat_longitude=80.83,
                sat_latitude=8.57,
                sat_altitude=614.86,
                burst_datetime=datetime(2026, 5, 4, 7, 10, 6, 500000),
                ra=242.0199,
                dec=-48.8985,
                error_radius=-1.0,
            ),
        ),
    ],
)
def test_parse_svom_grm_trigger(filename: str, expected: SvomGrm):
    payload = (FIXTURES / filename).read_bytes()
    result = parse_svom_grm_trigger(payload)
    assert result == expected


def test_parse_svom_grm_completes():
    for path in sorted(FIXTURES.glob("*.xml")):
        root = ElementTree.fromstring(path.read_bytes())
        packet_type = int(root.find(".//What/Param[@name='Packet_Type']").get("value"))
        if packet_type == 201:
            result = parse_svom_grm_trigger(path.read_bytes())
            assert isinstance(result, SvomGrm)


_KEEP = frozenset({"Who", "What", "WhereWhen", "How"})


def _has_sections(root: ElementTree.Element) -> set[str]:
    result = set()
    for child in root:
        local = child.tag.split("}")[-1] if "}" in child.tag else child.tag
        if local in _KEEP:
            result.add(local)
    return result


def test_all_grm_trigger_fixtures_have_standard_sections():
    fixtures = sorted(p for p in FIXTURES.iterdir() if p.suffix == ".xml")
    assert len(fixtures) >= 2

    for path in fixtures:
        root = ElementTree.fromstring(path.read_bytes())
        packet_type = int(root.find(".//What/Param[@name='Packet_Type']").get("value"))
        if packet_type == 201:
            sections = _has_sections(root)
            assert sections == _KEEP, f"{path.name} missing sections: {_KEEP - sections}"
