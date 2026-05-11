from datetime import datetime
from pathlib import Path
from xml.etree import ElementTree

import pytest

from gcnparser.fermi.fermi_lat_pos_ini import FermiLATPosIni
from gcnparser.fermi.fermi_lat_pos_ini import parse_fermi_lat_pos_ini

FIXTURES = Path("tests/fixtures/fermi")

_BASE = dict(
    author_contact_name="Julie McEnery",
    author_email="Julie.E.McEnery@nasa.gov",
    packet_type=120,
    record_num=0,
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
    followup=None,
)


def _lat_pos_ini(**overrides) -> FermiLATPosIni:
    return FermiLATPosIni(**{**_BASE, **overrides})


@pytest.mark.parametrize(
    "filename, expected",
    [
        (
            "fermi_lat_pos_ini/fermi_lat_pos_ini_0.xml",
            _lat_pos_ini(
                ivorn="ivo://nasa.gsfc.gcn/Fermi#LAT_Initial_Pos_2026-01--9130T00:00:00.00_793795104_0-086",
                alert_datetime=datetime(2026, 2, 26, 10, 39),
                pkt_ser_num=1,
                trig_id=793795104,
                burst_tjd=11910,
                burst_sod=0.0,
                burst_inten=98,
                cnts_e1=101,
                cnts_e2=91,
                cnts_e3=6,
                cnts_e4=1,
                integ_time=3.092,
                trig_index=0,
                temp_test_stat=458.75,
                image_test_stat=544.5,
                burst_datetime=datetime(2026, 2, 26, 10, 38),
                ra=42.2333,
                dec=8.0,
                error_radius=0.5,
            ),
        ),
    ],
)
def test_parse_fermi_lat_pos_ini(filename, expected):
    payload = (FIXTURES / filename).read_bytes()
    result = parse_fermi_lat_pos_ini(payload)
    assert result == expected


def test_parse_fermi_lat_pos_ini_completes():
    """Tests parser runs without error over all fixtures."""
    for p in filter(lambda s: s.suffix == ".xml", (FIXTURES / "fermi_lat_pos_ini").iterdir()):
        parse_fermi_lat_pos_ini(p.read_bytes())


def test_all_lat_pos_ini_fixtures_have_standard_sections():
    """All fermi_lat_pos_ini fixtures must contain the standard VOE sections."""
    fixtures = sorted(p for p in (FIXTURES / "fermi_lat_pos_ini").iterdir() if p.suffix == ".xml")

    ref_sections = ElementTree.fromstring(fixtures[0].read_bytes())
    _KEEP = frozenset({"Who", "What", "WhereWhen", "How", "Why"})
    sections = set()
    for child in ref_sections:
        local = child.tag.split("}")[-1] if "}" in child.tag else child.tag
        if local in _KEEP:
            sections.add(local)
    assert sections == _KEEP
