from datetime import datetime
from typing import Annotated
from xml.etree import ElementTree as ET

from pydantic import BaseModel

from gcnparser.utils import attr as _attr
from gcnparser.utils import group_flag as _group_flag
from gcnparser.utils import group_param as _group_param
from gcnparser.utils import opt_text as _opt_text
from gcnparser.utils import param as _param
from gcnparser.utils import text as _text


class FermiGBMFinPos(BaseModel):
    """Parsed Fermi-GBM final position VOEvent notice (packet type 115).

    Attributes:
        author_contact_name: Contact name of the notice author.
        author_email: Email address of the notice author.
        alert_datetime: UTC datetime when the notice was issued (ISO-8601).
        packet_type: GCN packet type number (115 = Fin Pos, 146 = Fin Pos Internal).
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
        algorithm: Version index of the location algorithm.
        lo_energy: Lower energy bound of the analysis range (keV).
        hi_energy: Upper energy bound of the analysis range (keV).
        def_not_a_grb: Whether ground analysis determined this is definitely not a GRB.
        target_in_blk_catalog: Whether the source is in the blocked-source catalog.
        human_generated: Whether the position was manually reviewed by a human.
        robo_generated: Whether the position was generated autonomously.
        long_short: Classification of the burst duration (``"long"``, ``"short"``, or ``"unknown"``).
        spatial_prox_match: Whether spatial coincidence was found with another event.
        temporal_prox_match: Whether temporal coincidence was found with another event.
        test_submission: Whether this is an internal test submission.
        values_out_of_range: Whether any coordinate values were out of valid range.
        flt_generated: Whether the notice originated from flight software.
        gnd_generated: Whether the notice originated from ground operations.
        crc_error: Whether a CRC error was detected.
        lightcurve_url: URL to the quicklook lightcurve GIF.
        locationmap_url: URL to the location plot PNG.
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
    def_not_a_grb: bool
    target_in_blk_catalog: bool
    human_generated: bool
    robo_generated: bool
    long_short: str
    spatial_prox_match: bool
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
    "sequence_num": lambda r: int(_param(r, "Sequence_Num")),
    "burst_tjd": lambda r: int(_param(r, "Burst_TJD")),
    "burst_sod": lambda r: float(_param(r, "Burst_SOD")),
    "burst_inten": lambda r: int(_param(r, "Burst_Inten")),
    "data_integ": lambda r: float(_param(r, "Data_Integ")),
    "burst_signif": lambda r: float(_param(r, "Burst_Signif")),
    "phi": lambda r: float(_param(r, "Phi")),
    "theta": lambda r: float(_param(r, "Theta")),
    "algorithm": lambda r: int(_param(r, "Algorithm")),
    "lo_energy": lambda r: int(_param(r, "Lo_Energy")),
    "hi_energy": lambda r: int(_param(r, "Hi_Energy")),
    "lightcurve_url": lambda r: _param(r, "LightCurve_URL"),
    "locationmap_url": lambda r: _param(r, "LocationMap_URL"),
    "coords_type": lambda r: int(_param(r, "Coords_Type")),
    "coords_string": lambda r: _param(r, "Coords_String"),
    "def_not_a_grb": lambda r: _group_flag(r, "Trigger_ID", "Def_NOT_a_GRB"),
    "target_in_blk_catalog": lambda r: _group_flag(r, "Trigger_ID", "Target_in_Blk_Catalog"),
    "human_generated": lambda r: _group_flag(r, "Trigger_ID", "Human_generated"),
    "robo_generated": lambda r: _group_flag(r, "Trigger_ID", "Robo_generated"),
    "long_short": lambda r: _group_param(r, "Trigger_ID", "Long_short") or "unknown",
    "spatial_prox_match": lambda r: _group_flag(r, "Trigger_ID", "Spatial_Prox_Match"),
    "temporal_prox_match": lambda r: _group_flag(r, "Trigger_ID", "Temporal_Prox_Match"),
    "test_submission": lambda r: _group_flag(r, "Trigger_ID", "Test_Submission"),
    "values_out_of_range": lambda r: _group_flag(r, "Misc_Flags", "Values_Out_of_Range"),
    "flt_generated": lambda r: _group_flag(r, "Misc_Flags", "Flt_Generated"),
    "gnd_generated": lambda r: _group_flag(r, "Misc_Flags", "Gnd_Generated"),
    "crc_error": lambda r: _group_flag(r, "Misc_Flags", "CRC_Error"),
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


def parse_fermi_gbm_fin_pos(value: bytes) -> FermiGBMFinPos:
    """Parses a Fermi GBM final position notice."""
    root = ET.fromstring(value)
    data = {}
    data.update(_parse_who(root))
    data.update(_parse_what(root))
    data.update(_parse_where_when(root))
    data.update(_parse_how(root))
    data.update(_parse_why(root))
    data.update(_parse_citations(root))
    return FermiGBMFinPos(**data)
