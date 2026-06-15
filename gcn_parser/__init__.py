"""GCN notice parsers."""

from . import ep
from . import fermi
from . import svom
from .exceptions import FieldParseError
from .exceptions import ParseError
from .exceptions import UnsupportedTopicError
from .parse import parse
from .parse import Topic
from .parse import Notice


def supported_topics() -> list[Topic]:
    """Return a list of GCN Kafka supported topics.

    Returns:
        List of supported topic enum members. The returned list can be passed
            directly to Kafka consumers that accept string-like topic values.
    """
    return list(Topic)


SUPPORTED_TOPICS: list[Topic] = supported_topics()
