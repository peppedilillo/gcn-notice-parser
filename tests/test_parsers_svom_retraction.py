from datetime import datetime
from datetime import timezone
from pathlib import Path
from xml.etree import ElementTree

from gcnparser.svom import parse_svom_retraction
from gcnparser.svom import SvomRetraction

FIXTURE_GROUPS = [
    Path("tests/fixtures/svom/eclairs"),
    Path("tests/fixtures/svom/grm"),
    Path("tests/fixtures/svom/mxt"),
]


def _retraction_fixtures() -> list[Path]:
    fixtures = []
    for root in FIXTURE_GROUPS:
        for path in sorted(root.glob("*.xml")):
            xml_root = ElementTree.fromstring(path.read_bytes())
            packet_type = int(xml_root.find(".//What/Param[@name='Packet_Type']").get("value"))
            if packet_type == 219:
                fixtures.append(path)
    return fixtures


def test_parse_svom_retraction_from_eclairs_fixture():
    result = parse_svom_retraction(Path("tests/fixtures/svom/eclairs/eclairs_304.xml").read_bytes())

    assert result.ivorn == "ivo://org.svom/fsc#sb26030408_retraction"
    assert result.packet_type == 219
    assert result.notice_level == "N3e"
    assert result.burst_id == "sb26030408"
    assert result.alert_seq_t0 is None
    assert result.description == "Determined to not be a viable GRB candidate"
    assert result.reference_uri is None
    assert result.retractions == ("ivo://org.svom/fsc#sb26030408_eclairs-wakeup",)


def test_parse_svom_retraction_from_multi_target_fixture():
    result = parse_svom_retraction(Path("tests/fixtures/svom/grm/grm_286.xml").read_bytes())

    assert result.ivorn == "ivo://org.svom/fsc#sb26020402_retraction"
    assert result.packet_type == 219
    assert result.notice_level == "N3e"
    assert result.burst_id == "sb26020402"
    assert result.alert_datetime == datetime(2026, 2, 4, 12, 18, 14, tzinfo=timezone.utc)
    assert result.description == "Determined to not be a viable GRB candidate"
    assert result.reference_uri is None
    assert result.retractions == (
        "ivo://org.svom/fsc#sb26020402_grm-trigger",
        "ivo://org.svom/fsc#sb26020402_eclairs-preliminary",
        "ivo://org.svom/fsc#sb26020402_not-slewing",
    )


def test_parse_all_svom_retraction_fixtures():
    for path in _retraction_fixtures():
        result = parse_svom_retraction(path.read_bytes())
        assert isinstance(result, SvomRetraction)
