"""Parser for SVOM GRM trigger notices."""

from datetime import datetime
from typing import Annotated

from pydantic import BaseModel

from ..parse_xml import attr
from ..parse_xml import group_param
from ..parse_xml import opt_group_datetime
from ..parse_xml import opt_group_float
from ..parse_xml import opt_position_float
from ..parse_xml import param
from ..parse_xml import parse_utc_datetime
from ..parse_xml import parse_voevent_notice
from ..parse_xml import root_attr
from ..parse_xml import text
from ..svom import SvomPacket


class SvomGrm(BaseModel):
    """Parsed SVOM GRM trigger notice (N1g, Packet_Type=201).

    Issued when at least 2 out of the 3 Gamma-Ray Detectors (GRDs) are
    triggered. If only 2 GRDs trigger, only the trigger time is provided
    and no localisation or target fields are available (ra, dec,
    error_radius, galactic targets are ``None``). With all 3 GRDs,
    localisation is provided but the error radius is set to -1 (not
    computable on-board).

    Attributes:
        author_contact_name: Contact name of the notice author.
        author_email: Email address of the notice author.
        alert_datetime: UTC datetime when the notice was issued (ISO-8601).
        ivorn: Raw VOEvent IVORN identifying this notice instance.
        packet_type: GCN packet type identifier (201 for GRM trigger).
        pkt_ser_num: Serial number for this packet type.
        instrument: Instrument involved (``"GRM"``).
        notice_level: SVOM notice level (``"N1g"``).
        burst_id: Identifier of the alert sequence (``sbYYMMDDnn``).
        alert_seq_t0: Time of the alert sequence T0 (ISO-8601).
        snr: Signal-to-noise ratio of the detection (sigma).
        timescale: Time window in which the burst was detected (s).
        time_window_start: Start time of the detection time window (ISO-8601).
        time_window_end: End time of the detection time window (ISO-8601).
        lower_energy_bound: Lower energy bound of the detection range (keV).
        upper_energy_bound: Upper energy bound of the detection range (keV).
        triggered_grds: Trigger status of the 3 GRDs (e.g. ``"111"``,
            ``"110"``, ``"101"``, ``"011"``). Each digit corresponds to one
            GRD; 1 means triggered, 0 means not.
        galactic_lon: Galactic longitude of the target (deg). ``None`` when
            only 2 GRDs trigger.
        galactic_lat: Galactic latitude of the target (deg). ``None`` when
            only 2 GRDs trigger.
        moon_angle: Angular distance between the target and the Moon (deg).
            ``None`` when only 2 GRDs trigger.
        sun_angle: Angular distance between the target and the Sun (deg).
            ``None`` when only 2 GRDs trigger.
        attitude_ra: Platform attitude Right Ascension (deg).
        attitude_dec: Platform attitude Declination (deg).
        attitude_roll: Platform attitude Roll angle (deg).
        sat_longitude: Satellite geodetic longitude (deg).
        sat_latitude: Satellite geodetic latitude (deg).
        sat_altitude: Satellite altitude (km).
        burst_datetime: UTC time of the trigger event (ISO-8601).
        ra: Right Ascension of the detection (deg). ``None`` when only 2
            GRDs trigger.
        dec: Declination of the detection (deg). ``None`` when only 2 GRDs
            trigger.
        error_radius: R90 uncertainty radius (deg). Set to -1 when all 3
            GRDs trigger but no error can be computed; ``None`` when only 2
            GRDs trigger.
        description: Description of the notice.
        reference_uri: URL to the GRM instrument description.
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
    lower_energy_bound: Annotated[float, "keV"]
    upper_energy_bound: Annotated[float, "keV"]
    triggered_grds: str
    galactic_lon: Annotated[float | None, "deg"] = None
    galactic_lat: Annotated[float | None, "deg"] = None
    moon_angle: Annotated[float | None, "deg"] = None
    sun_angle: Annotated[float | None, "deg"] = None
    attitude_ra: Annotated[float, "deg"]
    attitude_dec: Annotated[float, "deg"]
    attitude_roll: Annotated[float, "deg"]
    sat_longitude: Annotated[float, "deg"]
    sat_latitude: Annotated[float, "deg"]
    sat_altitude: Annotated[float, "km"]
    burst_datetime: Annotated[datetime, "ISO8601"]
    ra: Annotated[float | None, "deg"] = None
    dec: Annotated[float | None, "deg"] = None
    error_radius: Annotated[float | None, "deg"] = None
    description: str
    reference_uri: str


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
    "lower_energy_bound": lambda r: float(group_param(r, "Detection_Info", "Lower_Energy_Bound")),
    "upper_energy_bound": lambda r: float(group_param(r, "Detection_Info", "Upper_Energy_Bound")),
    "triggered_grds": lambda r: group_param(r, "Detection_Info", "Triggered_GRDs"),
    "galactic_lon": lambda r: opt_group_float(r, "Target_Info", "Galactic_Lon"),
    "galactic_lat": lambda r: opt_group_float(r, "Target_Info", "Galactic_Lat"),
    "moon_angle": lambda r: opt_group_float(r, "Target_Info", "Moon_Angle"),
    "sun_angle": lambda r: opt_group_float(r, "Target_Info", "Sun_Angle"),
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
    "description": lambda r: text(r, "How/Description"),
    "reference_uri": lambda r: attr(r, "How/Reference", "uri"),
}


def parse_svom_grm_trigger(value: bytes) -> SvomGrm:
    """Parses an SVOM GRM trigger notice.

    Args:
        value: Raw XML bytes of the VOEvent notice.

    Returns:
        Parsed GRM trigger notice model.

    Raises:
        ParseError: If the XML document cannot be parsed or model validation
            fails.
        FieldParseError: If a specific field cannot be extracted from the
            notice.
    """
    return parse_voevent_notice(
        value,
        SvomGrm,
        "parse_svom_grm_trigger",
        {
            "VOEvent": _ROOT_RULES,
            "Who": _WHO_RULES,
            "What": _WHAT_RULES,
            "WhereWhen": _WHEREWHEN_RULES,
            "How": _HOW_RULES,
        },
    )
