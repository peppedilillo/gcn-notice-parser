"""Internal SVOM helpers."""

from enum import IntEnum


# we have a dedicated type packets because, for SVOM, structurally different
# notices may arrive from the same topic.
class SvomPacket(IntEnum):
    """SVOM ECLAIRs notice packet type identifiers."""

    GRM_TRIGGER = 201
    ECLAIR_WAKEUP = 202
    ECLAIR_CATALOG = 203
    ECLAIR_SLEWING = 204
    ECLAIR_NOT_SLEWING = 205
    MXT_INITIAL = 209
    MXT_UPDATE = 210
    VT_CANDIDATE = 211
    RETRACTION = 219
