from dataclasses import dataclass
####Global variables####
@dataclass
class Globals:
    tooling: str = ""
    leds_per_nest: int = 3
    x_tolerance: float = 0.0125
    y_tolerance: float = 0.015
    lo_tolerance: float = 0.02
    hi_tolerance: float = 0.03

glob = Globals(
    tooling="Test",
    leds_per_nest=3,
    x_tolerance=0.0125,
    y_tolerance=0.015,
    lo_tolerance=0.02,
    hi_tolerance=0.03
)