from datetime import datetime
from datetime import timezone
from pathlib import Path
from xml.etree import ElementTree

import pytest

from gcn_parser.exceptions import ParseError
from gcn_parser.svom import parse_svom_eclairs
from gcn_parser.svom import SvomEclairs
from gcn_parser.svom import SvomPacket
from tests._datetime import assert_datetime_fields_timezone_aware
from tests._datetime import utcify_datetimes

FIXTURES = Path("tests/fixtures/svom/eclairs")

_BASE = dict(
    author_contact_name="Henri Louvin",
    author_email="svom-contact@cea.fr",
    pkt_ser_num=1,
    instrument="ECLAIRs",
    notice_level="N1e",
    description="N1e notice, data from ECLAIRs",
    reference_uri="https://www.svom.eu/en/telescope-eclairs-en/",
    alert_seq_t0=None,
    onboard_catalog_id=None,
    source_name=None,
    followups=(),
)


def _notice(**overrides) -> SvomEclairs:
    return SvomEclairs(**utcify_datetimes({**_BASE, **overrides}))


@pytest.mark.parametrize(
    "filename, expected",
    [
        (
            "eclairs_296.xml",
            _notice(
                ivorn="ivo://org.svom/fsc#sb26021102_eclairs-wakeup",
                alert_datetime=datetime(2026, 2, 11, 19, 25, 50, tzinfo=timezone.utc),
                packet_type=SvomPacket.ECLAIR_WAKEUP,
                burst_id="sb26021102",
                snr=12.79,
                timescale=40.96,
                time_window_start=datetime(2026, 2, 11, 19, 24, 23, 604000, tzinfo=timezone.utc),
                time_window_end=datetime(2026, 2, 11, 19, 25, 4, 564000, tzinfo=timezone.utc),
                lower_energy_bound=5,
                upper_energy_bound=20,
                trigger_type="IMT",
                galactic_lon=205.94,
                galactic_lat=-14.3,
                moon_angle=149.61,
                sun_angle=120.75,
                slew_status="not-requested",
                attitude_ra=114.17,
                attitude_dec=22.7,
                attitude_roll=78.74,
                sat_longitude=112.3,
                sat_latitude=-2.46,
                sat_altitude=621.27,
                burst_datetime=datetime(2026, 2, 11, 19, 24, 23, 604000),
                ra=86.9755,
                dec=-0.4379,
                error_radius=0.1057,
            ),
        ),
        (
            "eclairs_310.xml",
            _notice(
                ivorn="ivo://org.svom/fsc#sb26041206_eclairs-wakeup",
                alert_datetime=datetime(2026, 4, 12, 6, 23, 20, tzinfo=timezone.utc),
                packet_type=SvomPacket.ECLAIR_WAKEUP,
                burst_id="sb26041206",
                snr=32.31,
                timescale=20.4,
                time_window_start=datetime(2026, 4, 12, 6, 13, 48, 759000, tzinfo=timezone.utc),
                time_window_end=datetime(2026, 4, 12, 6, 14, 9, 159000, tzinfo=timezone.utc),
                lower_energy_bound=8,
                upper_energy_bound=120,
                trigger_type="CRT",
                galactic_lon=250.16,
                galactic_lat=-34.56,
                moon_angle=97.77,
                sun_angle=75.4,
                slew_status="rejected",
                attitude_ra=110.67,
                attitude_dec=-20.94,
                attitude_roll=82.06,
                sat_longitude=None,
                sat_latitude=None,
                sat_altitude=None,
                burst_datetime=datetime(2026, 4, 12, 6, 13, 48, 759000),
                ra=79.9016,
                dec=-44.5946,
                error_radius=0.0519,
                alert_seq_t0=datetime(2026, 4, 12, 6, 13, 46, 139000, tzinfo=timezone.utc),
                followups=("ivo://org.svom/fsc#sb26041206_not-slewing",),
            ),
        ),
        (
            "svom_voevent_sb25091702_eclairs-catalog.xml",
            _notice(
                author_contact_name="Timothe Roland",
                author_email="svom-contact@cea.fr",
                ivorn="ivo://org.svom/fsc#sb25091702_eclairs-catalog",
                alert_datetime=datetime(2025, 9, 17, 12, 1, 42, tzinfo=timezone.utc),
                packet_type=SvomPacket.ECLAIR_CATALOG,
                pkt_ser_num=1,
                burst_id="sb25091702",
                snr=24.95,
                timescale=20.48,
                time_window_start=datetime(2025, 9, 17, 12, 0, 45, 860000, tzinfo=timezone.utc),
                time_window_end=datetime(2025, 9, 17, 12, 1, 6, 340000, tzinfo=timezone.utc),
                lower_energy_bound=5,
                upper_energy_bound=20,
                trigger_type="IMT",
                galactic_lon=343.88,
                galactic_lat=-1.32,
                moon_angle=134.35,
                sun_angle=85.39,
                slew_status="not-requested",
                attitude_ra=268.28,
                attitude_dec=-35.32,
                attitude_roll=90.15,
                sat_longitude=29.52,
                sat_latitude=7.3,
                sat_altitude=615.93,
                burst_datetime=datetime(2025, 9, 17, 12, 0, 45, 860000),
                ra=256.5645,
                dec=-43.0392,
                error_radius=0.0613,
                onboard_catalog_id=81,
                source_name="GX 340-00",
            ),
        ),
        (
            "eclairs_300.xml",
            _notice(
                ivorn="ivo://org.svom/fsc#sb26022501_slewing",
                alert_datetime=datetime(2026, 2, 25, 8, 54, 17, tzinfo=timezone.utc),
                packet_type=SvomPacket.ECLAIR_SLEWING,
                burst_id="sb26022501",
                snr=16.32,
                timescale=40.96,
                time_window_start=datetime(2026, 2, 25, 8, 50, 57, 169000, tzinfo=timezone.utc),
                time_window_end=datetime(2026, 2, 25, 8, 51, 38, 129000, tzinfo=timezone.utc),
                lower_energy_bound=8,
                upper_energy_bound=120,
                trigger_type="IMT",
                galactic_lon=97.62,
                galactic_lat=70.08,
                moon_angle=93.55,
                sun_angle=126.52,
                slew_status="accepted",
                attitude_ra=194.38,
                attitude_dec=24.21,
                attitude_roll=287.22,
                sat_longitude=-5.69,
                sat_latitude=0.98,
                sat_altitude=620.72,
                burst_datetime=datetime(2026, 2, 25, 8, 50, 57, 169000),
                ra=204.6748,
                dec=44.6546,
                error_radius=0.0854,
                followups=(
                    "ivo://org.svom/fsc#sb26022501_eclairs-preliminary",
                    "ivo://org.svom/fsc#sb26022501_eclairs-wakeup",
                ),
            ),
        ),
        (
            "eclairs_297.xml",
            _notice(
                ivorn="ivo://org.svom/fsc#sb26021102_not-slewing",
                alert_datetime=datetime(2026, 2, 11, 19, 32, 24, tzinfo=timezone.utc),
                packet_type=SvomPacket.ECLAIR_NOT_SLEWING,
                burst_id="sb26021102",
                snr=14.48,
                timescale=20.4,
                time_window_start=datetime(2026, 2, 11, 19, 24, 28, 734000, tzinfo=timezone.utc),
                time_window_end=datetime(2026, 2, 11, 19, 24, 49, 134000, tzinfo=timezone.utc),
                lower_energy_bound=5,
                upper_energy_bound=20,
                trigger_type="CRT",
                galactic_lon=205.94,
                galactic_lat=-14.28,
                moon_angle=149.61,
                sun_angle=120.77,
                slew_status="rejected",
                attitude_ra=114.17,
                attitude_dec=22.7,
                attitude_roll=78.74,
                sat_longitude=110.98,
                sat_latitude=-3.18,
                sat_altitude=621.36,
                burst_datetime=datetime(2026, 2, 11, 19, 24, 28, 734000),
                ra=86.9994,
                dec=-0.4306,
                error_radius=0.0947,
                followups=(
                    "ivo://org.svom/fsc#sb26021102_eclairs-preliminary",
                    "ivo://org.svom/fsc#sb26021102_eclairs-wakeup",
                ),
            ),
        ),
    ],
)
def test_parse_svom_eclairs(filename, expected):
    payload = (FIXTURES / filename).read_bytes()
    result = parse_svom_eclairs(payload)
    assert result == expected


def test_parse_svom_eclairs_completes():
    for path in filter(lambda p: p.suffix == ".xml", FIXTURES.iterdir()):
        if path.name == "eclairs_304.xml":
            continue
        parse_svom_eclairs(path.read_bytes())


def test_parse_svom_eclairs_datetimes_are_timezone_aware():
    for path in filter(lambda p: p.suffix == ".xml", FIXTURES.iterdir()):
        if path.name == "eclairs_304.xml":
            continue
        result = parse_svom_eclairs(path.read_bytes())
        assert_datetime_fields_timezone_aware(result)


def test_parse_svom_eclairs_rejects_retraction():
    with pytest.raises(ParseError):
        parse_svom_eclairs((FIXTURES / "eclairs_304.xml").read_bytes())


_KEEP = frozenset({"Who", "What", "WhereWhen", "How"})


def _has_sections(root: ElementTree.Element) -> set[str]:
    result = set()
    for child in root:
        local = child.tag.split("}")[-1] if "}" in child.tag else child.tag
        if local in _KEEP:
            result.add(local)
    return result


def test_all_non_retraction_eclairs_fixtures_have_standard_sections():
    fixtures = sorted(p for p in FIXTURES.iterdir() if p.suffix == ".xml" and p.name != "eclairs_304.xml")
    assert len(fixtures) >= 2

    for path in fixtures:
        sections = _has_sections(ElementTree.fromstring(path.read_bytes()))
        assert sections == _KEEP, f"{path.name} missing sections: {_KEEP - sections}"
