from datetime import datetime
from pathlib import Path
from xml.etree import ElementTree

import pytest

from gcn_parser.fermi.fermi_lat_offline import FermiLATOffline
from gcn_parser.fermi.fermi_lat_offline import parse_fermi_lat_offline
from tests._datetime import utcify_datetimes

FIXTURES = Path("tests/fixtures/fermi")

_BASE = dict(
    author_contact_name="Julie McEnery",
    author_email="Julie.E.McEnery@nasa.gov",
    packet_type=128,
    burst_inten=0,
    integ_time=0.0,
    trigger_signif=-0.0,
    coords_type=1,
    coords_string="source_object",
    reference_uri="http://gcn.gsfc.nasa.gov/fermi.html",
    importance=0.9,
    inference_probability=0.9,
    def_not_a_grb=False,
    spatial_prox_match=False,
    report_request_made=False,
    values_out_of_range=False,
    near_bright_star=False,
    err_circle_in_galaxy=False,
    galaxy_in_err_circle=False,
    followup=None,
)


def _lat_offline(**overrides) -> FermiLATOffline:
    return FermiLATOffline(**utcify_datetimes({**_BASE, **overrides}))


@pytest.mark.parametrize(
    "filename, expected",
    [
        (
            "fermi_lat_offline/fermi_lat_offline_29.xml",
            _lat_offline(
                ivorn="ivo://nasa.gsfc.gcn/Fermi#LAT_Offline_Pos_2026-02-26T10:38:18.84_793795080-0-190",
                alert_datetime=datetime(2026, 2, 26, 15, 42, 21),
                pkt_ser_num=3,
                trig_id=793795080,
                burst_tjd=21097,
                burst_sod=38298.84,
                all_gammas_used=True,
                only_gammas_above_used=False,
                temporal_prox_match=True,
                burst_datetime=datetime(2026, 2, 26, 10, 38, 18, 840000),
                ra=41.9209,
                dec=7.7199,
                error_radius=0.1059,
            ),
        ),
    ],
)
def test_parse_fermi_lat_offline(filename, expected):
    payload = (FIXTURES / filename).read_bytes()
    result = parse_fermi_lat_offline(payload)
    assert result == expected


def test_parse_fermi_lat_offline_completes():
    """Tests parser runs without error over all fixtures."""
    for p in filter(lambda s: s.suffix == ".xml", (FIXTURES / "fermi_lat_offline").iterdir()):
        parse_fermi_lat_offline(p.read_bytes())


def test_all_lat_offline_fixtures_have_standard_sections():
    """All fermi_lat_offline fixtures must contain the standard VOE sections."""
    fixtures = sorted(p for p in (FIXTURES / "fermi_lat_offline").iterdir() if p.suffix == ".xml")
    _KEEP = frozenset({"Who", "What", "WhereWhen", "How", "Why"})

    for path in fixtures:
        root = ElementTree.fromstring(path.read_bytes())
        sections = set()
        for child in root:
            local = child.tag.split("}")[-1] if "}" in child.tag else child.tag
            if local in _KEEP:
                sections.add(local)
        assert sections == _KEEP, f"{path.name} missing sections: {_KEEP - sections}"
