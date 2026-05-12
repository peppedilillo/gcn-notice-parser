from datetime import datetime
from typing import Annotated

from pydantic import BaseModel

from gcnparser.parse_xml import attr
from gcnparser.parse_xml import citations
from gcnparser.parse_xml import description
from gcnparser.parse_xml import group_param
from gcnparser.parse_xml import opt_group_datetime
from gcnparser.parse_xml import opt_group_float
from gcnparser.parse_xml import param
from gcnparser.parse_xml import parse_utc_datetime
from gcnparser.parse_xml import parse_voevent_notice
from gcnparser.parse_xml import root_attr
from gcnparser.parse_xml import text
from gcnparser.svom import SvomPacketType


class SvomEclairsNotice(BaseModel):
    """Parsed SVOM ECLAIRs VOEvent notice (N1e).

    Covers all ECLAIRs notice types: wake-up (202), catalog trigger (203),
    slewing (204), and not-slewing (205). The specific notice type is
    identified by ``packet_type``.

    Attributes:
        author_contact_name: Contact name of the notice author.
        author_email: Email address of the notice author.
        alert_datetime: UTC datetime when the notice was issued (ISO-8601).
        ivorn: Raw VOEvent IVORN identifying this notice instance.
        packet_type: ECLAIRs notice type identifier.
        pkt_ser_num: Serial number for this packet type.
        instrument: Instrument involved (``"ECLAIRs"``).
        notice_level: SVOM notice level (``"N1e"``).
        burst_id: Identifier of the alert sequence (``sbYYMMDDnn``).
        snr: Signal-to-noise ratio in the reconstructed ECLAIRs image (sigma).
        timescale: Time window in which the burst was detected (s).
        time_window_start: Start time of the detection time window (ISO-8601).
        time_window_end: End time of the detection time window (ISO-8601).
        lower_energy_bound: Lower energy bound of the detection range (keV).
        upper_energy_bound: Upper energy bound of the detection range (keV).
        trigger_type: Type of trigger (``"CRT"`` for count-rate trigger or
            ``"IMT"`` for image trigger).
        galactic_lon: Galactic longitude of the target (deg).
        galactic_lat: Galactic latitude of the target (deg).
        moon_angle: Angular distance between the target and the Moon (deg).
        sun_angle: Angular distance between the target and the Sun (deg).
        slew_status: Slew status of the SVOM platform.
        attitude_ra: Platform attitude Right Ascension (deg).
        attitude_dec: Platform attitude Declination (deg).
        attitude_roll: Platform attitude Roll angle (deg).
        sat_longitude: Satellite geodetic longitude (deg).
        sat_latitude: Satellite geodetic latitude (deg).
        sat_altitude: Satellite altitude (km).
        burst_datetime: UTC time of the trigger event (ISO-8601).
        ra: Right Ascension of the detection (deg).
        dec: Declination of the detection (deg).
        error_radius: R90 uncertainty radius of the localisation (deg).
        description: Description of the notice.
        reference_uri: URL to the ECLAIRs instrument description.
        alert_seq_t0: Time of the alert sequence T0 (ISO-8601). ``None`` for
            basic wake-up and catalog notices.
        onboard_catalog_id: Identifier of the source in the ECLAIRs on-board
            catalogue. ``None`` for non-catalog notices.
        source_name: Name of the source in the ECLAIRs on-board catalogue.
            ``None`` for non-catalog notices.
        followups: IVORNs of previously published notices for the same event.
    """

    author_contact_name: str
    author_email: str
    alert_datetime: Annotated[datetime, "ISO8601"]
    ivorn: str
    packet_type: SvomPacketType
    pkt_ser_num: int
    instrument: str
    notice_level: str
    burst_id: str
    snr: Annotated[float, "sigma"]
    timescale: Annotated[float, "s"]
    time_window_start: Annotated[datetime, "ISO8601"]
    time_window_end: Annotated[datetime, "ISO8601"]
    lower_energy_bound: Annotated[int, "keV"]
    upper_energy_bound: Annotated[int, "keV"]
    trigger_type: str
    galactic_lon: Annotated[float, "deg"]
    galactic_lat: Annotated[float, "deg"]
    moon_angle: Annotated[float, "deg"]
    sun_angle: Annotated[float, "deg"]
    slew_status: str
    attitude_ra: Annotated[float, "deg"]
    attitude_dec: Annotated[float, "deg"]
    attitude_roll: Annotated[float, "deg"]
    sat_longitude: Annotated[float | None, "deg"]
    sat_latitude: Annotated[float | None, "deg"]
    sat_altitude: Annotated[float | None, "km"]
    burst_datetime: Annotated[datetime, "ISO8601"]
    ra: Annotated[float, "deg"]
    dec: Annotated[float, "deg"]
    error_radius: Annotated[float, "deg"]
    description: str | None
    reference_uri: str | None
    alert_seq_t0: Annotated[datetime | None, "ISO8601"] = None
    onboard_catalog_id: int | None = None
    source_name: str | None = None
    followups: tuple[str, ...] = ()


_ROOT_RULES = {
    "ivorn": lambda r: root_attr(r, "ivorn"),
}

_WHO_RULES = {
    "author_contact_name": lambda r: text(r, "Who/Author/contactName"),
    "author_email": lambda r: text(r, "Who/Author/contactEmail"),
    "alert_datetime": lambda r: parse_utc_datetime(text(r, "Who/Date")),
}

_WHAT_RULES = {
    "packet_type": lambda r: SvomPacketType(int(param(r, "Packet_Type"))),
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
    "galactic_lon": lambda r: float(group_param(r, "Target_Info", "Galactic_Lon")),
    "galactic_lat": lambda r: float(group_param(r, "Target_Info", "Galactic_Lat")),
    "moon_angle": lambda r: float(group_param(r, "Target_Info", "Moon_Angle")),
    "sun_angle": lambda r: float(group_param(r, "Target_Info", "Sun_Angle")),
    "slew_status": lambda r: group_param(r, "Satellite_Info", "Slew_Status"),
    "attitude_ra": lambda r: float(group_param(r, "Satellite_Info", "Attitude_Ra")),
    "attitude_dec": lambda r: float(group_param(r, "Satellite_Info", "Attitude_Dec")),
    "attitude_roll": lambda r: float(group_param(r, "Satellite_Info", "Attitude_Roll")),
    "sat_longitude": lambda r: opt_group_float(r, "Satellite_Info", "Sat_Longitude"),
    "sat_latitude": lambda r: opt_group_float(r, "Satellite_Info", "Sat_Latitude"),
    "sat_altitude": lambda r: opt_group_float(r, "Satellite_Info", "Sat_Altitude"),
    "onboard_catalog_id": lambda r: (
        int(group_param(r, "Target_Info", "Onboard_Catalog_Id"))
        if group_param(r, "Target_Info", "Onboard_Catalog_Id") is not None
        else None
    ),
    "source_name": lambda r: group_param(r, "Target_Info", "Source_Name"),
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
    "description": description,
    "reference_uri": lambda r: attr(r, "How/Reference", "uri"),
}

_CITATIONS_RULES = {
    "followups": lambda r: citations(r, "followup"),
}


def parse_svom_eclairs(value: bytes) -> SvomEclairsNotice:
    """Parses an SVOM ECLAIRs VOEvent notice.

    Args:
        value: Raw XML bytes of the VOEvent notice.

    Returns:
        Parsed ECLAIRs notice model.

    Raises:
        ParseError: If the XML document cannot be parsed, the
            ``Packet_Type`` is not a known ECLAIRs notice type, or model
            validation fails.
        FieldParseError: If a specific field cannot be extracted from the
            notice.
    """
    return parse_voevent_notice(
        value,
        SvomEclairsNotice,
        "parse_svom_eclairs",
        {
            "VOEvent": _ROOT_RULES,
            "Who": _WHO_RULES,
            "What": _WHAT_RULES,
            "WhereWhen": _WHEREWHEN_RULES,
            "How": _HOW_RULES,
            "Citations": _CITATIONS_RULES,
        },
    )
