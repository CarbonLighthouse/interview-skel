from collections import defaultdict
from datetime import datetime
from typing import List, Optional

from dateutil.relativedelta import relativedelta
from pydantic import BaseModel

from energy_client import EnergyClient, MeasureType


def get_first_moment_of_month(now: datetime) -> datetime:
    return now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)


class Fault(BaseModel):
    # Not used for the at-home challenge
    name: str
    fault_factor: float = 1
    start: datetime
    end: datetime


class Measure(BaseModel):
    name: str
    measure_type: MeasureType
    faults: Optional[List[Fault]]  # Note, this would actually be a reverse relation in a real data model
    start: datetime
    end: datetime


class Building(BaseModel):
    name: str
    measures: Optional[List[Measure]]  # Note, this would actually be a reverse relation in a real data model

    def get_past_and_future_year_of_monthly_energy_usage_without_measures(self):
        now = get_first_moment_of_month(datetime.now())
        start = now - relativedelta(years=1)
        end = now + relativedelta(years=1)

        quarter_hourly_data = EnergyClient.get_building_expected_energy_usage(start, end, self.name)

        bucket_res = defaultdict(int)
        for quarter_hour_usage in quarter_hourly_data:
            bucket_ts = get_first_moment_of_month(quarter_hour_usage["timestamp"])
            bucket_res[bucket_ts] += quarter_hour_usage["value"]

        return [{"timestamp": ts, "value": v} for ts, v in bucket_res.items()]


    def get_past_and_future_year_of_monthly_energy_usage_with_measures(self):
        # Please provide your solution here.
        raise NotImplementedError()

BUILDINGS = [
    Building(name="Building 1", measures=[
        Measure(
            name="Building 1 - Measure 1",
            measure_type=MeasureType.SCHEDULING,
            start=datetime(year=2020, month=1, day=1),
            end=datetime(year=2022, month=1, day=1)
        ),
        Measure(
            name="Building 1 - Measure 2",
            measure_type=MeasureType.SAT_RESET,
            start=datetime(year=2020, month=1, day=1),
            end=datetime(year=2022, month=1, day=1)
        ),
    ])
]
