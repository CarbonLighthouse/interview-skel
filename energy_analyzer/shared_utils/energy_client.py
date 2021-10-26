from enum import Enum
from typing import Dict, List
from random import random
import time
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
    def get_baseline_energy_usage_kwh(start: datetime, end: datetime, building_name: str) -> List[Dict]:
        current_time = round_to_last_15m(start)
        results = []

        while current_time < end:
            results.append({
                'timestamp': current_time,
                'value': 1000
            })

            current_time += relativedelta(minutes=15)

        # Part III
        # fake this result taking a while to run. In the real world, this
        # would take even longer
        # time.sleep(3)

        return results

    @staticmethod
    def get_measure_energy_savings_kwh(measure_type: MeasureType, measure_name: str) -> List[Dict]:

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

        # Part III
        # fake this result taking a while to run. In the real world, this
        # would take even longer
        # time.sleep(3)

        return results

