from datetime import datetime
from pathlib import Path
from xml.etree import ElementTree

import pytest

from gcnparser.fermi.fermi_lat_pos_diag import FermiLATPosDiag
from gcnparser.fermi.fermi_lat_pos_diag import parse_fermi_lat_pos_diag
from tests._datetime import utcify_datetimes

FIXTURES = Path("tests/fixtures/fermi")

_BASE = dict(
    author_contact_name="Julie McEnery",
    author_email="Julie.E.McEnery@nasa.gov",
    packet_type=122,
    record_num=0,
    burst_tjd=11910,
    burst_sod=0.0,
    trig_index=0,
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


def _lat_pos_diag(**overrides) -> FermiLATPosDiag:
    return FermiLATPosDiag(**utcify_datetimes({**_BASE, **overrides}))


_FOLLOWUP = "ivo://nasa.gsfc.gcn/Fermi#LAT_Initial_Pos_2026-01--9130T00:00:00.00_793795104_0-086"


@pytest.mark.parametrize(
    "filename, expected",
    [
        (
            "fermi_lat_pos_diag/fermi_lat_pos_diag_0.xml",
            _lat_pos_diag(
                ivorn="ivo://nasa.gsfc.gcn/Fermi#LAT_Final_Pos_2026-01--9130T00:00:00.00_793795104_0-134",
                alert_datetime=datetime(2026, 2, 26, 10, 48, 44),
                pkt_ser_num=1,
                trig_id=793795104,
                burst_inten=2898,
                cnts_e1=247,
                cnts_e2=21,
                cnts_e3=123,
                cnts_e4=194,
                integ_time=2401.224,
                temp_test_stat=41.25,
                image_test_stat=55.25,
                burst_datetime=datetime(2026, 2, 26, 10, 38),
                ra=42.0166,
                dec=8.05,
                error_radius=0.5,
                followup=_FOLLOWUP,
            ),
        ),
    ],
)
def test_parse_fermi_lat_pos_diag(filename, expected):
    payload = (FIXTURES / filename).read_bytes()
    result = parse_fermi_lat_pos_diag(payload)
    assert result == expected


def test_parse_fermi_lat_pos_diag_completes():
    """Tests parser runs without error over all fixtures."""
    for p in filter(lambda s: s.suffix == ".xml", (FIXTURES / "fermi_lat_pos_diag").iterdir()):
        parse_fermi_lat_pos_diag(p.read_bytes())


def test_all_lat_pos_diag_fixtures_have_standard_sections():
    """All fermi_lat_pos_diag fixtures must contain the standard VOE sections."""
    fixtures = sorted(p for p in (FIXTURES / "fermi_lat_pos_diag").iterdir() if p.suffix == ".xml")
    _KEEP = frozenset({"Who", "What", "WhereWhen", "How", "Why"})

    for path in fixtures:
        root = ElementTree.fromstring(path.read_bytes())
        sections = set()
        for child in root:
            local = child.tag.split("}")[-1] if "}" in child.tag else child.tag
            if local in _KEEP:
                sections.add(local)
        assert sections == _KEEP, f"{path.name} missing sections: {_KEEP - sections}"
