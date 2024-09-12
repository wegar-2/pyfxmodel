from datetime import datetime
from pathlib import Path
import zipfile

from histdata import download_hist_data
from histdata.api import Platform, TimeFrame
from loguru import logger
import pandas as pd
import pytz

from pyfxmodel.src.pair import Pair
EST = pytz.timezone("EST")


class Extractor:

    _DPATH: Path = Path(__file__).parent.parent / "data"

    def __init__(
            self,
            year: int,
            month: int,
            pair: Pair
    ):
        assert pd.Period(year=year, month=month, freq="M"), \
            "Invalid year-month passed"
        self._year: int = year
        self._month: int = month
        self._pair: Pair = pair

    def extract(self) -> pd.DataFrame:
        logger.info("Downloading data")
        data_path: Path = Path(download_hist_data(
            year=self._year,
            month=self._month,
            pair=self._pair.value,
            time_frame=TimeFrame.TICK_DATA,
            platform=Platform.GENERIC_ASCII,
            output_directory=str(self._DPATH),
            verbose=True
        ))
        logger.info("Unpacking data")
        with zipfile.ZipFile(file=data_path, mode="r") as zip_file:
            data_file, _ = zip_file.namelist()
            with zip_file.open(data_file, mode="r") as int_data_file:
                data: pd.DataFrame = pd.read_csv(
                    int_data_file, sep=",", decimal=".", header=None,
                    names=["time_stamp", "bid", "ask", "marker"],
                    index_col=False,
                )
            data["time_stamp"] = [
                datetime.strptime(x, "%Y%m%d %H%M%S%f").replace(
                    tzinfo=EST).astimezone(tz=pytz.UTC)
                for x in data["time_stamp"]
            ]
            data = data.set_index("time_stamp")
            data = data.sort_index()
        if data_path.exists():
            logger.info("Tidying up")
            data_path.unlink()
        return data


if __name__ == '__main__':

    data_ = Extractor(year=2024, month=1, pair=Pair.EURPLN).extract()
