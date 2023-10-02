from dataclasses import dataclass
####Global variables####
@dataclass
class Globals:
    tooling: str = ""
    leds_per_nest: int = 3
    tolerance: float = 0.015
    lo_tolerance: float = 0.02
    hi_tolerance: float = 0.03

glob = Globals(
    tooling="TOP_PASSAT_B9",
    leds_per_nest=3,
    tolerance=0.015,
    lo_tolerance=0.02,
    hi_tolerance=0.03
)