from pathlib import Path

import pytest

from gcn_parser.ep import EinsteinProbeWXT
from gcn_parser.exceptions import ParseError
from gcn_parser.exceptions import UnsupportedTopicError
from gcn_parser.parse import parse
from gcn_parser.svom import is_svom_retraction
from gcn_parser.svom import SvomEclairs
from gcn_parser.svom import SvomRetraction
from gcn_parser.topics import Topic


class Message:
    def __init__(self, topic: Topic | str, value: bytes) -> None:
        self._topic = topic
        self._value = value

    def topic(self) -> Topic | str:
        return self._topic

    def value(self) -> bytes:
        return self._value


def test_is_svom_retraction_true_for_retraction_fixture():
    payload = Path("tests/fixtures/svom/eclairs/eclairs_304.xml").read_bytes()

    assert is_svom_retraction(payload) is True


def test_is_svom_retraction_false_for_non_retraction_fixture():
    payload = Path("tests/fixtures/svom/eclairs/eclairs_296.xml").read_bytes()

    assert is_svom_retraction(payload) is False


def test_is_svom_retraction_wraps_malformed_xml():
    with pytest.raises(ParseError) as exc_info:
        is_svom_retraction(b"<VOEvent")

    assert "is_svom_retraction: failed to parse document" in str(exc_info.value)


def test_parse_dispatches_svom_eclairs_notice():
    msg = Message(Topic.SVOM_ECLAIRS, Path("tests/fixtures/svom/eclairs/eclairs_296.xml").read_bytes())

    result = parse(msg)

    assert isinstance(result, SvomEclairs)


def test_parse_dispatches_svom_retraction_notice():
    msg = Message(Topic.SVOM_ECLAIRS, Path("tests/fixtures/svom/eclairs/eclairs_304.xml").read_bytes())

    result = parse(msg)

    assert isinstance(result, SvomRetraction)


def test_parse_dispatches_non_svom_notice():
    msg = Message(Topic.EINSTEIN_PROBE_WXT_ALERT, Path("tests/fixtures/ep/alert/alert_247.json").read_bytes())

    result = parse(msg)

    assert isinstance(result, EinsteinProbeWXT)


def test_parse_raises_for_unsupported_topic():
    msg = Message("unsupported.topic", b"{}")

    with pytest.raises(UnsupportedTopicError):
        parse(msg)
