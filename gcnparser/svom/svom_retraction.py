from datetime import datetime
from typing import Annotated

from pydantic import BaseModel

from gcnparser.parse_xml import attr
from gcnparser.parse_xml import group_param
from gcnparser.parse_xml import param
from gcnparser.parse_xml import parse_notice
from gcnparser.parse_xml import root_attr
from gcnparser.parse_xml import text
from gcnparser.svom._svom_xml import citations
from gcnparser.svom._svom_xml import description
from gcnparser.svom._svom_xml import opt_group_datetime
from gcnparser.svom._svom_xml import opt_group_float
from gcnparser.svom._svom_xml import opt_position_float
from gcnparser.svom._svom_xml import parse_datetime


class SvomRetraction(BaseModel):
    """Parsed generic SVOM packet-219 retraction notice.

    Retractions are modeled as their own document shape and preserve the raw
    cited IVORNs in ``retractions``.
    """

    author_contact_name: str
    author_email: str
    alert_datetime: Annotated[datetime, "ISO8601"]
    ivorn: str
    packet_type: int
    pkt_ser_num: int
    instrument: str
    notice_level: str
    burst_id: str
    alert_seq_t0: Annotated[datetime | None, "ISO8601"] = None
    snr: Annotated[float, "sigma"]
    timescale: Annotated[float, "s"]
    time_window_start: Annotated[datetime, "ISO8601"]
    time_window_end: Annotated[datetime, "ISO8601"]
    lower_energy_bound: Annotated[int, "keV"]
    upper_energy_bound: Annotated[int, "keV"]
    trigger_type: str | None = None
    galactic_lon: Annotated[float | None, "deg"] = None
    galactic_lat: Annotated[float | None, "deg"] = None
    moon_angle: Annotated[float | None, "deg"] = None
    sun_angle: Annotated[float | None, "deg"] = None
    slew_status: str | None = None
    attitude_ra: Annotated[float, "deg"]
    attitude_dec: Annotated[float, "deg"]
    attitude_roll: Annotated[float, "deg"]
    sat_longitude: Annotated[float | None, "deg"] = None
    sat_latitude: Annotated[float | None, "deg"] = None
    sat_altitude: Annotated[float | None, "km"] = None
    burst_datetime: Annotated[datetime, "ISO8601"]
    ra: Annotated[float | None, "deg"] = None
    dec: Annotated[float | None, "deg"] = None
    error_radius: Annotated[float | None, "deg"] = None
    description: str | None = None
    reference_uri: str | None = None
    retractions: tuple[str, ...]


_ROOT_RULES = {
    "ivorn": lambda r: root_attr(r, "ivorn"),
}

_WHO_RULES = {
    "author_contact_name": lambda r: text(r, "Who/Author/contactName"),
    "author_email": lambda r: text(r, "Who/Author/contactEmail"),
    "alert_datetime": lambda r: parse_datetime(text(r, "Who/Date")),
}

_WHAT_RULES = {
    "packet_type": lambda r: int(param(r, "Packet_Type")),
    "pkt_ser_num": lambda r: int(param(r, "Pkt_Ser_Num")),
    "instrument": lambda r: param(r, "Instrument"),
    "notice_level": lambda r: group_param(r, "Svom_Identifiers", "Notice_Level"),
    "burst_id": lambda r: group_param(r, "Svom_Identifiers", "Burst_Id"),
    "alert_seq_t0": lambda r: opt_group_datetime(r, "Svom_Identifiers", "Alert_Seq_T0"),
    "snr": lambda r: float(group_param(r, "Detection_Info", "SNR")),
    "timescale": lambda r: float(group_param(r, "Detection_Info", "Timescale")),
    "time_window_start": lambda r: parse_datetime(group_param(r, "Detection_Info", "Time_Window_Start")),
    "time_window_end": lambda r: parse_datetime(group_param(r, "Detection_Info", "Time_Window_End")),
    "lower_energy_bound": lambda r: int(group_param(r, "Detection_Info", "Lower_Energy_Bound")),
    "upper_energy_bound": lambda r: int(group_param(r, "Detection_Info", "Upper_Energy_Bound")),
    "trigger_type": lambda r: group_param(r, "Detection_Info", "Trigger_Type"),
    "galactic_lon": lambda r: opt_group_float(r, "Target_Info", "Galactic_Lon"),
    "galactic_lat": lambda r: opt_group_float(r, "Target_Info", "Galactic_Lat"),
    "moon_angle": lambda r: opt_group_float(r, "Target_Info", "Moon_Angle"),
    "sun_angle": lambda r: opt_group_float(r, "Target_Info", "Sun_Angle"),
    "slew_status": lambda r: group_param(r, "Satellite_Info", "Slew_Status"),
    "attitude_ra": lambda r: float(group_param(r, "Satellite_Info", "Attitude_Ra")),
    "attitude_dec": lambda r: float(group_param(r, "Satellite_Info", "Attitude_Dec")),
    "attitude_roll": lambda r: float(group_param(r, "Satellite_Info", "Attitude_Roll")),
    "sat_longitude": lambda r: opt_group_float(r, "Satellite_Info", "Sat_Longitude"),
    "sat_latitude": lambda r: opt_group_float(r, "Satellite_Info", "Sat_Latitude"),
    "sat_altitude": lambda r: opt_group_float(r, "Satellite_Info", "Sat_Altitude"),
}

_WHEREWHEN_RULES = {
    "burst_datetime": lambda r: datetime.fromisoformat(
        text(r, "WhereWhen/ObsDataLocation/ObservationLocation/AstroCoords/Time/TimeInstant/ISOTime")
    ),
    "ra": lambda r: opt_position_float(
        r, "WhereWhen/ObsDataLocation/ObservationLocation/AstroCoords/Position2D/Value2/C1"
    ),
    "dec": lambda r: opt_position_float(
        r, "WhereWhen/ObsDataLocation/ObservationLocation/AstroCoords/Position2D/Value2/C2"
    ),
    "error_radius": lambda r: opt_position_float(
        r, "WhereWhen/ObsDataLocation/ObservationLocation/AstroCoords/Position2D/Error2Radius"
    ),
}

_HOW_RULES = {
    "description": description,
    "reference_uri": lambda r: attr(r, "How/Reference", "uri") if r.find("How/Reference") is not None else None,
}

_CITATIONS_RULES = {
    "retractions": lambda r: citations(r, "retraction"),
}


def parse_svom_retraction(value: bytes) -> SvomRetraction:
    """Parses a generic SVOM retraction notice.

    Args:
        value: Raw XML bytes of the VOEvent notice.

    Returns:
        Parsed retraction notice model.

    Raises:
        ParseError: If the XML document cannot be parsed or model validation
            fails.
        FieldParseError: If a specific field cannot be extracted from the
            notice.
    """
    return parse_notice(
        value,
        SvomRetraction,
        "parse_svom_retraction",
        {
            "VOEvent": _ROOT_RULES,
            "Who": _WHO_RULES,
            "What": _WHAT_RULES,
            "WhereWhen": _WHEREWHEN_RULES,
            "How": _HOW_RULES,
            "Citations": _CITATIONS_RULES,
        },
    )
