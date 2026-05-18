from datetime import datetime
from typing import Literal

from pydantic import BaseModel

from ..parse_json import parse_json_notice


class EinsteinProbeWXT(BaseModel):
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
    return parse_json_notice(value, EinsteinProbeWXT, "parse_einstein_probe_wxt")
