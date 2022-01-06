import unittest
from datetime import datetime
from dateutil.relativedelta import relativedelta
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

    # this should pass once the Challenge task has been completed correctly
    def test_get_past_and_future_year_of_monthly_energy_usage_with_measures(self):
        for building in BUILDINGS:
            result_with_measures = (
                building.get_past_and_future_year_of_monthly_energy_usage_with_measures()
            )
            result_without_measures = (
                building.get_past_and_future_year_of_monthly_energy_usage_without_measures()
            )
            for with_measures, without_measures in zip(
                result_with_measures, result_without_measures
            ):
                ts = with_measures["timestamp"]
                if any(
                    get_first_moment_of_month(measure.start) <= ts < measure.end
                    for measure in building.measures
                ):
                    self.assertLess(with_measures["value"], without_measures["value"])
                else:
                    self.assertEqual(with_measures["value"], without_measures["value"])

    # this should pass once the Challenge task has been completed correctly
    def test_partial_month_coverage(self):
        start_of_month = get_first_moment_of_month(datetime.now())

        building_partial_coverage = Building(
            name="Building Partial Coverage",
            measures=[
                Measure(
                    name="Measure Partial Coverage",
                    measure_type=MeasureType.SAT_RESET,
                    start=datetime(
                        year=start_of_month.year,
                        month=start_of_month.month,
                        day=6,
                    ),
                    end=datetime(
                        year=start_of_month.year,
                        month=start_of_month.month,
                        day=15,
                    ),
                )
            ],
        )

        building_full_coverage = Building(
            name="Building Full Coverage",
            measures=[
                Measure(
                    name="Measure Full Coverage",
                    measure_type=MeasureType.SAT_RESET,
                    start=start_of_month,
                    end=start_of_month + relativedelta(months=1),
                )
            ],
        )

        result_partial_coverage = (
            building_partial_coverage.get_past_and_future_year_of_monthly_energy_usage_with_measures()
        )
        result_full_coverage = (
            building_full_coverage.get_past_and_future_year_of_monthly_energy_usage_with_measures()
        )

        for partial_coverage, full_coverage in zip(
            result_partial_coverage, result_full_coverage
        ):
            ts = partial_coverage["timestamp"]
            if ts.year == start_of_month.year and ts.month == start_of_month.month:
                self.assertLess(partial_coverage["value"], full_coverage["value"])


if __name__ == "__main__":
    unittest.main()
