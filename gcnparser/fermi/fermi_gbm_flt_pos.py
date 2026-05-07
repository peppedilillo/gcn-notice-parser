from datetime import datetime
from enum import IntEnum
from typing import Annotated
from xml.etree import ElementTree as ET

from pydantic import BaseModel

from gcnparser.utils import attr as _attr
from gcnparser.utils import group_flag as _group_flag
from gcnparser.utils import group_param as _group_param
from gcnparser.utils import opt_text as _opt_text
from gcnparser.utils import param as _param
from gcnparser.utils import text as _text


class LikelySource(IntEnum):
    ERROR = 0
    UNRELIABLE_LOCATION = 1
    LOCAL_PARTICLES = 2
    BELOW_HORIZON = 3
    GRB = 4
    GENERIC_SGR = 5
    GENERIC_TRANSIENT = 6
    DISTANT_PARTICLES = 7
    SOLAR_FLARE = 8
    CYG_X1 = 9
    SGR_1806_20 = 10
    GROJ_0422_32 = 11
    UNDEFINED = 12
    TGF = 19


class FermiGBMFltPos(BaseModel):
    """Parsed Fermi-GBM flight position VOEvent notice (packet type 111).

    Attributes:
        author_contact_name: Contact name of the notice author.
        author_email: Email address of the notice author.
        alert_datetime: UTC datetime when the notice was issued (ISO-8601).
        packet_type: GCN packet type number (111 = Flt Pos, 117 = Flt Pos Internal).
        pkt_ser_num: Serial number for this packet type.
        trig_id: Unique trigger identifier; seconds since 2001-01-01.
        sequence_num: Record sequence number across all messages for this trigger.
        burst_datetime: UTC datetime of the trigger event (ISO-8601).
        burst_tjd: Truncated Julian Day of the trigger (days).
        burst_sod: Seconds of day of the trigger (s).
        burst_inten: Number of events in the trigger integration window (counts).
        trig_timescale: Binning of the countrate lightcurve used for trigger detection (s).
        data_timescale: Binning of the countrate lightcurve used for location calculation (s).
        data_signif: Significance of the ongoing integrated data (sigma).
        phi: GBM instrument azimuth of the burst (deg).
        theta: GBM instrument zenith of the burst measured from LAT boresight (deg).
        ra: Right ascension of the burst position (deg).
        dec: Declination of the burst position (deg).
        error_radius: Radius of the positional error circle (deg).
        sc_long: East geographic longitude of the spacecraft at trigger time (deg).
        sc_lat: Geographic latitude of the spacecraft at trigger time (deg).
        algorithm: Version index of the flight software location algorithm.
        most_likely_index: Class ID of the most likely source class (dn).
        most_likely_prob: Probability of the most likely source class (percent).
        sec_most_likely_index: Class ID of the second most likely source class (dn).
        sec_most_likely_prob: Probability of the second most likely source class (percent).
        hardness_ratio: Hardness ratio (15-50 keV / 50-300 keV).
        def_not_a_grb: Whether ground analysis determined this is definitely not a GRB.
        target_in_blk_catalog: Whether the source is in the blocked-source catalog.
        spatial_prox_match: Whether spatial coincidence was found with another event.
        temporal_prox_match: Whether temporal coincidence was found with another event.
        test_submission: Whether this is an internal test submission.
        values_out_of_range: Whether any coordinate values were out of valid range.
        delayed_transmission: Whether transmission of this notice was delayed.
        flt_generated: Whether the notice originated from flight software.
        gnd_generated: Whether the notice originated from ground operations.
        lightcurve_url: URL to the quicklook lightcurve GIF.
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
    packet_type: int
    pkt_ser_num: int
    trig_id: int
    sequence_num: int
    burst_datetime: Annotated[datetime, "ISO8601"]
    burst_tjd: Annotated[int, "days"]
    burst_sod: Annotated[float, "s"]
    burst_inten: Annotated[int, "counts"]
    trig_timescale: Annotated[float, "s"]
    data_timescale: Annotated[float, "s"]
    data_signif: Annotated[float, "sigma"]
    phi: Annotated[float, "deg"]
    theta: Annotated[float, "deg"]
    ra: Annotated[float, "deg"]
    dec: Annotated[float, "deg"]
    error_radius: Annotated[float, "deg"]
    sc_long: Annotated[float, "deg"]
    sc_lat: Annotated[float, "deg"]
    algorithm: int
    most_likely_index: LikelySource
    most_likely_prob: Annotated[int, "percent"]
    sec_most_likely_index: LikelySource
    sec_most_likely_prob: Annotated[int, "percent"]
    hardness_ratio: float
    def_not_a_grb: bool
    target_in_blk_catalog: bool
    spatial_prox_match: bool
    temporal_prox_match: bool
    test_submission: bool
    values_out_of_range: bool
    delayed_transmission: bool
    flt_generated: bool
    gnd_generated: bool
    lightcurve_url: str
    coords_type: Annotated[int, "dn"]
    coords_string: str
    reference_uri: str
    importance: float
    inference_probability: float
    followup: str | None = None


_WHO_RULES = {
    "author_contact_name": lambda r: _text(r, "Who/Author/contactName"),
    "author_email": lambda r: _text(r, "Who/Author/contactEmail"),
    "alert_datetime": lambda r: datetime.fromisoformat(_text(r, "Who/Date")),
}

_WHAT_RULES = {
    "packet_type": lambda r: int(_param(r, "Packet_Type")),
    "pkt_ser_num": lambda r: int(_param(r, "Pkt_Ser_Num")),
    "trig_id": lambda r: int(_param(r, "TrigID")),
    "sequence_num": lambda r: int(_param(r, "Sequence_Num")),
    "burst_tjd": lambda r: int(_param(r, "Burst_TJD")),
    "burst_sod": lambda r: float(_param(r, "Burst_SOD")),
    "burst_inten": lambda r: int(_param(r, "Burst_Inten")),
    "trig_timescale": lambda r: float(_param(r, "Trig_Timescale")),
    "data_timescale": lambda r: float(_param(r, "Data_Timescale")),
    "data_signif": lambda r: float(_param(r, "Data_Signif")),
    "phi": lambda r: float(_param(r, "Phi")),
    "theta": lambda r: float(_param(r, "Theta")),
    "sc_long": lambda r: float(_param(r, "SC_Long")),
    "sc_lat": lambda r: float(_param(r, "SC_Lat")),
    "algorithm": lambda r: int(_param(r, "Algorithm")),
    "most_likely_index": lambda r: LikelySource(int(_param(r, "Most_Likely_Index"))),
    "most_likely_prob": lambda r: int(_param(r, "Most_Likely_Prob")),
    "sec_most_likely_index": lambda r: LikelySource(int(_param(r, "Sec_Most_Likely_Index"))),
    "sec_most_likely_prob": lambda r: int(_param(r, "Sec_Most_Likely_Prob")),
    "hardness_ratio": lambda r: float(_param(r, "Hardness_Ratio")),
    "lightcurve_url": lambda r: _param(r, "LightCurve_URL"),
    "coords_type": lambda r: int(_param(r, "Coords_Type")),
    "coords_string": lambda r: _param(r, "Coords_String"),
    "def_not_a_grb": lambda r: _group_flag(r, "Trigger_ID", "Def_NOT_a_GRB"),
    "target_in_blk_catalog": lambda r: _group_flag(r, "Trigger_ID", "Target_in_Blk_Catalog"),
    "spatial_prox_match": lambda r: _group_flag(r, "Trigger_ID", "Spatial_Prox_Match"),
    "temporal_prox_match": lambda r: _group_flag(r, "Trigger_ID", "Temporal_Prox_Match"),
    "test_submission": lambda r: _group_flag(r, "Trigger_ID", "Test_Submission"),
    "values_out_of_range": lambda r: _group_flag(r, "Misc_Flags", "Values_Out_of_Range"),
    "delayed_transmission": lambda r: _group_flag(r, "Misc_Flags", "Delayed_Transmission"),
    "flt_generated": lambda r: _group_flag(r, "Misc_Flags", "Flt_Generated"),
    "gnd_generated": lambda r: _group_flag(r, "Misc_Flags", "Gnd_Generated"),
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


def parse_fermi_gbm_flt_pos(value: bytes) -> FermiGBMFltPos:
    """Parses a Fermi GBM flight position notice."""
    root = ET.fromstring(value)
    data = {}
    data.update(_parse_who(root))
    data.update(_parse_what(root))
    data.update(_parse_where_when(root))
    data.update(_parse_how(root))
    data.update(_parse_why(root))
    data.update(_parse_citations(root))
    return FermiGBMFltPos(**data)
