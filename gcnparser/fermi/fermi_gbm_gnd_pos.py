from datetime import datetime
from typing import Annotated

from pydantic import BaseModel

from gcnparser.parse_xml import attr
from gcnparser.parse_xml import group_flag
from gcnparser.parse_xml import group_param
from gcnparser.parse_xml import opt_text
from gcnparser.parse_xml import param
from gcnparser.parse_xml import parse_voevent_notice
from gcnparser.parse_xml import root_attr
from gcnparser.parse_xml import text


class FermiGBMGndPos(BaseModel):
    """Parsed Fermi-GBM ground position VOEvent notice (packet type 112).

    Attributes:
        author_contact_name: Contact name of the notice author.
        author_email: Email address of the notice author.
        alert_datetime: UTC datetime when the notice was issued (ISO-8601).
        ivorn: Raw VOEvent IVORN identifying this notice instance.
        packet_type: GCN packet type number (112 = Gnd Pos).
        pkt_ser_num: Serial number for this packet type.
        trig_id: Unique trigger identifier; seconds since 2001-01-01.
        sequence_num: Record sequence number across all messages for this trigger.
        burst_datetime: UTC datetime of the trigger event (ISO-8601).
        burst_tjd: Truncated Julian Day of the trigger (days).
        burst_sod: Seconds of day of the trigger (s).
        burst_inten: Number of events in the trigger integration window (counts).
        data_integ: Duration of the trigger integration interval (s).
        burst_signif: Significance of the burst in the integrated data (sigma).
        phi: GBM instrument azimuth of the burst (deg).
        theta: GBM instrument zenith of the burst measured from LAT boresight (deg).
        ra: Right ascension of the burst position (deg).
        dec: Declination of the burst position (deg).
        error_radius: Radius of the positional error circle (deg).
        algorithm: Version index of the ground location algorithm.
        lo_energy: Lower energy bound of the analysis range (keV).
        hi_energy: Upper energy bound of the analysis range (keV).
        sc_geo_x: Spacecraft geocentric X-coordinate (*4 km).
        sc_geo_y: Spacecraft geocentric Y-coordinate (*4 km).
        sc_geo_z: Spacecraft geocentric Z-coordinate (*4 km).
        def_not_a_grb: Whether ground analysis determined this is definitely not a GRB.
        target_in_blk_catalog: Whether the source is in the blocked-source catalog.
        spatial_prox_match: Whether spatial coincidence was found with another event.
        long_short: Classification of the burst duration (``"long"``, ``"short"``, or ``"unknown"``).
        temporal_prox_match: Whether temporal coincidence was found with another event.
        test_submission: Whether this is an internal test submission.
        values_out_of_range: Whether any coordinate values were out of valid range.
        flt_generated: Whether the notice originated from flight software.
        gnd_generated: Whether the notice originated from ground operations.
        crc_error: Whether a CRC error was detected.
        lightcurve_url: URL to the quicklook lightcurve GIF.
        locationmap_url: URL to the ground location FITS map.
        coords_type: Coordinate type code (dn).
        coords_string: Human-readable description of the coordinate type.
        reference_uri: URL to the Fermi GBM instrument documentation.
        followup: IVORN of the parent notice that this notice updates (if any).
        importance: VOEvent importance rating.
        inference_probability: VOEvent inference probability.
    """

    author_contact_name: str
    author_email: str
    alert_datetime: Annotated[datetime, "ISO8601"]
    ivorn: str
    packet_type: int
    pkt_ser_num: int
    trig_id: int
    sequence_num: int
    burst_datetime: Annotated[datetime, "ISO8601"]
    burst_tjd: Annotated[int, "days"]
    burst_sod: Annotated[float, "s"]
    burst_inten: Annotated[int, "counts"]
    data_integ: Annotated[float, "s"]
    burst_signif: Annotated[float, "sigma"]
    phi: Annotated[float, "deg"]
    theta: Annotated[float, "deg"]
    ra: Annotated[float, "deg"]
    dec: Annotated[float, "deg"]
    error_radius: Annotated[float, "deg"]
    algorithm: int
    lo_energy: Annotated[int, "keV"]
    hi_energy: Annotated[int, "keV"]
    sc_geo_x: int
    sc_geo_y: int
    sc_geo_z: int
    def_not_a_grb: bool
    target_in_blk_catalog: bool
    spatial_prox_match: bool
    long_short: str
    temporal_prox_match: bool
    test_submission: bool
    values_out_of_range: bool
    flt_generated: bool
    gnd_generated: bool
    crc_error: bool
    lightcurve_url: str
    locationmap_url: str
    coords_type: Annotated[int, "dn"]
    coords_string: str
    reference_uri: str
    importance: float
    inference_probability: float
    followup: str | None = None


_ROOT_RULES = {
    "ivorn": lambda r: root_attr(r, "ivorn"),
}

_WHO_RULES = {
    "author_contact_name": lambda r: text(r, "Who/Author/contactName"),
    "author_email": lambda r: text(r, "Who/Author/contactEmail"),
    "alert_datetime": lambda r: datetime.fromisoformat(text(r, "Who/Date")),
}

_WHAT_RULES = {
    "packet_type": lambda r: int(param(r, "Packet_Type")),
    "pkt_ser_num": lambda r: int(param(r, "Pkt_Ser_Num")),
    "trig_id": lambda r: int(param(r, "TrigID")),
    "sequence_num": lambda r: int(param(r, "Sequence_Num")),
    "burst_tjd": lambda r: int(param(r, "Burst_TJD")),
    "burst_sod": lambda r: float(param(r, "Burst_SOD")),
    "burst_inten": lambda r: int(param(r, "Burst_Inten")),
    "data_integ": lambda r: float(param(r, "Data_Integ")),
    "burst_signif": lambda r: float(param(r, "Burst_Signif")),
    "phi": lambda r: float(param(r, "Phi")),
    "theta": lambda r: float(param(r, "Theta")),
    "algorithm": lambda r: int(param(r, "Algorithm")),
    "lo_energy": lambda r: int(param(r, "Lo_Energy")),
    "hi_energy": lambda r: int(param(r, "Hi_Energy")),
    "sc_geo_x": lambda r: int(param(r, "SC_Geo_X")),
    "sc_geo_y": lambda r: int(param(r, "SC_Geo_Y")),
    "sc_geo_z": lambda r: int(param(r, "SC_Geo_Z")),
    "lightcurve_url": lambda r: param(r, "LightCurve_URL"),
    "locationmap_url": lambda r: param(r, "LocationMap_URL"),
    "coords_type": lambda r: int(param(r, "Coords_Type")),
    "coords_string": lambda r: param(r, "Coords_String"),
    "def_not_a_grb": lambda r: group_flag(r, "Trigger_ID", "Def_NOT_a_GRB"),
    "target_in_blk_catalog": lambda r: group_flag(r, "Trigger_ID", "Target_in_Blk_Catalog"),
    "spatial_prox_match": lambda r: group_flag(r, "Trigger_ID", "Spatial_Prox_Match"),
    "long_short": lambda r: group_param(r, "Trigger_ID", "Long_short"),
    "temporal_prox_match": lambda r: group_flag(r, "Trigger_ID", "Temporal_Prox_Match"),
    "test_submission": lambda r: group_flag(r, "Trigger_ID", "Test_Submission"),
    "values_out_of_range": lambda r: group_flag(r, "Misc_Flags", "Values_Out_of_Range"),
    "flt_generated": lambda r: group_flag(r, "Misc_Flags", "Flt_Generated"),
    "gnd_generated": lambda r: group_flag(r, "Misc_Flags", "Gnd_Generated"),
    "crc_error": lambda r: group_flag(r, "Misc_Flags", "CRC_Error"),
}

_WHEREWHEN_RULES = {
    "burst_datetime": lambda r: datetime.fromisoformat(
        text(r, "WhereWhen/ObsDataLocation/ObservationLocation/AstroCoords/Time/TimeInstant/ISOTime")
    ),
    "ra": lambda r: float(text(r, "WhereWhen/ObsDataLocation/ObservationLocation/AstroCoords/Position2D/Value2/C1")),
    "dec": lambda r: float(text(r, "WhereWhen/ObsDataLocation/ObservationLocation/AstroCoords/Position2D/Value2/C2")),
    "error_radius": lambda r: float(
        text(r, "WhereWhen/ObsDataLocation/ObservationLocation/AstroCoords/Position2D/Error2Radius")
    ),
}

_HOW_RULES = {
    "reference_uri": lambda r: attr(r, "How/Reference", "uri"),
}

_WHY_RULES = {
    "importance": lambda r: float(attr(r, "Why", "importance")),
    "inference_probability": lambda r: float(attr(r, "Why/Inference", "probability")),
}

_CITATIONS_RULES = {
    "followup": lambda r: opt_text(r, "Citations/EventIVORN[@cite='followup']"),
}


def parse_fermi_gbm_gnd_pos(value: bytes) -> FermiGBMGndPos:
    """Parses a Fermi GBM ground position notice.

    Args:
        value: Raw XML bytes of the VOEvent notice.

    Returns:
        Parsed GBM ground position notice model.

    Raises:
        ParseError: If the XML document cannot be parsed or model validation
            fails.
        FieldParseError: If a specific field cannot be extracted from the
            notice.
    """
    return parse_voevent_notice(
        value,
        FermiGBMGndPos,
        "parse_fermi_gbm_gnd_pos",
        {
            "VOEvent": _ROOT_RULES,
            "Who": _WHO_RULES,
            "What": _WHAT_RULES,
            "WhereWhen": _WHEREWHEN_RULES,
            "How": _HOW_RULES,
            "Why": _WHY_RULES,
            "Citations": _CITATIONS_RULES,
        },
    )
