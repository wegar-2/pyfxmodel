from typing import Optional

import pandas as pd

from pyfxmodel.src.freq import Freq


class Transformer:

    def __init__(
            self,
            freq: Freq,
            exec_data: bool = False,
            ticks: Optional[int] = None
    ):
        self._freq: Freq = freq
        self._exec_data: bool = exec_data
        self._ticks: Optional[int] = ticks
        if self._freq == Freq.TICK:
            if ticks is None:
                raise ValueError("")

    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        pass
