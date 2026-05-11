from datetime import datetime
from pathlib import Path
from xml.etree import ElementTree

import pytest

from gcnparser.fermi.fermi_gbm_gnd_pos import FermiGBMGndPos
from gcnparser.fermi.fermi_gbm_gnd_pos import parse_fermi_gbm_gnd_pos

FIXTURES = Path("tests/fixtures/fermi")

_BASE = dict(
    author_contact_name="Julie McEnery",
    author_email="Julie.E.McEnery@nasa.gov",
    packet_type=112,
    algorithm=4173,
    lo_energy=44032,
    hi_energy=279965,
    coords_type=1,
    coords_string="source_object",
    reference_uri="http://gcn.gsfc.nasa.gov/fermi.html",
    importance=0.95,
    inference_probability=0.5,
    burst_inten=0,
    def_not_a_grb=False,
    target_in_blk_catalog=False,
    spatial_prox_match=False,
    long_short="unknown",
    temporal_prox_match=False,
    test_submission=False,
    values_out_of_range=False,
    flt_generated=False,
    gnd_generated=True,
    crc_error=False,
    followup=None,
)


def _gnd_pos(**overrides) -> FermiGBMGndPos:
    return FermiGBMGndPos(**{**_BASE, **overrides})


@pytest.mark.parametrize(
    "filename, expected",
    [
        (
            "fermi_gbm_gnd_pos/fermi_gbm_gnd_pos_1698.xml",
            _gnd_pos(
                ivorn="ivo://nasa.gsfc.gcn/Fermi#GBM_Gnd_Pos_2026-02-04T16:50:06.96_791916611_57-053",
                alert_datetime=datetime(2026, 2, 4, 16, 50, 54),
                pkt_ser_num=36,
                trig_id=791916611,
                sequence_num=57,
                burst_tjd=21075,
                burst_sod=60606.96,
                data_integ=4.096,
                burst_signif=6.9,
                phi=326.0,
                theta=72.0,
                sc_geo_x=-56376,
                sc_geo_y=-93324,
                sc_geo_z=-13688,
                lightcurve_url="http://heasarc.gsfc.nasa.gov/FTP/fermi/data/gbm/triggers/2026/bn260204701/quicklook/glg_lc_medres34_bn260204701.gif",
                locationmap_url="http://gcn.gsfc.nasa.gov/notices_f/gbm_gnd_loc_map_791916611.fits",
                burst_datetime=datetime(2026, 2, 4, 16, 50, 6, 960000),
                ra=341.07,
                dec=-49.11,
                error_radius=12.04,
                followup="ivo://nasa.gsfc.gcn/Fermi#GBM_Alert_2026-02-04T16:50:06.96_791916611_1-047",
            ),
        ),
        (
            "fermi_gbm_gnd_pos/fermi_gbm_gnd_pos_1704.xml",
            _gnd_pos(
                ivorn="ivo://nasa.gsfc.gcn/Fermi#GBM_Gnd_Pos_2026-02-07T13:12:10.83_792162735_59-451",
                alert_datetime=datetime(2026, 2, 7, 13, 12, 57),
                pkt_ser_num=4,
                trig_id=792162735,
                sequence_num=59,
                burst_tjd=21078,
                burst_sod=47530.83,
                data_integ=0.064,
                burst_signif=83.4,
                phi=278.0,
                theta=50.0,
                sc_geo_x=92504,
                sc_geo_y=59036,
                sc_geo_z=7796,
                lightcurve_url="http://heasarc.gsfc.nasa.gov/FTP/fermi/data/gbm/triggers/2026/bn260207550/quicklook/glg_lc_medres34_bn260207550.gif",
                locationmap_url="http://gcn.gsfc.nasa.gov/notices_f/gbm_gnd_loc_map_792162735.fits",
                burst_datetime=datetime(2026, 2, 7, 13, 12, 10, 830000),
                ra=283.81,
                dec=50.33,
                error_radius=2.16,
                followup="ivo://nasa.gsfc.gcn/Fermi#GBM_Alert_2026-02-07T13:12:10.83_792162735_1-449",
            ),
        ),
        (
            "fermi_gbm_gnd_pos/fermi_gbm_gnd_pos_1826.xml",
            _gnd_pos(
                ivorn="ivo://nasa.gsfc.gcn/Fermi#GBM_Gnd_Pos_2026-04-09T17:32:45.67_797448770_58-663",
                alert_datetime=datetime(2026, 4, 9, 17, 33, 33),
                pkt_ser_num=1,
                trig_id=797448770,
                sequence_num=58,
                burst_tjd=21139,
                burst_sod=63165.67,
                data_integ=4.096,
                burst_signif=26.8,
                phi=56.0,
                theta=109.0,
                sc_geo_x=91096,
                sc_geo_y=-61348,
                sc_geo_z=5900,
                lightcurve_url="http://heasarc.gsfc.nasa.gov/FTP/fermi/data/gbm/triggers/2026/bn260409731/quicklook/glg_lc_medres34_bn260409731.gif",
                locationmap_url="http://gcn.gsfc.nasa.gov/notices_f/gbm_gnd_loc_map_797448770.fits",
                burst_datetime=datetime(2026, 4, 9, 17, 32, 45, 670000),
                ra=304.69,
                dec=48.88,
                error_radius=3.27,
                followup="ivo://nasa.gsfc.gcn/Fermi#GBM_Alert_2026-04-09T17:32:45.67_797448770_1-657",
            ),
        ),
    ],
)
def test_parse_fermi_gbm_gnd_pos(filename, expected):
    payload = (FIXTURES / filename).read_bytes()
    result = parse_fermi_gbm_gnd_pos(payload)
    assert result == expected


def test_parse_fermi_gbm_gnd_pos_completes():
    """Tests parser runs without error over all fixtures."""
    for p in filter(lambda s: s.suffix == ".xml", (FIXTURES / "fermi_gbm_gnd_pos").iterdir()):
        parse_fermi_gbm_gnd_pos(p.read_bytes())


_KEEP = frozenset({"Who", "What", "WhereWhen", "How", "Why"})


def _has_sections(root: ElementTree.Element) -> set[str]:
    result = set()
    for child in root:
        local = child.tag.split("}")[-1] if "}" in child.tag else child.tag
        if local in _KEEP:
            result.add(local)
    return result


def test_all_gnd_pos_fixtures_have_standard_sections():
    """All fermi_gbm_gnd_pos fixtures must contain the standard VOE sections."""
    fixtures = sorted(p for p in (FIXTURES / "fermi_gbm_gnd_pos").iterdir() if p.suffix == ".xml")
    assert len(fixtures) >= 2

    for path in fixtures:
        sections = _has_sections(ElementTree.fromstring(path.read_bytes()))
        assert sections == _KEEP, f"{path.name} missing sections: {_KEEP - sections}"
