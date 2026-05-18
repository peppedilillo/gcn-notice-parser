from enum import StrEnum


class Topic(StrEnum):
    """GCN Kafka topics for which parsing is supported."""

    FERMI_GBM_ALERT: str = "gcn.classic.voevent.FERMI_GBM_ALERT"
    FERMI_GBM_FIN_POS: str = "gcn.classic.voevent.FERMI_GBM_FIN_POS"
    FERMI_GBM_FLT_POS: str = "gcn.classic.voevent.FERMI_GBM_FLT_POS"
    FERMI_GBM_GND_POS: str = "gcn.classic.voevent.FERMI_GBM_GND_POS"
    FERMI_LAT_OFFLINE: str = "gcn.classic.voevent.FERMI_LAT_OFFLINE"
    FERMI_LAT_POS_DIAG: str = "gcn.classic.voevent.FERMI_LAT_POS_DIAG"
    FERMI_LAT_POS_INI: str = "gcn.classic.voevent.FERMI_LAT_POS_INI"
    FERMI_LAT_POS_UPD: str = "gcn.classic.voevent.FERMI_LAT_POS_UPD"

    SVOM_GRM: str = "gcn.notices.svom.voevent.grm"
    SVOM_ECLAIRS: str = "gcn.notices.svom.voevent.eclairs"
    SVOM_MXT: str = "gcn.notices.svom.voevent.mxt"

    EINSTEIN_PROBE_WXT_ALERT: str = "gcn.notices.einstein_probe.wxt.alert"
