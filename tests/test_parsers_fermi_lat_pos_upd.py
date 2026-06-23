from datetime import datetime
from pathlib import Path
from xml.etree import ElementTree

import pytest

from gcn_parser.fermi.fermi_lat_pos_upd import FermiLATPosUpd
from gcn_parser.fermi.fermi_lat_pos_upd import parse_fermi_lat_pos_upd
from tests._datetime import assert_datetime_fields_timezone_aware
from tests._datetime import utcify_datetimes

FIXTURES = Path("tests/fixtures/fermi")

_BASE = dict(
    author_contact_name="Julie McEnery",
    author_email="Julie.E.McEnery@nasa.gov",
    packet_type=121,
    record_num=0,
    burst_tjd=11910,
    burst_sod=0.0,
    trig_index=0,
    temp_test_stat=458.75,
    image_test_stat=544.5,
    coords_type=1,
    coords_string="source_object",
    reference_uri="http://gcn.gsfc.nasa.gov/fermi.html",
    importance=0.5,
    inference_probability=0.5,
    all_gammas_used=False,
    only_gammas_above_used=True,
    def_not_a_grb=False,
    spatial_prox_match=False,
    temporal_prox_match=False,
    report_request_made=False,
    values_out_of_range=False,
    near_bright_star=False,
    err_circle_in_galaxy=False,
    galaxy_in_err_circle=False,
)


def _lat_pos_upd(**overrides) -> FermiLATPosUpd:
    return FermiLATPosUpd(**utcify_datetimes({**_BASE, **overrides}))


_FOLLOWUP = "ivo://nasa.gsfc.gcn/Fermi#LAT_Initial_Pos_2026-01--9130T00:00:00.00_793795104_0-086"


@pytest.mark.parametrize(
    "filename, expected",
    [
        (
            "fermi_lat_pos_upd/fermi_lat_pos_upd_0.xml",
            _lat_pos_upd(
                ivorn="ivo://nasa.gsfc.gcn/Fermi#LAT_Updated_Pos_2026-01--9130T00:00:00.00_793795104_0-094",
                alert_datetime=datetime(2026, 2, 26, 10, 39, 21),
                pkt_ser_num=1,
                trig_id=793795104,
                burst_inten=186,
                cnts_e1=220,
                cnts_e2=173,
                cnts_e3=11,
                cnts_e4=2,
                integ_time=8.044,
                burst_datetime=datetime(2026, 2, 26, 10, 38),
                ra=42.2166,
                dec=8.0333,
                error_radius=0.5,
                followup=_FOLLOWUP,
            ),
        ),
        (
            "fermi_lat_pos_upd/fermi_lat_pos_upd_1.xml",
            _lat_pos_upd(
                ivorn="ivo://nasa.gsfc.gcn/Fermi#LAT_Updated_Pos_2026-01--9130T00:00:00.00_793795104_0-095",
                alert_datetime=datetime(2026, 2, 26, 10, 39, 41),
                pkt_ser_num=2,
                trig_id=793795104,
                burst_inten=248,
                cnts_e1=78,
                cnts_e2=232,
                cnts_e3=11,
                cnts_e4=5,
                integ_time=12.08,
                burst_datetime=datetime(2026, 2, 26, 10, 38),
                ra=42.3,
                dec=8.0166,
                error_radius=0.5,
                followup=_FOLLOWUP,
            ),
        ),
        (
            "fermi_lat_pos_upd/fermi_lat_pos_upd_2.xml",
            _lat_pos_upd(
                ivorn="ivo://nasa.gsfc.gcn/Fermi#LAT_Updated_Pos_2026-01--9130T00:00:00.00_793795104_0-096",
                alert_datetime=datetime(2026, 2, 26, 10, 40, 2),
                pkt_ser_num=3,
                trig_id=793795104,
                burst_inten=352,
                cnts_e1=32,
                cnts_e2=74,
                cnts_e3=14,
                cnts_e4=8,
                integ_time=20.044,
                burst_datetime=datetime(2026, 2, 26, 10, 38),
                ra=42.2166,
                dec=7.9833,
                error_radius=0.5,
                followup=_FOLLOWUP,
            ),
        ),
    ],
)
def test_parse_fermi_lat_pos_upd(filename, expected):
    payload = (FIXTURES / filename).read_bytes()
    result = parse_fermi_lat_pos_upd(payload)
    assert result == expected


def test_parse_fermi_lat_pos_upd_completes():
    """Tests parser runs without error over all fixtures."""
    for p in filter(lambda s: s.suffix == ".xml", (FIXTURES / "fermi_lat_pos_upd").iterdir()):
        parse_fermi_lat_pos_upd(p.read_bytes())


def test_parse_fermi_lat_pos_upd_datetimes_are_timezone_aware():
    for p in filter(lambda s: s.suffix == ".xml", (FIXTURES / "fermi_lat_pos_upd").iterdir()):
        result = parse_fermi_lat_pos_upd(p.read_bytes())
        assert_datetime_fields_timezone_aware(result)


def test_all_lat_pos_upd_fixtures_have_standard_sections():
    """All fermi_lat_pos_upd fixtures must contain the standard VOE sections."""
    fixtures = sorted(p for p in (FIXTURES / "fermi_lat_pos_upd").iterdir() if p.suffix == ".xml")
    _KEEP = frozenset({"Who", "What", "WhereWhen", "How", "Why"})

    for path in fixtures:
        root = ElementTree.fromstring(path.read_bytes())
        sections = set()
        for child in root:
            local = child.tag.split("}")[-1] if "}" in child.tag else child.tag
            if local in _KEEP:
                sections.add(local)
        assert sections == _KEEP, f"{path.name} missing sections: {_KEEP - sections}"
