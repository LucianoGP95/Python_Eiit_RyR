from dataclasses import dataclass
####Global variables####
@dataclass
class Globals:
    tooling: str = "" #Refcode name of the tooling
    lenses_per_nest: int = 3 #Lenses placed in each nest
    nests_number: int = 4 #Number of nests in the machine
    x_tolerance: float = 0.0125 #X colour value allowed tolerance from nominal to limit
    y_tolerance: float = 0.015 #Y colour value allowed tolerance from nominal to limit
    lo_tolerance: float = 0.02 #General lower limit allowed tolerance
    hi_tolerance: float = 0.03 #General upper limit allowed tolerance

glob = Globals(
    tooling="TOP_PASSAT_B9",
    lenses_per_nest=3,
    nests_number=4,
    x_tolerance=0.0125, 
    y_tolerance=0.0165,
    lo_tolerance=0.02,
    hi_tolerance=0.03,
)