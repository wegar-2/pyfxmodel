from datetime import date
from typing import TypeAlias

Dates: TypeAlias = list[date]


class DataCalendar:

    def __init__(self, start: date, end: date):
        if start > end:
            raise ValueError()
        self._start: date = start
        self._end: date = end
        self._grid: Dates

    def _make_data_grid(self) -> Dates:
        pass
    