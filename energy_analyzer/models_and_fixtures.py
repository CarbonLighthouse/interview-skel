from typing import List
from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta
from pydantic import BaseModel

from shared_utils.energy_client import EnergyClient, MeasureType


def get_first_moment_of_month(now: datetime) -> datetime:
    return now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)


class Fault(BaseModel):
    name: str
    fault_factor: float = 1
    # TODO: implement any additional fields needed


class Measure(BaseModel):
    name: str
    measure_type: MeasureType
    faults: List[Fault]  # Note, this would actually be a reverse relation in a real data model
    # TODO: implement any additional fields needed

    def get_measure_energy_savings_kwh(self):
        return EnergyClient.get_measure_energy_savings_kwh(self.measure_type, self.name)


class Building(BaseModel):
    name: str
    measures: List[Measure]  # Note, this would actually be a reverse relation in a real data model

    def get_baseline_energy_usage_kwh(self, start, end):
        return EnergyClient.get_baseline_energy_usage_kwh(start, end, self.name)

    def get_baseline_past_and_future_year_of_monthly_energy_usage(self):
        now = get_first_moment_of_month(datetime.now())
        start = now - relativedelta(years=1)
        end = now + relativedelta(years=1)

        quarter_hourly_data = self.get_baseline_energy_usage_kwh(start, end)

        current_time = get_first_moment_of_month(start)

        results = []
        quarter_hourly_data_index = 0
        while current_time < end:
            if quarter_hourly_data_index >= len(quarter_hourly_data):
                break

            bucket_time = quarter_hourly_data[quarter_hourly_data_index]['timestamp']

            bucket_sum = 0
            while bucket_time < (current_time + relativedelta(months=1)):
                if quarter_hourly_data_index >= len(quarter_hourly_data):
                    break
                bucket_time = quarter_hourly_data[quarter_hourly_data_index]['timestamp']
                bucket_sum += quarter_hourly_data[quarter_hourly_data_index]['value']
                quarter_hourly_data_index += 1
            results.append({
                'timestamp': current_time,
                'value': bucket_sum
            })
            current_time += relativedelta(months=1)

        return results


BUILDINGS = [
    Building(name="Building 1", measures=[
        Measure(name="Building 1 - Measure 1", measure_type=MeasureType.SCHEDULING),
        Measure(name="Building 1 - Measure 2", measure_type=MeasureType.SAT_RESET),
    ])
]