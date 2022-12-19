from collections import defaultdict
from datetime import datetime
from typing import List, Optional

from dateutil.relativedelta import relativedelta
from pydantic import BaseModel

from energy_analyzer.energy_client import (
    EnergyClient,
    MeasureType,
    Timeseries,
    DataPoint,
)


def get_first_moment_of_month(now: datetime) -> datetime:
    return now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)


class Measure(BaseModel):
    """
    This model represents an Energy Efficiency Measure, including a time range that
    describes when that measure was implemented / active on a building.
    """

    name: str
    measure_type: MeasureType
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

    def get_past_and_future_year_of_monthly_energy_usage(self) -> Timeseries:
        now = get_first_moment_of_month(datetime.now())
        start = now - relativedelta(years=1)
        end = now + relativedelta(years=1)

        quarter_hourly_usage_data = EnergyClient.get_building_expected_energy_usage(
            start, end
        )

        monthly_usage = defaultdict(int)
        for quarter_hour_usage in quarter_hourly_usage_data:
            month_timestamp = get_first_moment_of_month(quarter_hour_usage.timestamp)
            monthly_usage[month_timestamp] += quarter_hour_usage.value

        return [DataPoint(timestamp=ts, value=v) for ts, v in monthly_usage.items()]
