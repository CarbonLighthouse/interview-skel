import unittest
from datetime import datetime
from dateutil.relativedelta import relativedelta
from .models import Building, Measure, MeasureType, get_first_moment_of_month

# These fixtures are provided as an overview of what a building setup could look like.
# Note that the dates on which measures are active do not necessarily overlap. Feel
# free to add more fixtures as you build out your own tests.
BUILDINGS = [
    Building(name="Building 1", measures=[
        Measure(
            name="Building 1 - Measure 1",
            measure_type=MeasureType.SCHEDULING,
            start=datetime(year=2020, month=6, day=1),
            end=datetime(year=2021, month=1, day=1)
        ),
        Measure(
            name="Building 1 - Measure 2",
            measure_type=MeasureType.SAT_RESET,
            start=datetime(year=2021, month=8, day=1),
            end=datetime(year=2021, month=12, day=1)
        ),
    ]),
    Building(name="Building 2", measures=[
        Measure(
            name="Building 2 - Measure 1",
            measure_type=MeasureType.LED_RETROFIT,
            start=datetime(year=2022, month=6, day=1),
            end=datetime(year=2023, month=1, day=1)
        )
    ])
]


class TestSampleTask(unittest.TestCase):
    def test_get_past_and_future_year_of_monthly_energy_usage_without_measures(self):
        for building in BUILDINGS:
            result = building.get_past_and_future_year_of_monthly_energy_usage_without_measures()
            # should have two years of 15m results
            self.assertEqual(len(result), 24)


class TestChallengeSampleTask(unittest.TestCase):
    def test_get_past_and_future_year_of_monthly_energy_usage_with_measures(self):
        for building in BUILDINGS:
            result_without_measures = building.get_past_and_future_year_of_monthly_energy_usage_without_measures()
            result_with_measures = building.get_past_and_future_year_of_monthly_energy_usage_with_measures()
            # this should pass once the Challenge task has been completed correctly
            self.assertLess(result_with_measures[0]['value'], result_without_measures[0]['value'])


    def test_measure_dates_applied_correctly(self):
        measure_start = get_first_moment_of_month(datetime.now())
        measure_end = measure_start + relativedelta(months=8)

        building = Building(
            name="Test Building",
            measures=[Measure(
                name="Test Building Measure",
                measure_type=MeasureType.AHU_VFD,
                start=measure_start,
                end=measure_end
            )]
        )

        result_without_measures = building.get_past_and_future_year_of_monthly_energy_usage_without_measures()
        result_with_measures = building.get_past_and_future_year_of_monthly_energy_usage_with_measures()
        # this should pass once the Challenge task has been completed correctly
        self.assertEqual(len(result_without_measures), len(result_with_measures))
        for res_without_measure, res_with_measure in zip(result_without_measures, result_with_measures):
            if res_without_measure["timestamp"] < measure_start or res_without_measure > measure_end:
                self.assertLess(res_with_measure["value"], res_without_measure["value"])
            else:
                self.assertEqual(res_with_measure["value"], res_without_measure["value"])



if __name__ == '__main__':
    unittest.main()
