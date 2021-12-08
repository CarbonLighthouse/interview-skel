import time
from enum import Enum
from typing import Dict, List

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


class MeasureType(Enum):
    SCHEDULING = 1
    SAT_RESET = 2
    LED_RETROFIT = 3
    AHU_VFD = 4


def round_to_last_15m(dt):
    return dt - (dt - datetime.min) % timedelta(minutes=15)


class EnergyClient():
    @staticmethod
    def get_building_expected_energy_usage(start: datetime, end: datetime, building_name: str) -> List[Dict]:
        """
        This API call will return a list of dicts that represents timeseries data at 15 minute intervals.

        The start and end dates determine the range of the result.

        Ex. result:
        [
            {
                'timestamp': 2021-09-16 22:00:00,
                'value': 1000
            },
            ...
            {
                'timestamp': 2021-010-16 22:00:00,
                'value': 1000
            },
        ]
        """
        current_time = round_to_last_15m(start)
        results = []

        while current_time < end:
            results.append({
                'timestamp': current_time,
                'value': 1000  # This value is hard-coded in this example, but represents an energy prediction.
            })

            current_time += relativedelta(minutes=15)

        # Not used for the at-home challenge
        # time.sleep(3)

        return results

    @staticmethod
    def get_measure_expected_energy_savings(measure_type: MeasureType, measure_name: str) -> List[Dict]:
        """
        This API call will return a list of dicts that represents timeseries data at 15 minute intervals.

        The result represents the expected savings over an average year. The year will be set to `2010`, but
        that year should be ignored: this data represents an arbitrary year, not a specific year.

        Ex. result:
        [
            {
                'timestamp': 2010-01-01 00:00:00,
                'value': 201
            },
            ...
            {
                'timestamp': 2010-12-21 23:45:00,
                'value': 205
            },
        ]
        """
        # These values are hard-coded in this example, but represent an energy savings prediction.
        _SAVINGS_BY_MEASURE = {
            MeasureType.SCHEDULING: 100,
            MeasureType.SAT_RESET: 200,
            MeasureType.LED_RETROFIT: 300,
            MeasureType.AHU_VFD: 400,
        }
        current_time = datetime(year=2010, month=1, day=1)
        end = current_time + relativedelta(years=1)
        results = []

        while current_time < end:
            results.append({
                'timestamp': current_time,
                'value': _SAVINGS_BY_MEASURE[measure_type]
            })

            current_time += relativedelta(minutes=15)

        # Not used for the at-home challenge
        # time.sleep(3)

        return results

