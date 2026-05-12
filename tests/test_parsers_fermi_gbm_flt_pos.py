from datetime import datetime
from pathlib import Path
from xml.etree import ElementTree

import pytest

from gcnparser.fermi.fermi_gbm_flt_pos import FermiGBMFltPos
from gcnparser.fermi.fermi_gbm_flt_pos import parse_fermi_gbm_flt_pos
from tests._datetime import utcify_datetimes

FIXTURES = Path("tests/fixtures/fermi")

_BASE = dict(
    author_contact_name="Julie McEnery",
    author_email="Julie.E.McEnery@nasa.gov",
    packet_type=111,
    algorithm=3,
    coords_type=1,
    coords_string="source_object",
    reference_uri="http://gcn.gsfc.nasa.gov/fermi.html",
    importance=0.5,
    inference_probability=0.5,
    def_not_a_grb=False,
    target_in_blk_catalog=False,
    spatial_prox_match=False,
    temporal_prox_match=False,
    test_submission=False,
    values_out_of_range=False,
    delayed_transmission=True,
    flt_generated=True,
    gnd_generated=False,
    followup=None,
)


def _flt_pos(**overrides) -> FermiGBMFltPos:
    return FermiGBMFltPos(**utcify_datetimes({**_BASE, **overrides}))


@pytest.mark.parametrize(
    "filename, expected",
    [
        (
            "fermi_gbm_flt_pos/fermi_gbm_flt_pos_8126.xml",
            _flt_pos(
                ivorn="ivo://nasa.gsfc.gcn/Fermi#GBM_Flt_Pos_2026-02-07T05:42:33.65_792135758_44-945",
                alert_datetime=datetime(2026, 2, 7, 5, 43, 2),
                pkt_ser_num=5,
                trig_id=792135758,
                sequence_num=44,
                burst_tjd=21078,
                burst_sod=20553.65,
                burst_inten=152,
                trig_timescale=1.024,
                data_timescale=1.024,
                data_signif=6.4,
                phi=94.0,
                theta=40.0,
                sc_long=257.17,
                sc_lat=25.57,
                most_likely_index=4,
                most_likely_prob=72,
                sec_most_likely_index=7,
                sec_most_likely_prob=25,
                hardness_ratio=0.73,
                lightcurve_url="http://heasarc.gsfc.nasa.gov/FTP/fermi/data/gbm/triggers/2026/bn260207238/quicklook/glg_lc_medres34_bn260207238.gif",
                burst_datetime=datetime(2026, 2, 7, 5, 42, 33, 650000),
                ra=163.8167,
                dec=-35.4,
                error_radius=13.2667,
                followup="ivo://nasa.gsfc.gcn/Fermi#GBM_Alert_2026-02-07T05:42:33.65_792135758_1-944",
            ),
        ),
        (
            "fermi_gbm_flt_pos/fermi_gbm_flt_pos_8127.xml",
            _flt_pos(
                ivorn="ivo://nasa.gsfc.gcn/Fermi#GBM_Flt_Pos_2026-02-07T05:42:33.65_792135758_58-949",
                alert_datetime=datetime(2026, 2, 7, 5, 43, 11),
                pkt_ser_num=6,
                trig_id=792135758,
                sequence_num=58,
                burst_tjd=21078,
                burst_sod=20553.65,
                burst_inten=111,
                trig_timescale=4.096,
                data_timescale=4.096,
                data_signif=9.8,
                phi=92.0,
                theta=50.0,
                sc_long=257.17,
                sc_lat=25.57,
                most_likely_index=4,
                most_likely_prob=62,
                sec_most_likely_index=7,
                sec_most_likely_prob=36,
                hardness_ratio=0.78,
                lightcurve_url="http://heasarc.gsfc.nasa.gov/FTP/fermi/data/gbm/triggers/2026/bn260207238/quicklook/glg_lc_medres34_bn260207238.gif",
                burst_datetime=datetime(2026, 2, 7, 5, 42, 33, 650000),
                ra=176.3667,
                dec=-36.75,
                error_radius=10.3833,
                followup="ivo://nasa.gsfc.gcn/Fermi#GBM_Alert_2026-02-07T05:42:33.65_792135758_1-944",
            ),
        ),
        (
            "fermi_gbm_flt_pos/fermi_gbm_flt_pos_8131.xml",
            _flt_pos(
                ivorn="ivo://nasa.gsfc.gcn/Fermi#GBM_Flt_Pos_2026-02-08T04:53:37.18_792219222_72-565",
                alert_datetime=datetime(2026, 2, 8, 4, 54, 25),
                pkt_ser_num=10,
                trig_id=792219222,
                sequence_num=72,
                burst_tjd=21079,
                burst_sod=17617.18,
                burst_inten=4703,
                trig_timescale=4.096,
                data_timescale=4.096,
                data_signif=455.9,
                phi=354.0,
                theta=60.0,
                sc_long=169.38,
                sc_lat=0.77,
                most_likely_index=8,
                most_likely_prob=97,
                sec_most_likely_index=4,
                sec_most_likely_prob=1,
                hardness_ratio=7.39,
                lightcurve_url="http://heasarc.gsfc.nasa.gov/FTP/fermi/data/gbm/triggers/2026/bn260208204/quicklook/glg_lc_medres34_bn260208204.gif",
                burst_datetime=datetime(2026, 2, 8, 4, 53, 37, 180000),
                ra=320.0,
                dec=-6.6833,
                error_radius=3.45,
                followup="ivo://nasa.gsfc.gcn/Fermi#GBM_Alert_2026-02-08T04:53:37.18_792219222_1-558",
            ),
        ),
        (
            "fermi_gbm_flt_pos/fermi_gbm_flt_pos_8134.xml",
            _flt_pos(
                ivorn="ivo://nasa.gsfc.gcn/Fermi#GBM_Flt_Pos_2026-02-08T05:07:28.24_792220053_69-621",
                alert_datetime=datetime(2026, 2, 8, 5, 8, 31),
                pkt_ser_num=13,
                trig_id=792220053,
                sequence_num=69,
                burst_tjd=21079,
                burst_sod=18448.24,
                burst_inten=1409,
                trig_timescale=4.096,
                data_timescale=4.096,
                data_signif=140.4,
                phi=242.0,
                theta=70.0,
                sc_long=216.05,
                sc_lat=20.65,
                most_likely_index=4,
                most_likely_prob=84,
                sec_most_likely_index=7,
                sec_most_likely_prob=12,
                hardness_ratio=0.64,
                lightcurve_url="http://heasarc.gsfc.nasa.gov/FTP/fermi/data/gbm/triggers/2026/bn260208214/quicklook/glg_lc_medres34_bn260208214.gif",
                burst_datetime=datetime(2026, 2, 8, 5, 7, 28, 240000),
                ra=205.45,
                dec=42.2333,
                error_radius=3.9833,
                followup="ivo://nasa.gsfc.gcn/Fermi#GBM_Alert_2026-02-08T05:07:28.24_792220053_1-615",
            ),
        ),
    ],
)
def test_parse_fermi_gbm_flt_pos(filename, expected):
    payload = (FIXTURES / filename).read_bytes()
    result = parse_fermi_gbm_flt_pos(payload)
    assert result == expected


def test_parse_fermi_gbm_flt_pos_completes():
    """Tests parser runs without error over all fixtures."""
    for p in filter(lambda s: s.suffix == ".xml", (FIXTURES / "fermi_gbm_flt_pos").iterdir()):
        parse_fermi_gbm_flt_pos(p.read_bytes())


_KEEP = frozenset({"Who", "What", "WhereWhen", "How", "Why", "Citations"})


def _has_sections(root: ElementTree.Element) -> set[str]:
    result = set()
    for child in root:
        local = child.tag.split("}")[-1] if "}" in child.tag else child.tag
        if local in _KEEP:
            result.add(local)
    return result


def test_all_flt_pos_fixtures_have_standard_sections():
    """All fermi_gbm_flt_pos fixtures must contain the standard VOE sections."""
    fixtures = sorted(p for p in (FIXTURES / "fermi_gbm_flt_pos").iterdir() if p.suffix == ".xml")
    assert len(fixtures) >= 2

    for path in fixtures:
        sections = _has_sections(ElementTree.fromstring(path.read_bytes()))
        assert sections == _KEEP, f"{path.name} missing sections: {_KEEP - sections}"
