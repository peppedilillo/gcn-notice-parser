"""GCN notice parsers."""

from . import ep
from . import fermi
from . import svom
from .parse import parse
from .parse import Topic as _Topic

SUPPORTED_TOPICS = [t.value for t in _Topic]
