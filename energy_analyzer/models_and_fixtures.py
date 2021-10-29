from typing import List, Optional
from datetime import datetime

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

        current_time = get_first_moment_of_month(start)

        results = []
        quarter_hourly_data_index = 0
        while current_time < end:
            if quarter_hourly_data_index >= len(quarter_hourly_data):
                break

            bucket_timestamp = quarter_hourly_data[quarter_hourly_data_index]['timestamp']

            bucket_sum = 0
            while bucket_timestamp < (current_time + relativedelta(months=1)):
                if quarter_hourly_data_index >= len(quarter_hourly_data):
                    break
                bucket_timestamp = quarter_hourly_data[quarter_hourly_data_index]['timestamp']
                bucket_sum += quarter_hourly_data[quarter_hourly_data_index]['value']
                quarter_hourly_data_index += 1
            results.append({
                'timestamp': current_time,
                'value': bucket_sum
            })
            current_time += relativedelta(months=1)

        return results

    def get_past_and_future_year_of_monthly_energy_usage_with_measures(self):
        # Please provide your solution here.
        return self.get_past_and_future_year_of_monthly_energy_usage_without_measures()


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