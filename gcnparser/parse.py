from gcnparser.ep import EinsteinProbeWXT
from gcnparser.ep import parse_einstein_probe_wxt
from gcnparser.exceptions import UnsupportedTopicError
from gcnparser.fermi import FermiGBMAlert
from gcnparser.fermi import FermiGBMFinPos
from gcnparser.fermi import FermiGBMFltPos
from gcnparser.fermi import FermiGBMGndPos
from gcnparser.fermi import FermiLATOffline
from gcnparser.fermi import FermiLATPosDiag
from gcnparser.fermi import FermiLATPosIni
from gcnparser.fermi import FermiLATPosUpd
from gcnparser.fermi import parse_fermi_gbm_alert
from gcnparser.fermi import parse_fermi_gbm_fin_pos
from gcnparser.fermi import parse_fermi_gbm_flt_pos
from gcnparser.fermi import parse_fermi_gbm_gnd_pos
from gcnparser.fermi import parse_fermi_lat_offline
from gcnparser.fermi import parse_fermi_lat_pos_diag
from gcnparser.fermi import parse_fermi_lat_pos_ini
from gcnparser.fermi import parse_fermi_lat_pos_upd
from gcnparser.svom import is_svom_retraction
from gcnparser.svom import parse_svom_eclairs
from gcnparser.svom import parse_svom_grm_trigger
from gcnparser.svom import parse_svom_mxt
from gcnparser.svom import parse_svom_retraction
from gcnparser.svom import SvomEclairs
from gcnparser.svom import SvomGrm
from gcnparser.svom import SvomMxt
from gcnparser.svom import SvomRetraction
from gcnparser.topics import Topic


class Message:
    topic: Topic
    value: bytes


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
    match msg.topic:
        case Topic.FERMI_GBM_ALERT:
            return parse_fermi_gbm_alert(msg.value)
        case Topic.FERMI_GBM_FIN_POS:
            return parse_fermi_gbm_fin_pos(msg.value)
        case Topic.FERMI_GBM_FLT_POS:
            return parse_fermi_gbm_flt_pos(msg.value)
        case Topic.FERMI_GBM_GND_POS:
            return parse_fermi_gbm_gnd_pos(msg.value)
        case Topic.FERMI_LAT_OFFLINE:
            return parse_fermi_lat_offline(msg.value)
        case Topic.FERMI_LAT_POS_DIAG:
            return parse_fermi_lat_pos_diag(msg.value)
        case Topic.FERMI_LAT_POS_INI:
            return parse_fermi_lat_pos_ini(msg.value)
        case Topic.FERMI_LAT_POS_UPD:
            return parse_fermi_lat_pos_upd(msg.value)
        case Topic.EINSTEIN_PROBE_WXT_ALERT:
            return parse_einstein_probe_wxt(msg.value)
        case Topic.SVOM_ECLAIRS:
            if is_svom_retraction(msg.value):
                return parse_svom_retraction(msg.value)
            return parse_svom_eclairs(msg.value)
        case Topic.SVOM_GRM:
            if is_svom_retraction(msg.value):
                return parse_svom_retraction(msg.value)
            return parse_svom_grm_trigger(msg.value)
        case Topic.SVOM_MXT:
            if is_svom_retraction(msg.value):
                return parse_svom_retraction(msg.value)
            return parse_svom_mxt(msg.value)
        case _:
            raise UnsupportedTopicError(f"Unsupported topic: {msg.topic}")
