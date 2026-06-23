from datetime import datetime
from datetime import timezone
from pathlib import Path
from xml.etree import ElementTree

import pytest

from gcn_parser.svom import parse_svom_mxt
from gcn_parser.svom import SvomMxt
from gcn_parser.svom import SvomPacket
from tests._datetime import assert_datetime_fields_timezone_aware
from tests._datetime import utcify_datetimes

FIXTURES = Path("tests/fixtures/svom/mxt")

_BASE = dict(
    author_contact_name="Henri Louvin",
    author_email="svom-contact@cea.fr",
    pkt_ser_num=1,
    instrument="MXT",
    notice_level="N2m",
    description="N2m notice, data from MXT",
    reference_uri="https://www.svom.eu/en/mxt-microchannel-x-ray-telescope-en/",
)


def _notice(**overrides) -> SvomMxt:
    return SvomMxt(**utcify_datetimes({**_BASE, **overrides}))


@pytest.mark.parametrize(
    "filename, expected",
    [
        (
            "mxt_40.xml",
            _notice(
                ivorn="ivo://org.svom/fsc#sb26022501_mxt-initial_qf1",
                alert_datetime=datetime(2026, 2, 25, 10, 17, 26, tzinfo=timezone.utc),
                packet_type=209,
                burst_id="sb26022501",
                alert_seq_t0=None,
                snr=42.0,
                mean_flux=0.07,
                flux_error=0.27,
                within_eclairs_r90=False,
                eclairs_angle=29.11,
                galactic_lon=98.01,
                galactic_lat=69.61,
                moon_angle=93.03,
                sun_angle=126.2,
                use_vt_attitude=False,
                attitude_ra=194.38,
                attitude_dec=24.21,
                attitude_roll=287.22,
                sat_longitude=151.53,
                sat_latitude=-7.08,
                sat_altitude=615.16,
                burst_datetime=datetime(2026, 2, 25, 9, 36, 39, 104000),
                ra=204.8665,
                dec=45.1204,
                error_radius=0.0643,
                followups=(
                    "ivo://org.svom/fsc#sb26022501_eclairs-preliminary",
                    "ivo://org.svom/fsc#sb26022501_eclairs-wakeup",
                    "ivo://org.svom/fsc#sb26022501_slewing",
                ),
            ),
        ),
        (
            "mxt_42.xml",
            _notice(
                ivorn="ivo://org.svom/fsc#sb26022802_mxt-update_qf2",
                alert_datetime=datetime(2026, 3, 1, 1, 27, 8, tzinfo=timezone.utc),
                packet_type=210,
                burst_id="sb26022802",
                alert_seq_t0=None,
                snr=101.0,
                mean_flux=0.07,
                flux_error=0.26,
                within_eclairs_r90=False,
                eclairs_angle=28.34,
                galactic_lon=41.81,
                galactic_lat=50.36,
                moon_angle=94.84,
                sun_angle=106.04,
                use_vt_attitude=True,
                attitude_ra=205.22,
                attitude_dec=15.23,
                attitude_roll=274.68,
                sat_longitude=-12.9,
                sat_latitude=16.16,
                sat_altitude=613.39,
                burst_datetime=datetime(2026, 2, 28, 21, 48, 46, 626000),
                ra=237.4077,
                dec=26.0255,
                error_radius=0.034,
                followups=(
                    "ivo://org.svom/fsc#sb26022802_eclairs-preliminary",
                    "ivo://org.svom/fsc#sb26022802_eclairs-wakeup",
                    "ivo://org.svom/fsc#sb26022802_slewing",
                    "ivo://org.svom/fsc#sb26022802_mxt-initial_qf1",
                ),
            ),
        ),
    ],
)
def test_parse_svom_mxt(filename, expected):
    payload = (FIXTURES / filename).read_bytes()
    result = parse_svom_mxt(payload)
    assert result == expected


def test_parse_svom_mxt_completes():
    for path in filter(lambda p: p.suffix == ".xml", FIXTURES.iterdir()):
        parse_svom_mxt(path.read_bytes())


def test_parse_svom_mxt_datetimes_are_timezone_aware():
    for path in filter(lambda p: p.suffix == ".xml", FIXTURES.iterdir()):
        result = parse_svom_mxt(path.read_bytes())
        assert_datetime_fields_timezone_aware(result)


_KEEP = frozenset({"Who", "What", "WhereWhen", "How", "Citations"})


def _has_sections(root: ElementTree.Element) -> set[str]:
    result = set()
    for child in root:
        local = child.tag.split("}")[-1] if "}" in child.tag else child.tag
        if local in _KEEP:
            result.add(local)
    return result


def test_all_mxt_fixtures_have_standard_sections():
    fixtures = sorted(p for p in FIXTURES.iterdir() if p.suffix == ".xml")
    assert len(fixtures) >= 2

    for path in fixtures:
        sections = _has_sections(ElementTree.fromstring(path.read_bytes()))
        assert sections == _KEEP, f"{path.name} missing sections: {_KEEP - sections}"
