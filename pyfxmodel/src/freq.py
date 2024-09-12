from enum import Enum


class Freq(Enum):
    TICK = "tick"
    S1 = "1sec"
    S5 = "5sec"
    S15 = "15sec"
    S30 = "30sec"
    M1 = "1min"
    M5 = "5min"
    H1 = "1h"
