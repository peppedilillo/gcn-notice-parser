"""Parser for Fermi GBM alert notices."""

from datetime import datetime
from typing import Annotated

from pydantic import BaseModel

from ..parse_xml import attr
from ..parse_xml import group_flag
from ..parse_xml import opt_text
from ..parse_xml import param
from ..parse_xml import parse_utc_datetime
from ..parse_xml import parse_voevent_notice
from ..parse_xml import root_attr
from ..parse_xml import text


class FermiGBMAlert(BaseModel):
    """Parsed Fermi-GBM VOEvent alert notice.

    Attributes:
        author_contact_name: Contact name of the notice author.
        author_email: Email address of the notice author.
        alert_datetime: UTC datetime when the notice was issued (ISO-8601).
        ivorn: Raw VOEvent IVORN identifying this notice instance.
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
        followup: IVORN of the parent notice that this notice updates (unlikely any).

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


_ROOT_RULES = {
    "ivorn": lambda r: root_attr(r, "ivorn"),
}

_WHO_RULES = {
    "author_contact_name": lambda r: text(r, "Who/Author/contactName"),
    "author_email": lambda r: text(r, "Who/Author/contactEmail"),
    "alert_datetime": lambda r: parse_utc_datetime(text(r, "Who/Date")),
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
    "packet_type": lambda r: int(param(r, "Packet_Type")),
    "pkt_ser_num": lambda r: int(param(r, "Pkt_Ser_Num")),
    "trig_id": lambda r: int(param(r, "TrigID")),
    "sequence_num": lambda r: int(param(r, "Sequence_Num")),
    "burst_tjd": lambda r: int(param(r, "Burst_TJD")),
    "burst_sod": lambda r: float(param(r, "Burst_SOD")),
    "trig_signif": lambda r: float(param(r, "Trig_Signif")),
    "trig_dur": lambda r: float(param(r, "Trig_Dur")),
    "lo_chan_index": lambda r: int(param(r, "Lo_Chan_Index")),
    "hi_chan_index": lambda r: int(param(r, "Hi_Chan_Index")),
    "lo_chan_energy": lambda r: int(param(r, "Lo_Chan_Energy")),
    "hi_chan_energy": lambda r: None if param(r, "Hi_Chan_Energy") == "infinity" else int(param(r, "Hi_Chan_Energy")),
    "adc_lo_chan": lambda r: int(param(r, "ADC_Lo_Chan")),
    "adc_hi_chan": lambda r: int(param(r, "ADC_Hi_Chan")),
    "algorithm": lambda r: int(param(r, "Algorithm")),
    "dets": lambda r: _parse_dets(param(r, "Dets")),
    "sc_long": lambda r: float(param(r, "SC_Long")),
    "sc_lat": lambda r: float(param(r, "SC_Lat")),
    "lightcurve_url": lambda r: param(r, "LightCurve_URL"),
    "coords_type": lambda r: int(param(r, "Coords_Type")),
    "coords_string": lambda r: param(r, "Coords_String"),
    "values_out_of_range": lambda r: group_flag(r, "Misc_Flags", "Values_Out_of_Range"),
    "near_bright_star": lambda r: group_flag(r, "Misc_Flags", "Near_Bright_Star"),
    "err_circle_in_galaxy": lambda r: group_flag(r, "Misc_Flags", "Err_Circle_in_Galaxy"),
    "galaxy_in_err_circle": lambda r: group_flag(r, "Misc_Flags", "Galaxy_in_Err_Circle"),
    "too_generated": lambda r: group_flag(r, "Misc_Flags", "TOO_Generated"),
    "trig_time_is_sec_hdr_time": lambda r: group_flag(r, "Misc_Flags", "Trig_time_is_SecHdrTime"),
    "delayed_transmission": lambda r: group_flag(r, "Misc_Flags", "Delayed_Transmission"),
    "updated_notice": lambda r: group_flag(r, "Misc_Flags", "Updated_Notice"),
    "flt_generated": lambda r: group_flag(r, "Misc_Flags", "Flt_Generated"),
    "gnd_generated": lambda r: group_flag(r, "Misc_Flags", "Gnd_Generated"),
    "temporal_prox_match": lambda r: group_flag(r, "Misc_Flags", "Temporal_Prox_Match"),
    "crc_error": lambda r: group_flag(r, "Misc_Flags", "CRC_Error"),
}

_WHEREWHEN_RULES = {
    "burst_datetime": lambda r: parse_utc_datetime(
        text(r, "WhereWhen/ObsDataLocation/ObservationLocation/AstroCoords/Time/TimeInstant/ISOTime")
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


def parse_fermi_gbm_alert(value: bytes) -> FermiGBMAlert:
    """Parses a Fermi GBM alert notice from bytes.

    Args:
        value: Raw XML bytes of the VOEvent notice.

    Returns:
        Parsed GBM alert notice model.

    Raises:
        ParseError: If the XML document cannot be parsed or model validation
            fails.
        FieldParseError: If a specific field cannot be extracted from the
            notice.
    """
    return parse_voevent_notice(
        value,
        FermiGBMAlert,
        "parse_fermi_gbm_alert",
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
