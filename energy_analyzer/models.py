from collections import defaultdict
from datetime import datetime
from typing import List, Optional

from dateutil.relativedelta import relativedelta
from pydantic import BaseModel

from energy_client import EnergyClient, MeasureType, Timeseries


def get_first_moment_of_month(now: datetime) -> datetime:
    return now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)


class Fault(BaseModel):  # Not used for the at-home challenge
    """
    This model represents a Faulty measure, and is used to adjust the savings
    of a measure over a specific time range. For a given measure, you can
    assume that there are no overlapping faults.
    """

    name: str
    fault_factor: float = 1
    start: datetime
    end: datetime


class Measure(BaseModel):
    """
    This model represents an Energy Efficiency Measure, including a time range that
    describes when that measure was implemented / active on a building.
    """

    name: str
    measure_type: MeasureType
    faults: Optional[List[Fault]]  # not used for the at-home challenge
    start: datetime
    end: datetime


class Building(BaseModel):
    """
    This model represents the overall Building in which we are looking to reduce energy usage.
    Each Building has a list of Energy Efficiency Measures which provide energy savings over
    a given time frame.
    """

    name: str
    measures: Optional[List[Measure]]

    def get_past_and_future_year_of_monthly_energy_usage_without_measures(
        self,
    ) -> Timeseries:
        now = get_first_moment_of_month(datetime.now())
        start = now - relativedelta(years=1)
        end = now + relativedelta(years=1)

        quarter_hourly_data = EnergyClient.get_building_expected_energy_usage(
            start, end, self.name
        )

        bucket_res = defaultdict(int)
        for quarter_hour_usage in quarter_hourly_data:
            bucket_ts = get_first_moment_of_month(quarter_hour_usage["timestamp"])
            bucket_res[bucket_ts] += quarter_hour_usage["value"]

        return [{"timestamp": ts, "value": v} for ts, v in bucket_res.items()]

    def get_past_and_future_year_of_monthly_energy_usage_with_measures(
        self,
    ) -> Timeseries:
        # Please provide your solution here.
        raise NotImplementedError()
