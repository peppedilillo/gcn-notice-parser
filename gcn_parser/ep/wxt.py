"""Parser for Einstein Probe WXT alert notices."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel

from ..parse_json import parse_json_notice


class EinsteinProbeWXT(BaseModel):
    """Parsed Einstein Probe WXT alert notice.

    Candidate X-ray transient reported from the EP/WXT on board trigger.

    Attributes:
        instrument: Reporting instrument. Always ``"WXT"``.
        trigger_time: UTC trigger time of the transient.
        id: Mission-provided event identifiers.
        ra: Right ascension of the candidate transient position (deg).
        dec: Declination of the candidate transient position (deg).
        ra_dec_error: Positional uncertainty radius for RA/Dec (deg).
        image_energy_range: Energy range of the accumulated image (keV).
        net_count_rate: Net count rate derived from the accumulated image.
        image_snr: Signal-to-noise ratio in the image.
        additional_info: Mission-provided note about the notice or measurement.

    """

    instrument: Literal["WXT"]
    trigger_time: datetime
    id: tuple[str, ...]
    ra: float
    dec: float
    ra_dec_error: float
    image_energy_range: tuple[float, float]
    net_count_rate: float
    image_snr: float
    additional_info: str


def parse_einstein_probe_wxt(value: bytes) -> EinsteinProbeWXT:
    """Parse an Einstein Probe WXT alert notice from bytes.

    Args:
        value: Raw JSON bytes of the notice.

    Returns:
        Parsed Einstein Probe WXT alert notice model.

    Raises:
        ParseError: If the JSON document cannot be parsed or model validation
            fails.
    """
    return parse_json_notice(value, EinsteinProbeWXT, "parse_einstein_probe_wxt")
