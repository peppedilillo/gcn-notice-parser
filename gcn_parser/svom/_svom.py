"""Internal SVOM helpers."""

from enum import IntEnum


class SvomPacket(IntEnum):
    """SVOM ECLAIRs notice packet type identifiers.
    See `https://fsc.svom.org/readthedocs/svom/notices_and_circulars/notice_levels.html`

    We implement a specific type because notices with different packe type (and schema)
    may be streamed from the same topic.
    """

    GRM_TRIGGER = 201
    ECLAIR_WAKEUP = 202
    ECLAIR_CATALOG = 203
    ECLAIR_SLEWING = 204
    ECLAIR_NOT_SLEWING = 205
    MXT_INITIAL = 209
    MXT_UPDATE = 210
    VT_CANDIDATE = 211
    RETRACTION = 219
