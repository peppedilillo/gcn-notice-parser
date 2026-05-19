"""Parser for generic SVOM retraction notices."""

from datetime import datetime
from typing import Annotated

from pydantic import BaseModel

from . import SvomPacket
from ..parse_xml import attr
from ..parse_xml import citations
from ..parse_xml import description
from ..parse_xml import group_param
from ..parse_xml import opt_group_datetime
from ..parse_xml import opt_group_float
from ..parse_xml import opt_position_float
from ..parse_xml import param
from ..parse_xml import parse_utc_datetime
from ..parse_xml import parse_voevent_notice
from ..parse_xml import parse_voevent_root
from ..parse_xml import root_attr
from ..parse_xml import text


class SvomRetraction(BaseModel):
    """Parsed generic SVOM packet-219 retraction notice.

    Retractions are modeled as their own document shape and preserve the raw
    cited IVORNs in ``retractions``.

    Attributes:
        author_contact_name: Contact name of the notice author.
        author_email: Email address of the notice author.
        alert_datetime: UTC datetime when the retraction notice was issued
            (ISO-8601).
        ivorn: Raw VOEvent IVORN identifying this retraction notice instance.
        packet_type: SVOM retraction notice type identifier (219).
        pkt_ser_num: Serial number for this packet type.
        instrument: Instrument associated with the retracted alert sequence.
        notice_level: SVOM notice level for the retraction.
        burst_id: Identifier of the alert sequence (``sbYYMMDDnn``).
        alert_seq_t0: Time of the alert sequence T0 (ISO-8601). ``None``
            when absent from the notice.
        snr: Signal-to-noise ratio of the original detection (sigma).
        timescale: Time window in which the original burst was detected (s).
        time_window_start: Start time of the original detection time window
            (ISO-8601).
        time_window_end: End time of the original detection time window
            (ISO-8601).
        lower_energy_bound: Lower energy bound of the original detection
            range (keV).
        upper_energy_bound: Upper energy bound of the original detection
            range (keV).
        trigger_type: Type of original ECLAIRs trigger, when present.
        galactic_lon: Galactic longitude of the retracted target (deg).
            ``None`` when absent from the notice.
        galactic_lat: Galactic latitude of the retracted target (deg).
            ``None`` when absent from the notice.
        moon_angle: Angular distance between the target and the Moon (deg).
            ``None`` when absent from the notice.
        sun_angle: Angular distance between the target and the Sun (deg).
            ``None`` when absent from the notice.
        slew_status: Slew status of the SVOM platform, when present.
        attitude_ra: Platform attitude Right Ascension (deg).
        attitude_dec: Platform attitude Declination (deg).
        attitude_roll: Platform attitude Roll angle (deg).
        sat_longitude: Satellite geodetic longitude (deg). ``None`` when
            absent from the notice.
        sat_latitude: Satellite geodetic latitude (deg). ``None`` when absent
            from the notice.
        sat_altitude: Satellite altitude (km). ``None`` when absent from the
            notice.
        burst_datetime: UTC time of the original trigger event (ISO-8601).
        ra: Right Ascension of the retracted localisation (deg). ``None``
            when no localisation is provided.
        dec: Declination of the retracted localisation (deg). ``None`` when
            no localisation is provided.
        error_radius: R90 uncertainty radius of the retracted localisation
            (deg). ``None`` when no localisation is provided.
        description: Human-readable reason for the retraction.
        reference_uri: URL to the instrument description. ``None`` when the
            retraction notice does not include a reference.
        retractions: IVORNs of previously published notices retracted by this
            notice.

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
    "alert_datetime": lambda r: parse_utc_datetime(text(r, "Who/Date")),
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
    "time_window_start": lambda r: parse_utc_datetime(group_param(r, "Detection_Info", "Time_Window_Start")),
    "time_window_end": lambda r: parse_utc_datetime(group_param(r, "Detection_Info", "Time_Window_End")),
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
    "burst_datetime": lambda r: parse_utc_datetime(
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


def is_svom_retraction(value: bytes) -> bool:
    """Checks whether the notice is a SVOM retraction.

    Args:
        value: Raw XML bytes of the VOEvent notice.

    Returns:
        True if the notice is a SVOM retraction.
    """
    root = parse_voevent_root(value, "is_svom_retraction")
    return int(param(root, "Packet_Type")) == SvomPacket.RETRACTION


def parse_svom_retraction(value: bytes) -> SvomRetraction:
    """Parses a generic SVOM retraction notice from bytes.

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
    return parse_voevent_notice(
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
