from datetime import datetime
from typing import Annotated
from xml.etree import ElementTree as ET

from pydantic import BaseModel

from gcnparser.utils import attr as _attr
from gcnparser.utils import group_flag as _group_flag
from gcnparser.utils import opt_text as _opt_text
from gcnparser.utils import param as _param
from gcnparser.utils import text as _text


class FermiLATPos(BaseModel):
    """Shared model for Fermi-LAT position notices (packet types 120, 121, 122).

    Attributes:
        author_contact_name: Contact name of the notice author.
        author_email: Email address of the notice author.
        alert_datetime: UTC datetime when the notice was issued (ISO-8601).
        packet_type: GCN packet type number.
        pkt_ser_num: Serial number for this packet type.
        trig_id: Unique trigger identifier; seconds since 2001-01-01.
        record_num: Record sequence number across all messages for this trigger.
        burst_datetime: UTC datetime of the trigger event (ISO-8601).
        burst_tjd: Truncated Julian Day of the trigger (days).
        burst_sod: Seconds of day of the trigger (s).
        burst_inten: Number of events used in the location calculation (counts).
        cnts_e1: Event counts in the 0--100 MeV energy band (counts).
        cnts_e2: Event counts in the 100 MeV--1 GeV energy band (counts).
        cnts_e3: Event counts in the 1--10 GeV energy band (counts).
        cnts_e4: Event counts in the >10 GeV energy band (counts).
        integ_time: Integration time between first and last photons used (s).
        trig_index: Index of the trigger criterion that provided the successful trigger (dn).
        temp_test_stat: Temporal test statistic (``-log`` probability).
        image_test_stat: Image test statistic (``-log`` probability).
        ra: Right ascension of the burst position (deg).
        dec: Declination of the burst position (deg).
        error_radius: Radius of the positional error circle (deg).
        all_gammas_used: Whether all gammas were used in the location method.
        only_gammas_above_used: Whether only gammas above an energy cut were used.
        def_not_a_grb: Whether ground analysis determined this is definitely not a GRB.
        spatial_prox_match: Whether spatial coincidence was found with another event.
        temporal_prox_match: Whether temporal coincidence was found with another event.
        report_request_made: Whether a repoint request was made to the spacecraft.
        values_out_of_range: Whether any coordinate values were out of valid range.
        near_bright_star: Whether the position is near a bright star (mag < 6.5).
        err_circle_in_galaxy: Whether the error circle overlaps the Galactic plane.
        galaxy_in_err_circle: Whether the Galactic plane lies within the error circle.
        coords_type: Coordinate type code (dn).
        coords_string: Human-readable description of the coordinate type.
        reference_uri: URL to the Fermi LAT instrument documentation.
        followup: IVORN of the parent notice that this notice updates (if any).
        importance: VOEvent importance rating.
        inference_probability: VOEvent inference probability.
    """

    author_contact_name: str
    author_email: str
    alert_datetime: Annotated[datetime, "ISO8601"]
    packet_type: int
    pkt_ser_num: int
    trig_id: int
    record_num: int
    burst_datetime: Annotated[datetime, "ISO8601"]
    burst_tjd: Annotated[int, "days"]
    burst_sod: Annotated[float, "s"]
    burst_inten: Annotated[int, "counts"]
    cnts_e1: Annotated[int, "counts"]
    cnts_e2: Annotated[int, "counts"]
    cnts_e3: Annotated[int, "counts"]
    cnts_e4: Annotated[int, "counts"]
    integ_time: Annotated[float, "s"]
    trig_index: Annotated[int, "dn"]
    temp_test_stat: Annotated[float, "-log(prob)"]
    image_test_stat: Annotated[float, "-log(prob)"]
    ra: Annotated[float, "deg"]
    dec: Annotated[float, "deg"]
    error_radius: Annotated[float, "deg"]
    all_gammas_used: bool
    only_gammas_above_used: bool
    def_not_a_grb: bool
    spatial_prox_match: bool
    temporal_prox_match: bool
    report_request_made: bool
    values_out_of_range: bool
    near_bright_star: bool
    err_circle_in_galaxy: bool
    galaxy_in_err_circle: bool
    coords_type: Annotated[int, "dn"]
    coords_string: str
    reference_uri: str
    followup: str | None = None
    importance: float
    inference_probability: float


_WHO_RULES = {
    "author_contact_name": lambda r: _text(r, "Who/Author/contactName"),
    "author_email": lambda r: _text(r, "Who/Author/contactEmail"),
    "alert_datetime": lambda r: datetime.fromisoformat(_text(r, "Who/Date")),
}

_WHAT_RULES = {
    "packet_type": lambda r: int(_param(r, "Packet_Type")),
    "pkt_ser_num": lambda r: int(_param(r, "Pkt_Ser_Num")),
    "trig_id": lambda r: int(_param(r, "TrigID")),
    "record_num": lambda r: int(_param(r, "Record_Num")),
    "burst_tjd": lambda r: int(_param(r, "Burst_TJD")),
    "burst_sod": lambda r: float(_param(r, "Burst_SOD")),
    "burst_inten": lambda r: int(_param(r, "Burst_Inten")),
    "cnts_e1": lambda r: int(_param(r, "Cnts_E1")),
    "cnts_e2": lambda r: int(_param(r, "Cnts_E2")),
    "cnts_e3": lambda r: int(_param(r, "Cnts_E3")),
    "cnts_e4": lambda r: int(_param(r, "Cnts_E4")),
    "integ_time": lambda r: float(_param(r, "Integ_Time")),
    "trig_index": lambda r: int(_param(r, "Trig_Index")),
    "temp_test_stat": lambda r: float(_param(r, "Temp_Test_Stat")),
    "image_test_stat": lambda r: float(_param(r, "Image_Test_Stat")),
    "coords_type": lambda r: int(_param(r, "Coords_Type")),
    "coords_string": lambda r: _param(r, "Coords_String"),
    "all_gammas_used": lambda r: _group_flag(r, "Trigger_ID", "All_Gammas_Used"),
    "only_gammas_above_used": lambda r: _group_flag(r, "Trigger_ID", "Only_Gammas_Above_Used"),
    "def_not_a_grb": lambda r: _group_flag(r, "Trigger_ID", "Def_NOT_a_GRB"),
    "spatial_prox_match": lambda r: _group_flag(r, "Trigger_ID", "Spatial_Prox_Match"),
    "temporal_prox_match": lambda r: _group_flag(r, "Trigger_ID", "Temporal_Prox_Match"),
    "report_request_made": lambda r: _group_flag(r, "Misc_Flags", "Report_Request_Made"),
    "values_out_of_range": lambda r: _group_flag(r, "Misc_Flags", "Values_Out_of_Range"),
    "near_bright_star": lambda r: _group_flag(r, "Misc_Flags", "Near_Bright_Star"),
    "err_circle_in_galaxy": lambda r: _group_flag(r, "Misc_Flags", "Err_Circle_in_Galaxy"),
    "galaxy_in_err_circle": lambda r: _group_flag(r, "Misc_Flags", "Galaxy_in_Err_Circle"),
}

_WHEREWHEN_RULES = {
    "burst_datetime": lambda r: datetime.fromisoformat(
        _text(r, "WhereWhen/ObsDataLocation/ObservationLocation/AstroCoords/Time/TimeInstant/ISOTime")
    ),
    "ra": lambda r: float(_text(r, "WhereWhen/ObsDataLocation/ObservationLocation/AstroCoords/Position2D/Value2/C1")),
    "dec": lambda r: float(_text(r, "WhereWhen/ObsDataLocation/ObservationLocation/AstroCoords/Position2D/Value2/C2")),
    "error_radius": lambda r: float(
        _text(r, "WhereWhen/ObsDataLocation/ObservationLocation/AstroCoords/Position2D/Error2Radius")
    ),
}

_HOW_RULES = {
    "reference_uri": lambda r: _attr(r, "How/Reference", "uri"),
}

_WHY_RULES = {
    "importance": lambda r: float(_attr(r, "Why", "importance")),
    "inference_probability": lambda r: float(_attr(r, "Why/Inference", "probability")),
}

_CITATIONS_RULES = {
    "followup": lambda r: _opt_text(r, "Citations/EventIVORN[@cite='followup']"),
}


def _parse_who(root: ET.Element) -> dict:
    return {k: v(root) for k, v in _WHO_RULES.items()}


def _parse_what(root: ET.Element) -> dict:
    return {k: v(root) for k, v in _WHAT_RULES.items()}


def _parse_where_when(root: ET.Element) -> dict:
    return {k: v(root) for k, v in _WHEREWHEN_RULES.items()}


def _parse_how(root: ET.Element) -> dict:
    return {k: v(root) for k, v in _HOW_RULES.items()}


def _parse_why(root: ET.Element) -> dict:
    return {k: v(root) for k, v in _WHY_RULES.items()}


def _parse_citations(root: ET.Element) -> dict:
    return {k: v(root) for k, v in _CITATIONS_RULES.items()}


def parse_fermi_lat_pos(value: bytes) -> FermiLATPos:
    """Parses a Fermi-LAT position notice."""
    root = ET.fromstring(value)
    data = {}
    data.update(_parse_who(root))
    data.update(_parse_what(root))
    data.update(_parse_where_when(root))
    data.update(_parse_how(root))
    data.update(_parse_why(root))
    data.update(_parse_citations(root))
    return FermiLATPos(**data)
