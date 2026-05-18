"""Exception types raised by GCN notice parsers."""


class ParseError(Exception):
    """Raised when a notice cannot be parsed or validated."""

    pass


class FieldParseError(ParseError):
    """Raised when a parser cannot extract a specific notice field."""

    pass


class UnsupportedTopicError(Exception):
    """Raised for unsupported GCN topics."""

    pass
