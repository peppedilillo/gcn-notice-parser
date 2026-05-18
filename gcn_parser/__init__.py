"""GCN notice parsers."""

from . import ep
from . import fermi
from . import svom
from .exceptions import FieldParseError
from .exceptions import ParseError
from .exceptions import UnsupportedTopicError
from .parse import parse
from .parse import Topic

SUPPORTED_TOPICS: list[Topic] = [t for t in Topic]
