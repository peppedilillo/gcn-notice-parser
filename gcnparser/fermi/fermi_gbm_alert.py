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


class FermiGBMAlert(BaseModel):
    """Parsed Fermi-GBM VOEvent alert notice.

    Attributes:
        author_contact_name: Contact name of the notice author.
        author_email: Email address of the notice author.
        alert_datetime: UTC datetime when the notice was issued (ISO-8601).
        packet_type: GCN packet type number (110 = GBM Alert, 116 = GBM Alert Internal).
        pkt_ser_num: Serial number for this packet type.
        trig_id: Unique trigger identifier; seconds since 2001-01-01.
        sequence_num: Record sequence number across all messages for this trigger.
        burst_datetime: UTC datetime of the trigger event (ISO-8601).
        burst_tjd: Truncated Julian Day of the trigger (days).
        burst_sod: Seconds of day of the trigger (s).
        trig_signif: Significance of the trigger (sigma).
        trig_dur: Trigger integration interval duration (s).
        lo_chan_index: Lower energy channel index (dn).
        hi_chan_index: Upper energy channel index (dn).
        lo_chan_energy: Lower energy channel bound (keV).
        hi_chan_energy: Upper energy channel bound; ``None`` for open-ended range (keV).
        adc_lo_chan: Lower ADC channel (dn).
        adc_hi_chan: Upper ADC channel (dn).
        algorithm: Index identifying the location-calculation algorithm.
        dets: Names of the triggering detectors (0..9, A, B, BGO1, BGO2).
        sc_long: East geographic longitude of the spacecraft at trigger time (deg).
        sc_lat: Geographic latitude of the spacecraft at trigger time (deg).
        lightcurve_url: URL to the quicklook lightcurve GIF.
        coords_type: Coordinate type code (dn).
        coords_string: Human-readable description of the coordinate type.
        importance: VOEvent importance rating.
        inference_probability: VOEvent inference probability.
        values_out_of_range: Whether parameter values exceeded the valid range.
        near_bright_star: Whether the location is near a bright star.
        err_circle_in_galaxy: Whether the error circle overlaps the Galactic plane.
        galaxy_in_err_circle: Whether the Galactic plane lies within the error circle.
        too_generated: Whether a Target of Opportunity was generated.
        trig_time_is_sec_hdr_time: Whether trigger time equals the secondary header time.
        delayed_transmission: Whether transmission of this notice was delayed.
        updated_notice: Whether this notice updates a previous notice.
        flt_generated: Whether the notice originated from flight software.
        gnd_generated: Whether the notice originated from ground operations.
        temporal_prox_match: Whether temporal coincidence was found with another event.
        crc_error: Whether a CRC error was detected.
        reference_uri: URL to the Fermi GBM instrument documentation.
        followup: IVORN of the parent notice that this notice updates (if any).
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
    trig_signif: Annotated[float, "sigma"]
    trig_dur: Annotated[float, "s"]
    lo_chan_index: Annotated[int, "dn"]
    hi_chan_index: Annotated[int, "dn"]
    lo_chan_energy: Annotated[int, "keV"]
    hi_chan_energy: Annotated[int | None, "keV"]
    adc_lo_chan: Annotated[int, "dn"]
    adc_hi_chan: Annotated[int, "dn"]
    algorithm: int
    dets: tuple[str, ...]
    sc_long: Annotated[float, "deg"]
    sc_lat: Annotated[float, "deg"]
    lightcurve_url: str
    coords_type: Annotated[int, "dn"]
    coords_string: str
    importance: float
    inference_probability: float
    values_out_of_range: bool
    near_bright_star: bool
    err_circle_in_galaxy: bool
    galaxy_in_err_circle: bool
    too_generated: bool
    trig_time_is_sec_hdr_time: bool
    delayed_transmission: bool
    updated_notice: bool
    flt_generated: bool
    gnd_generated: bool
    temporal_prox_match: bool
    crc_error: bool
    reference_uri: str
    followup: str | None = None


_WHO_RULES = {
    "author_contact_name": lambda r: _text(r, "Who/Author/contactName"),
    "author_email": lambda r: _text(r, "Who/Author/contactEmail"),
    "alert_datetime": lambda r: datetime.fromisoformat(_text(r, "Who/Date")),
}


_DET_NAMES = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "BGO1", "BGO2")


def _parse_dets(value: str) -> tuple[str, ...]:
    """Parses detector bitmask according to Fermi-GBM socket packet definition:

      [26] The "det" contains which two of the 14 detectors that resulted in this event.
      There are 12 position-determining detectors and 2 spectrum-measuring detectors (BGO).
      The packing sequence starts with Det0 in the 2^0 bit, Det1 in 2^1, ..., DetB in 2^11,
      and the two BGO dets in 2^12 and 2^13.

    From `https://gcn.gsfc.nasa.gov/sock_pkt_def_doc.html`.
    """
    mask = int(value, 16)
    return tuple(name for i, name in enumerate(_DET_NAMES) if mask & (1 << i))


_WHAT_RULES = {
    "packet_type": lambda r: int(_param(r, "Packet_Type")),
    "pkt_ser_num": lambda r: int(_param(r, "Pkt_Ser_Num")),
    "trig_id": lambda r: int(_param(r, "TrigID")),
    "sequence_num": lambda r: int(_param(r, "Sequence_Num")),
    "burst_tjd": lambda r: int(_param(r, "Burst_TJD")),
    "burst_sod": lambda r: float(_param(r, "Burst_SOD")),
    "trig_signif": lambda r: float(_param(r, "Trig_Signif")),
    "trig_dur": lambda r: float(_param(r, "Trig_Dur")),
    "lo_chan_index": lambda r: int(_param(r, "Lo_Chan_Index")),
    "hi_chan_index": lambda r: int(_param(r, "Hi_Chan_Index")),
    "lo_chan_energy": lambda r: int(_param(r, "Lo_Chan_Energy")),
    "hi_chan_energy": lambda r: None if _param(r, "Hi_Chan_Energy") == "infinity" else int(_param(r, "Hi_Chan_Energy")),
    "adc_lo_chan": lambda r: int(_param(r, "ADC_Lo_Chan")),
    "adc_hi_chan": lambda r: int(_param(r, "ADC_Hi_Chan")),
    "algorithm": lambda r: int(_param(r, "Algorithm")),
    "dets": lambda r: _parse_dets(_param(r, "Dets")),
    "sc_long": lambda r: float(_param(r, "SC_Long")),
    "sc_lat": lambda r: float(_param(r, "SC_Lat")),
    "lightcurve_url": lambda r: _param(r, "LightCurve_URL"),
    "coords_type": lambda r: int(_param(r, "Coords_Type")),
    "coords_string": lambda r: _param(r, "Coords_String"),
    "values_out_of_range": lambda r: _group_flag(r, "Misc_Flags", "Values_Out_of_Range"),
    "near_bright_star": lambda r: _group_flag(r, "Misc_Flags", "Near_Bright_Star"),
    "err_circle_in_galaxy": lambda r: _group_flag(r, "Misc_Flags", "Err_Circle_in_Galaxy"),
    "galaxy_in_err_circle": lambda r: _group_flag(r, "Misc_Flags", "Galaxy_in_Err_Circle"),
    "too_generated": lambda r: _group_flag(r, "Misc_Flags", "TOO_Generated"),
    "trig_time_is_sec_hdr_time": lambda r: _group_flag(r, "Misc_Flags", "Trig_time_is_SecHdrTime"),
    "delayed_transmission": lambda r: _group_flag(r, "Misc_Flags", "Delayed_Transmission"),
    "updated_notice": lambda r: _group_flag(r, "Misc_Flags", "Updated_Notice"),
    "flt_generated": lambda r: _group_flag(r, "Misc_Flags", "Flt_Generated"),
    "gnd_generated": lambda r: _group_flag(r, "Misc_Flags", "Gnd_Generated"),
    "temporal_prox_match": lambda r: _group_flag(r, "Misc_Flags", "Temporal_Prox_Match"),
    "crc_error": lambda r: _group_flag(r, "Misc_Flags", "CRC_Error"),
}

_WHEREWHEN_RULES = {
    "burst_datetime": lambda r: datetime.fromisoformat(
        _text(r, "WhereWhen/ObsDataLocation/ObservationLocation/AstroCoords/Time/TimeInstant/ISOTime")
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
    """Helper parser for VOEvent `Who` block."""
    return {k: v(root) for k, v in _WHO_RULES.items()}


def _parse_what(root: ET.Element) -> dict:
    """Helper parser for VOEvent `What` block."""
    return {k: v(root) for k, v in _WHAT_RULES.items()}


def _parse_where_when(root: ET.Element) -> dict:
    """Helper parser for VOEvent `WhereWhen` block."""
    return {k: v(root) for k, v in _WHEREWHEN_RULES.items()}


def _parse_how(root: ET.Element) -> dict:
    """Helper parser for VOEvent `How` block."""
    return {k: v(root) for k, v in _HOW_RULES.items()}


def _parse_why(root: ET.Element) -> dict:
    """Helper parser for VOEvent `Why` block."""
    return {k: v(root) for k, v in _WHY_RULES.items()}


def _parse_citations(root: ET.Element) -> dict:
    """Helper parser for VOEvent `Citations` block."""
    return {k: v(root) for k, v in _CITATIONS_RULES.items()}


def parse_fermi_gbm_alert(value: bytes) -> FermiGBMAlert:
    """Parses a Fermi GBM alert from bytes."""
    root = ET.fromstring(value)
    data = {}
    data.update(_parse_who(root))
    data.update(_parse_what(root))
    data.update(_parse_where_when(root))
    data.update(_parse_how(root))
    data.update(_parse_why(root))
    data.update(_parse_citations(root))
    return FermiGBMAlert(**data)
