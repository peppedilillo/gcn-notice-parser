from datetime import datetime
from pathlib import Path
from xml.etree import ElementTree

import pytest

from gcnparser.fermi.fermi_gbm_alert import FermiGBMAlert
from gcnparser.fermi.fermi_gbm_alert import parse_fermi_gbm_alert
from tests._datetime import utcify_datetimes

FIXTURES = Path("tests/fixtures/fermi")

_BASE = dict(
    author_contact_name="Julie McEnery",
    author_email="Julie.E.McEnery@nasa.gov",
    packet_type=110,
    sequence_num=1,
    coords_type=0,
    coords_string="unavailable/inappropriate",
    reference_uri="http://gcn.gsfc.nasa.gov/fermi.html",
    importance=0.5,
    inference_probability=0.5,
    values_out_of_range=False,
    near_bright_star=False,
    err_circle_in_galaxy=False,
    galaxy_in_err_circle=False,
    too_generated=False,
    trig_time_is_sec_hdr_time=False,
    delayed_transmission=False,
    updated_notice=False,
    flt_generated=True,
    gnd_generated=False,
    temporal_prox_match=False,
    crc_error=False,
    hi_chan_energy=291,
    followup=None,
)


def _alert(**overrides) -> FermiGBMAlert:
    return FermiGBMAlert(**utcify_datetimes({**_BASE, **overrides}))


@pytest.mark.parametrize(
    "filename, expected",
    [
        (
            "fermi_gbm_alert/fermi_gbm_alert_3785.xml",
            _alert(
                ivorn="ivo://nasa.gsfc.gcn/Fermi#GBM_Alert_2026-02-07T05:42:33.65_792135758_1-944",
                alert_datetime=datetime(2026, 2, 7, 5, 42, 39),
                pkt_ser_num=2,
                trig_id=792135758,
                burst_tjd=21078,
                burst_sod=20553.65,
                trig_signif=4.7,
                trig_dur=0.512,
                lo_chan_index=3,
                hi_chan_index=4,
                lo_chan_energy=47,
                adc_lo_chan=259,
                adc_hi_chan=1352,
                algorithm=10,
                dets=("1", "2"),
                sc_long=257.167,
                sc_lat=25.567,
                lightcurve_url="http://heasarc.gsfc.nasa.gov/FTP/fermi/data/gbm/triggers/2026/bn260207238/quicklook/glg_lc_medres34_bn260207238.gif",
                burst_datetime=datetime(2026, 2, 7, 5, 42, 33, 650000),
            ),
        ),
        (
            "fermi_gbm_alert/fermi_gbm_alert_3786.xml",
            _alert(
                ivorn="ivo://nasa.gsfc.gcn/Fermi#GBM_Alert_2026-02-07T13:12:10.83_792162735_1-449",
                alert_datetime=datetime(2026, 2, 7, 13, 12, 17),
                pkt_ser_num=3,
                trig_id=792162735,
                burst_tjd=21078,
                burst_sod=47530.83,
                trig_signif=8.4,
                trig_dur=0.016,
                lo_chan_index=3,
                hi_chan_index=4,
                lo_chan_energy=47,
                adc_lo_chan=259,
                adc_hi_chan=1352,
                algorithm=1,
                dets=("6", "7", "8"),
                sc_long=56.75,
                sc_lat=4.033,
                lightcurve_url="http://heasarc.gsfc.nasa.gov/FTP/fermi/data/gbm/triggers/2026/bn260207550/quicklook/glg_lc_medres34_bn260207550.gif",
                burst_datetime=datetime(2026, 2, 7, 13, 12, 10, 830000),
            ),
        ),
        (
            "fermi_gbm_alert/fermi_gbm_alert_3787.xml",
            _alert(
                ivorn="ivo://nasa.gsfc.gcn/Fermi#GBM_Alert_2026-02-08T04:53:37.18_792219222_1-558",
                alert_datetime=datetime(2026, 2, 8, 4, 53, 42),
                pkt_ser_num=4,
                trig_id=792219222,
                burst_tjd=21079,
                burst_sod=17617.18,
                trig_signif=6.0,
                trig_dur=0.064,
                lo_chan_index=2,
                hi_chan_index=2,
                lo_chan_energy=23,
                hi_chan_energy=47,
                adc_lo_chan=143,
                adc_hi_chan=258,
                algorithm=26,
                dets=("0", "1", "5"),
                sc_long=169.383,
                sc_lat=0.767,
                lightcurve_url="http://heasarc.gsfc.nasa.gov/FTP/fermi/data/gbm/triggers/2026/bn260208204/quicklook/glg_lc_medres34_bn260208204.gif",
                burst_datetime=datetime(2026, 2, 8, 4, 53, 37, 180000),
            ),
        ),
        (
            "fermi_gbm_alert/fermi_gbm_alert_3788.xml",
            _alert(
                ivorn="ivo://nasa.gsfc.gcn/Fermi#GBM_Alert_2026-02-08T05:07:28.24_792220053_1-615",
                alert_datetime=datetime(2026, 2, 8, 5, 7, 33),
                pkt_ser_num=5,
                trig_id=792220053,
                burst_tjd=21079,
                burst_sod=18448.24,
                trig_signif=4.7,
                trig_dur=2.048,
                lo_chan_index=3,
                hi_chan_index=4,
                lo_chan_energy=47,
                adc_lo_chan=259,
                adc_hi_chan=1352,
                algorithm=14,
                dets=("6", "8"),
                sc_long=216.05,
                sc_lat=20.65,
                lightcurve_url="http://heasarc.gsfc.nasa.gov/FTP/fermi/data/gbm/triggers/2026/bn260208214/quicklook/glg_lc_medres34_bn260208214.gif",
                burst_datetime=datetime(2026, 2, 8, 5, 7, 28, 240000),
            ),
        ),
        (
            "fermi_gbm_alert/fermi_gbm_alert_3789.xml",
            _alert(
                ivorn="ivo://nasa.gsfc.gcn/Fermi#GBM_Alert_2026-02-08T08:00:55.65_792230460_1-189",
                alert_datetime=datetime(2026, 2, 8, 8, 0, 57),
                pkt_ser_num=6,
                trig_id=792230460,
                burst_tjd=21079,
                burst_sod=28855.65,
                trig_signif=13.6,
                trig_dur=0.016,
                lo_chan_index=5,
                hi_chan_index=7,
                lo_chan_energy=291,
                hi_chan_energy=None,
                adc_lo_chan=1353,
                adc_hi_chan=4095,
                algorithm=43,
                dets=("2", "4", "5"),
                sc_long=116.817,
                sc_lat=-1.467,
                lightcurve_url="http://heasarc.gsfc.nasa.gov/FTP/fermi/data/gbm/triggers/2026/bn260208334/quicklook/glg_lc_medres34_bn260208334.gif",
                burst_datetime=datetime(2026, 2, 8, 8, 0, 55, 650000),
            ),
        ),
        (
            "fermi_gbm_alert/fermi_gbm_alert_3790.xml",
            _alert(
                ivorn="ivo://nasa.gsfc.gcn/Fermi#GBM_Alert_2026-02-08T09:52:44.91_792237169_1-554",
                alert_datetime=datetime(2026, 2, 8, 9, 52, 49),
                pkt_ser_num=7,
                trig_id=792237169,
                burst_tjd=21079,
                burst_sod=35564.91,
                trig_signif=5.1,
                trig_dur=4.096,
                lo_chan_index=3,
                hi_chan_index=4,
                lo_chan_energy=47,
                adc_lo_chan=259,
                adc_hi_chan=1352,
                algorithm=16,
                dets=("6", "7", "9"),
                sc_long=152.1,
                sc_lat=22.683,
                lightcurve_url="http://heasarc.gsfc.nasa.gov/FTP/fermi/data/gbm/triggers/2026/bn260208412/quicklook/glg_lc_medres34_bn260208412.gif",
                burst_datetime=datetime(2026, 2, 8, 9, 52, 44, 910000),
            ),
        ),
        (
            "fermi_gbm_alert/fermi_gbm_alert_3791.xml",
            _alert(
                ivorn="ivo://nasa.gsfc.gcn/Fermi#GBM_Alert_2026-02-08T11:17:13.37_792242238_1-846",
                alert_datetime=datetime(2026, 2, 8, 11, 17, 14),
                pkt_ser_num=8,
                trig_id=792242238,
                burst_tjd=21079,
                burst_sod=40633.37,
                trig_signif=6.5,
                trig_dur=0.064,
                lo_chan_index=2,
                hi_chan_index=2,
                lo_chan_energy=23,
                hi_chan_energy=47,
                adc_lo_chan=143,
                adc_hi_chan=258,
                algorithm=26,
                dets=("3", "5"),
                sc_long=93.083,
                sc_lat=10.733,
                lightcurve_url="http://heasarc.gsfc.nasa.gov/FTP/fermi/data/gbm/triggers/2026/bn260208470/quicklook/glg_lc_medres34_bn260208470.gif",
                burst_datetime=datetime(2026, 2, 8, 11, 17, 13, 370000),
            ),
        ),
        (
            "fermi_gbm_alert/fermi_gbm_alert_3792.xml",
            _alert(
                ivorn="ivo://nasa.gsfc.gcn/Fermi#GBM_Alert_2026-02-08T15:12:18.59_792256343_1-624",
                alert_datetime=datetime(2026, 2, 8, 15, 12, 24),
                pkt_ser_num=9,
                trig_id=792256343,
                burst_tjd=21079,
                burst_sod=54738.59,
                trig_signif=4.9,
                trig_dur=0.512,
                lo_chan_index=3,
                hi_chan_index=4,
                lo_chan_energy=47,
                adc_lo_chan=259,
                adc_hi_chan=1352,
                algorithm=11,
                dets=("3", "4", "5"),
                sc_long=210.267,
                sc_lat=-9.55,
                lightcurve_url="http://heasarc.gsfc.nasa.gov/FTP/fermi/data/gbm/triggers/2026/bn260208634/quicklook/glg_lc_medres34_bn260208634.gif",
                burst_datetime=datetime(2026, 2, 8, 15, 12, 18, 590000),
            ),
        ),
        (
            "fermi_gbm_alert/fermi_gbm_alert_3793.xml",
            _alert(
                ivorn="ivo://nasa.gsfc.gcn/Fermi#GBM_Alert_2026-02-08T21:42:45.48_792279770_1-920",
                alert_datetime=datetime(2026, 2, 8, 21, 42, 51),
                pkt_ser_num=10,
                trig_id=792279770,
                burst_tjd=21079,
                burst_sod=78165.48,
                trig_signif=5.0,
                trig_dur=4.096,
                lo_chan_index=3,
                hi_chan_index=4,
                lo_chan_energy=47,
                adc_lo_chan=259,
                adc_hi_chan=1352,
                algorithm=17,
                dets=("3", "4", "5"),
                sc_long=160.8,
                sc_lat=-24.35,
                lightcurve_url="http://heasarc.gsfc.nasa.gov/FTP/fermi/data/gbm/triggers/2026/bn260208905/quicklook/glg_lc_medres34_bn260208905.gif",
                burst_datetime=datetime(2026, 2, 8, 21, 42, 45, 480000),
            ),
        ),
        (
            "fermi_gbm_alert/fermi_gbm_alert_3794.xml",
            _alert(
                ivorn="ivo://nasa.gsfc.gcn/Fermi#GBM_Alert_2026-02-09T02:45:57.24_792297962_1-931",
                alert_datetime=datetime(2026, 2, 9, 2, 46, 3),
                pkt_ser_num=11,
                trig_id=792297962,
                burst_tjd=21080,
                burst_sod=9957.24,
                trig_signif=4.3,
                trig_dur=0.256,
                lo_chan_index=3,
                hi_chan_index=4,
                lo_chan_energy=47,
                adc_lo_chan=259,
                adc_hi_chan=1352,
                algorithm=8,
                dets=("9", "A"),
                sc_long=164.55,
                sc_lat=-12.633,
                lightcurve_url="http://heasarc.gsfc.nasa.gov/FTP/fermi/data/gbm/triggers/2026/bn260209115/quicklook/glg_lc_medres34_bn260209115.gif",
                burst_datetime=datetime(2026, 2, 9, 2, 45, 57, 240000),
            ),
        ),
    ],
)
def test_parse_fermi_gbm_alert(filename, expected):
    payload = (FIXTURES / filename).read_bytes()
    result = parse_fermi_gbm_alert(payload)
    assert result == expected


def test_parse_fermi_gbm_completes():
    """Tests parser runs without error over all fixtures."""
    for p in filter(lambda s: s.suffix == ".xml", (FIXTURES / "fermi_gbm_alert").iterdir()):
        parse_fermi_gbm_alert(p.read_bytes())


_KEEP = frozenset({"Who", "What", "WhereWhen", "How", "Why"})


def _has_sections(root: ElementTree.Element) -> set[str]:
    result = set()
    for child in root:
        local = child.tag.split("}")[-1] if "}" in child.tag else child.tag
        if local in _KEEP:
            result.add(local)
    return result


def test_all_alert_fixtures_have_standard_sections():
    """All fermi_gbm_alert fixtures must contain the standard VOE sections."""
    fixtures = sorted(p for p in (FIXTURES / "fermi_gbm_alert").iterdir() if p.suffix == ".xml")
    assert len(fixtures) >= 2

    for path in fixtures:
        sections = _has_sections(ElementTree.fromstring(path.read_bytes()))
        assert sections == _KEEP, f"{path.name} missing sections: {_KEEP - sections}"
