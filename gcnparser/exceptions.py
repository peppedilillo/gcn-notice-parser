class ParseError(Exception):
    pass


class FieldParseError(ParseError):
    pass


class UnsupportedTopicError(Exception):
    pass
