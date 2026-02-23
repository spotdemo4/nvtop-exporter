import subprocess
import json
import re
import logging
from typing import List, Annotated, Any
from pydantic import BaseModel, BeforeValidator
from pydantic_core import PydanticUseDefault

log = logging.getLogger(__name__)


def to_percent(value: int) -> float:
    return float(value) / 100


def strip_unit(value: str) -> int:
    match = re.match(r"^(-?\d+)", value.strip())
    if match:
        return int(match.groups()[0])
    else:
        log.warning(f"Could not strip unit from metric: {value}")
        return 0


def default_none(value: Any) -> Any:
    if value is None:
        raise PydanticUseDefault()

    return value


Default = Annotated[int, BeforeValidator(default_none)]
Unit = Annotated[int, BeforeValidator(strip_unit), BeforeValidator(default_none)]
Percentage = Annotated[
    float,
    BeforeValidator(to_percent),
    BeforeValidator(strip_unit),
    BeforeValidator(default_none),
]


class Process(BaseModel):
    pid: int
    cmdline: str
    kind: str
    user: str
    gpu_usage: Unit = 0
    gpu_mem_bytes_alloc: Default = 0
    gpu_mem_usage: Percentage = 0
    encode_decode: Percentage = 0


class Device(BaseModel):
    device_name: str
    gpu_clock: Unit = 0
    mem_clock: Unit = 0
    temp: Unit = 0
    fan_speed: Unit = 0
    power_draw: Unit = 0
    gpu_util: Percentage = 0
    encode_decode: Percentage = 0
    mem_util: Unit = 0
    mem_total: Default = 0
    mem_used: Default = 0
    mem_free: Default = 0
    processes: List[Process]


class NvTop(BaseModel):
    devices: List[Device]


def get_nvtop():
    log.debug("Running nvtop -s")
    result = subprocess.run(["nvtop", "-s"], capture_output=True, text=True, check=True)

    log.debug("Loading JSON")
    nvtop_dict = json.loads(result.stdout)
    log.debug(nvtop_dict)

    log.debug("Parsing JSON")
    nvtop = NvTop(devices=nvtop_dict)
    log.debug(nvtop)

    return nvtop
