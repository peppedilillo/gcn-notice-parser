"""Parser for SVOM MXT notices."""

from datetime import datetime
from typing import Annotated

from pydantic import BaseModel

from ..parse_xml import attr
from ..parse_xml import citations
from ..parse_xml import group_param
from ..parse_xml import param
from ..parse_xml import parse_utc_datetime
from ..parse_xml import parse_voevent_notice
from ..parse_xml import root_attr
from ..parse_xml import text
from ..svom import SvomPacket


def parse_bool(value: str) -> bool:
    return value.lower() == "true"


class SvomMxt(BaseModel):
    """Parsed SVOM MXT notice.

    Covers both packet-209 initial notices and packet-210 update notices.
    The raw VOEvent identity is preserved in ``ivorn``.
    """

    author_contact_name: str
    author_email: str
    alert_datetime: Annotated[datetime, "ISO8601"]
    ivorn: str
    packet_type: SvomPacket
    pkt_ser_num: int
    instrument: str
    notice_level: str
    burst_id: str
    alert_seq_t0: Annotated[datetime | None, "ISO8601"] = None
    snr: Annotated[float, "sigma"]
    mean_flux: float
    flux_error: float
    within_eclairs_r90: bool
    eclairs_angle: Annotated[float, "arcmin"]
    galactic_lon: Annotated[float, "deg"]
    galactic_lat: Annotated[float, "deg"]
    moon_angle: Annotated[float, "deg"]
    sun_angle: Annotated[float, "deg"]
    use_vt_attitude: bool
    attitude_ra: Annotated[float, "deg"]
    attitude_dec: Annotated[float, "deg"]
    attitude_roll: Annotated[float, "deg"]
    sat_longitude: Annotated[float, "deg"]
    sat_latitude: Annotated[float, "deg"]
    sat_altitude: Annotated[float, "km"]
    burst_datetime: Annotated[datetime, "ISO8601"]
    ra: Annotated[float, "deg"]
    dec: Annotated[float, "deg"]
    error_radius: Annotated[float, "deg"]
    description: str
    reference_uri: str
    followups: tuple[str, ...]


_ROOT_RULES = {
    "ivorn": lambda r: root_attr(r, "ivorn"),
}

_WHO_RULES = {
    "author_contact_name": lambda r: text(r, "Who/Author/contactName"),
    "author_email": lambda r: text(r, "Who/Author/contactEmail"),
    "alert_datetime": lambda r: parse_utc_datetime(text(r, "Who/Date")),
}

_WHAT_RULES = {
    "packet_type": lambda r: SvomPacket(int(param(r, "Packet_Type"))),
    "pkt_ser_num": lambda r: int(param(r, "Pkt_Ser_Num")),
    "instrument": lambda r: param(r, "Instrument"),
    "notice_level": lambda r: group_param(r, "Svom_Identifiers", "Notice_Level"),
    "burst_id": lambda r: group_param(r, "Svom_Identifiers", "Burst_Id"),
    "alert_seq_t0": lambda r: (
        parse_utc_datetime(group_param(r, "Svom_Identifiers", "Alert_Seq_T0"))
        if group_param(r, "Svom_Identifiers", "Alert_Seq_T0") is not None
        else None
    ),
    "snr": lambda r: float(group_param(r, "Detection_Info", "SNR")),
    "mean_flux": lambda r: float(group_param(r, "Detection_Info", "Mean_Flux")),
    "flux_error": lambda r: float(group_param(r, "Detection_Info", "Flux_Error")),
    "within_eclairs_r90": lambda r: parse_bool(group_param(r, "Target_Info", "Within_ECLAIRs_R90")),
    "eclairs_angle": lambda r: float(group_param(r, "Target_Info", "ECLAIRs_Angle")),
    "galactic_lon": lambda r: float(group_param(r, "Target_Info", "Galactic_Lon")),
    "galactic_lat": lambda r: float(group_param(r, "Target_Info", "Galactic_Lat")),
    "moon_angle": lambda r: float(group_param(r, "Target_Info", "Moon_Angle")),
    "sun_angle": lambda r: float(group_param(r, "Target_Info", "Sun_Angle")),
    "use_vt_attitude": lambda r: parse_bool(group_param(r, "Satellite_Info", "Use_VT_Attitude")),
    "attitude_ra": lambda r: float(group_param(r, "Satellite_Info", "Attitude_Ra")),
    "attitude_dec": lambda r: float(group_param(r, "Satellite_Info", "Attitude_Dec")),
    "attitude_roll": lambda r: float(group_param(r, "Satellite_Info", "Attitude_Roll")),
    "sat_longitude": lambda r: float(group_param(r, "Satellite_Info", "Sat_Longitude")),
    "sat_latitude": lambda r: float(group_param(r, "Satellite_Info", "Sat_Latitude")),
    "sat_altitude": lambda r: float(group_param(r, "Satellite_Info", "Sat_Altitude")),
}

_WHEREWHEN_RULES = {
    "burst_datetime": lambda r: parse_utc_datetime(
        text(r, "WhereWhen/ObsDataLocation/ObservationLocation/AstroCoords/Time/TimeInstant/ISOTime")
    ),
    "ra": lambda r: float(text(r, "WhereWhen/ObsDataLocation/ObservationLocation/AstroCoords/Position2D/Value2/C1")),
    "dec": lambda r: float(text(r, "WhereWhen/ObsDataLocation/ObservationLocation/AstroCoords/Position2D/Value2/C2")),
    "error_radius": lambda r: float(
        text(r, "WhereWhen/ObsDataLocation/ObservationLocation/AstroCoords/Position2D/Error2Radius")
    ),
}

_HOW_RULES = {
    "description": lambda r: text(r, "How/Description"),
    "reference_uri": lambda r: attr(r, "How/Reference", "uri"),
}

_CITATIONS_RULES = {
    "followups": lambda r: citations(r, "followup"),
}


def parse_svom_mxt(value: bytes) -> SvomMxt:
    """Parses an SVOM MXT notice.

    Args:
        value: Raw XML bytes of the VOEvent notice.

    Returns:
        Parsed MXT notice model.

    Raises:
        ParseError: If the XML document cannot be parsed or model validation
            fails.
        FieldParseError: If a specific field cannot be extracted from the
            notice.
    """
    return parse_voevent_notice(
        value,
        SvomMxt,
        "parse_svom_mxt",
        {
            "VOEvent": _ROOT_RULES,
            "Who": _WHO_RULES,
            "What": _WHAT_RULES,
            "WhereWhen": _WHEREWHEN_RULES,
            "How": _HOW_RULES,
            "Citations": _CITATIONS_RULES,
        },
    )
