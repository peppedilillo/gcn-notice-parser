from dataclasses import dataclass
from pathlib import Path

import pytest

from gcnparser.ep import EinsteinProbeWXT
from gcnparser.exceptions import ParseError
from gcnparser.exceptions import UnsupportedTopicError
from gcnparser.parse import parse
from gcnparser.svom import is_svom_retraction
from gcnparser.svom import SvomEclairs
from gcnparser.svom import SvomRetraction
from gcnparser.topics import Topic


@dataclass
class Message:
    topic: Topic | str
    value: bytes


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
