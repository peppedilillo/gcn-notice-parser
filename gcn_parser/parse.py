"""High-level parser dispatch for GCN Kafka messages."""

from typing import Protocol

from .ep import EinsteinProbeWXT
from .ep import parse_einstein_probe_wxt
from .exceptions import UnsupportedTopicError
from .fermi import FermiGBMAlert
from .fermi import FermiGBMFinPos
from .fermi import FermiGBMFltPos
from .fermi import FermiGBMGndPos
from .fermi import FermiLATOffline
from .fermi import FermiLATPosDiag
from .fermi import FermiLATPosIni
from .fermi import FermiLATPosUpd
from .fermi import parse_fermi_gbm_alert
from .fermi import parse_fermi_gbm_fin_pos
from .fermi import parse_fermi_gbm_flt_pos
from .fermi import parse_fermi_gbm_gnd_pos
from .fermi import parse_fermi_lat_offline
from .fermi import parse_fermi_lat_pos_diag
from .fermi import parse_fermi_lat_pos_ini
from .fermi import parse_fermi_lat_pos_upd
from .svom import is_svom_retraction
from .svom import parse_svom_eclairs
from .svom import parse_svom_grm_trigger
from .svom import parse_svom_mxt
from .svom import parse_svom_retraction
from .svom import SvomEclairs
from .svom import SvomGrm
from .svom import SvomMxt
from .svom import SvomRetraction
from .topics import Topic


class Message(Protocol):
    """Kafka-style message protocol accepted by :func:`parse`."""

    def topic(self) -> str: ...
    def value(self) -> bytes: ...


Notice = (
    FermiGBMAlert
    | FermiGBMFinPos
    | FermiGBMFltPos
    | FermiGBMGndPos
    | FermiLATOffline
    | FermiLATPosDiag
    | FermiLATPosIni
    | FermiLATPosUpd
    | SvomRetraction
    | SvomMxt
    | SvomEclairs
    | SvomGrm
    | EinsteinProbeWXT
)


def parse(msg: Message) -> Notice:
    """Parse a supported GCN Kafka message.

    Args:
        msg: Kafka-style message object with ``topic()`` and ``value()``
            methods. ``topic()`` must return the GCN topic string, and
            ``value()`` must return the raw notice bytes.

    Returns:
        Parsed notice model for the message topic.

    Raises:
        UnsupportedTopicError: If the message topic is not supported.
        ParseError: If the topic-specific parser cannot parse or validate the
            message payload.
        FieldParseError: If a topic-specific parser cannot extract a required
            field from the message payload.
    """
    match msg.topic():
        case Topic.FERMI_GBM_ALERT:
            return parse_fermi_gbm_alert(msg.value())
        case Topic.FERMI_GBM_FIN_POS:
            return parse_fermi_gbm_fin_pos(msg.value())
        case Topic.FERMI_GBM_FLT_POS:
            return parse_fermi_gbm_flt_pos(msg.value())
        case Topic.FERMI_GBM_GND_POS:
            return parse_fermi_gbm_gnd_pos(msg.value())
        case Topic.FERMI_LAT_OFFLINE:
            return parse_fermi_lat_offline(msg.value())
        case Topic.FERMI_LAT_POS_DIAG:
            return parse_fermi_lat_pos_diag(msg.value())
        case Topic.FERMI_LAT_POS_INI:
            return parse_fermi_lat_pos_ini(msg.value())
        case Topic.FERMI_LAT_POS_UPD:
            return parse_fermi_lat_pos_upd(msg.value())
        case Topic.EINSTEIN_PROBE_WXT_ALERT:
            return parse_einstein_probe_wxt(msg.value())
        case Topic.SVOM_ECLAIRS:
            if is_svom_retraction(msg.value()):
                return parse_svom_retraction(msg.value())
            return parse_svom_eclairs(msg.value())
        case Topic.SVOM_GRM:
            if is_svom_retraction(msg.value()):
                return parse_svom_retraction(msg.value())
            return parse_svom_grm_trigger(msg.value())
        case Topic.SVOM_MXT:
            if is_svom_retraction(msg.value()):
                return parse_svom_retraction(msg.value())
            return parse_svom_mxt(msg.value())
        case _:
            raise UnsupportedTopicError(f"Unsupported topic: {msg.topic()}")
