from datetime import datetime
from pathlib import Path
from xml.etree import ElementTree

import pytest

from gcnparser.fermi.fermi_gbm_fin_pos import FermiGBMFinPos
from gcnparser.fermi.fermi_gbm_fin_pos import parse_fermi_gbm_fin_pos
from tests._datetime import utcify_datetimes

FIXTURES = Path("tests/fixtures/fermi")

_BASE = dict(
    author_contact_name="Julie McEnery",
    author_email="Julie.E.McEnery@nasa.gov",
    packet_type=115,
    sequence_num=0,
    burst_inten=0,
    data_integ=0.0,
    burst_signif=0.0,
    algorithm=41731,
    lo_energy=44032,
    hi_energy=279965,
    coords_type=1,
    coords_string="source_object",
    reference_uri="http://gcn.gsfc.nasa.gov/fermi.html",
    importance=0.95,
    inference_probability=1.0,
    def_not_a_grb=False,
    target_in_blk_catalog=False,
    human_generated=False,
    robo_generated=True,
    long_short="Long",
    spatial_prox_match=False,
    temporal_prox_match=False,
    test_submission=False,
    values_out_of_range=False,
    flt_generated=False,
    gnd_generated=True,
    crc_error=False,
    followup=None,
)


def _fin_pos(**overrides) -> FermiGBMFinPos:
    return FermiGBMFinPos(**utcify_datetimes({**_BASE, **overrides}))


@pytest.mark.parametrize(
    "filename, expected",
    [
        (
            "fermi_gbm_fin_pos/fermi_gbm_fin_pos_981.xml",
            _fin_pos(
                ivorn="ivo://nasa.gsfc.gcn/Fermi#GBM_Fin_Pos2026-02-04T16:50:06.96_791916611_0-084",
                alert_datetime=datetime(2026, 2, 4, 16, 59, 16),
                pkt_ser_num=14,
                trig_id=791916611,
                burst_tjd=21075,
                burst_sod=60606.96,
                phi=327.0,
                theta=70.0,
                lightcurve_url="http://heasarc.gsfc.nasa.gov/FTP/fermi/data/gbm/triggers/2026/bn260204701/quicklook/glg_lc_medres34_bn260204701.gif",
                locationmap_url="http://heasarc.gsfc.nasa.gov/FTP/fermi/data/gbm/triggers/2026/bn260204701/quicklook/glg_locplot_all_bn260204701.png",
                burst_datetime=datetime(2026, 2, 4, 16, 50, 6, 960000),
                ra=338.46,
                dec=-50.11,
                error_radius=6.38,
                followup="ivo://nasa.gsfc.gcn/Fermi#GBM_Alert_2026-02-04T16:50:06.96_791916611_1-047",
            ),
        ),
        (
            "fermi_gbm_fin_pos/fermi_gbm_fin_pos_1027.xml",
            _fin_pos(
                ivorn="ivo://nasa.gsfc.gcn/Fermi#GBM_Fin_Pos2026-04-02T22:57:17.54_796863442_0-545",
                alert_datetime=datetime(2026, 4, 2, 23, 6, 36),
                pkt_ser_num=17,
                trig_id=796863442,
                burst_tjd=21132,
                burst_sod=82637.54,
                phi=132.0,
                theta=72.0,
                lightcurve_url="http://heasarc.gsfc.nasa.gov/FTP/fermi/data/gbm/triggers/2026/bn260402956/quicklook/glg_lc_medres34_bn260402956.gif",
                locationmap_url="http://heasarc.gsfc.nasa.gov/FTP/fermi/data/gbm/triggers/2026/bn260402956/quicklook/glg_locplot_all_bn260402956.png",
                burst_datetime=datetime(2026, 4, 2, 22, 57, 17, 540000),
                ra=238.41,
                dec=0.18,
                error_radius=11.43,
                followup="ivo://nasa.gsfc.gcn/Fermi#GBM_Alert_2026-04-02T22:57:17.54_796863442_1-510",
            ),
        ),
        (
            "fermi_gbm_fin_pos/fermi_gbm_fin_pos_1039.xml",
            _fin_pos(
                ivorn="ivo://nasa.gsfc.gcn/Fermi#GBM_Fin_Pos2026-04-15T04:43:59.31_797921044_0-825",
                alert_datetime=datetime(2026, 4, 15, 4, 53, 27),
                pkt_ser_num=10,
                trig_id=797921044,
                burst_tjd=21145,
                burst_sod=17039.31,
                phi=48.0,
                theta=92.0,
                temporal_prox_match=True,
                lightcurve_url="http://heasarc.gsfc.nasa.gov/FTP/fermi/data/gbm/triggers/2026/bn260415197/quicklook/glg_lc_medres34_bn260415197.gif",
                locationmap_url="http://heasarc.gsfc.nasa.gov/FTP/fermi/data/gbm/triggers/2026/bn260415197/quicklook/glg_locplot_all_bn260415197.png",
                burst_datetime=datetime(2026, 4, 15, 4, 43, 59, 310000),
                ra=58.49,
                dec=-24.0,
                error_radius=5.55,
                followup="ivo://nasa.gsfc.gcn/Fermi#GBM_Alert_2026-04-15T04:43:59.31_797921044_1-784",
            ),
        ),
    ],
)
def test_parse_fermi_gbm_fin_pos(filename, expected):
    payload = (FIXTURES / filename).read_bytes()
    result = parse_fermi_gbm_fin_pos(payload)
    assert result == expected


def test_parse_fermi_gbm_fin_pos_completes():
    """Tests parser runs without error over all fixtures."""
    for p in filter(lambda s: s.suffix == ".xml", (FIXTURES / "fermi_gbm_fin_pos").iterdir()):
        parse_fermi_gbm_fin_pos(p.read_bytes())


_KEEP = frozenset({"Who", "What", "WhereWhen", "How", "Why"})


def _has_sections(root: ElementTree.Element) -> set[str]:
    result = set()
    for child in root:
        local = child.tag.split("}")[-1] if "}" in child.tag else child.tag
        if local in _KEEP:
            result.add(local)
    return result


def test_all_fin_pos_fixtures_have_standard_sections():
    """All fermi_gbm_fin_pos fixtures must contain the standard VOE sections."""
    fixtures = sorted(p for p in (FIXTURES / "fermi_gbm_fin_pos").iterdir() if p.suffix == ".xml")
    assert len(fixtures) >= 2

    for path in fixtures:
        sections = _has_sections(ElementTree.fromstring(path.read_bytes()))
        assert sections == _KEEP, f"{path.name} missing sections: {_KEEP - sections}"
