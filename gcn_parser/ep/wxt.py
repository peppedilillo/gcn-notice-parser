"""Parser for Einstein Probe WXT alert notices."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel

from ..parse_json import parse_json_notice


class EinsteinProbeWXT(BaseModel):
    """Parsed Einstein Probe WXT alert notice."""

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
    """Parse an Einstein Probe WXT alert notice.

    Args:
        value: Raw JSON bytes of the notice.

    Returns:
        Parsed Einstein Probe WXT alert notice model.

    Raises:
        ParseError: If the JSON document cannot be parsed or model validation
            fails.
    """
    return parse_json_notice(value, EinsteinProbeWXT, "parse_einstein_probe_wxt")
