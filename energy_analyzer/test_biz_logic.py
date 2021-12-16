import unittest
from datetime import datetime
from .models import Building, Measure, MeasureType, get_first_moment_of_month

# These fixtures are provided as an overview of what a building setup could look like.
# Note that the dates on which measures are active do not necessarily overlap. Feel
# free to add more fixtures as you build out your own tests.
BUILDINGS = [
    Building(
        name="Building 1",
        measures=[
            Measure(
                name="Building 1 - Measure 1",
                measure_type=MeasureType.SCHEDULING,
                start=datetime(year=2020, month=6, day=1),
                end=datetime(year=2021, month=1, day=1),
            ),
            Measure(
                name="Building 1 - Measure 2",
                measure_type=MeasureType.SAT_RESET,
                start=datetime(year=2021, month=8, day=7),
                end=datetime(year=2021, month=12, day=1),
            ),
        ],
    ),
    Building(
        name="Building 2",
        measures=[
            Measure(
                name="Building 2 - Measure 1",
                measure_type=MeasureType.LED_RETROFIT,
                start=datetime(year=2022, month=6, day=1),
                end=datetime(year=2023, month=1, day=1),
            )
        ],
    ),
]


class TestSampleTask(unittest.TestCase):
    def test_get_past_and_future_year_of_monthly_energy_usage_without_measures(self):
        for building in BUILDINGS:
            result = (
                building.get_past_and_future_year_of_monthly_energy_usage_without_measures()
            )
            # should have two years of 15m results
            self.assertEqual(len(result), 24)


class TestChallengeSampleTask(unittest.TestCase):
    @staticmethod
    def _measure_is_active_for_month(measure: Measure, timestamp: datetime) -> bool:
        return get_first_moment_of_month(measure.start) <= timestamp < measure.end

    def test_get_past_and_future_year_of_monthly_energy_usage_with_measures(self):
        for building in BUILDINGS:
            result_with_measures = (
                building.get_past_and_future_year_of_monthly_energy_usage_with_measures()
            )
            result_without_measures = (
                building.get_past_and_future_year_of_monthly_energy_usage_without_measures()
            )
            print(result_with_measures)
            print(result_without_measures)
            # this should pass once the Challenge task has been completed correctly
            for with_measures, without_measures in zip(
                result_with_measures, result_without_measures
            ):
                ts = with_measures["timestamp"]
                if any(
                    self._measure_is_active_for_month(measure, ts)
                    for measure in building.measures
                ):
                    self.assertLess(with_measures["value"], without_measures["value"])
                else:
                    self.assertEqual(with_measures["value"], without_measures["value"])


if __name__ == "__main__":
    unittest.main()
