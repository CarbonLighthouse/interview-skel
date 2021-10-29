import unittest

from models_and_fixtures import BUILDINGS


class TestSampleTask(unittest.TestCase):
    def test_get_past_and_future_year_of_monthly_energy_usage_without_measures(self):
        for building in BUILDINGS:
            result = building.get_past_and_future_year_of_monthly_energy_usage_without_measures()
            # print(result)
            # should have two years of 15m results
            self.assertEqual(len(result), 24)


class TestChallengeSampleTask(unittest.TestCase):
    def test_get_past_and_future_year_of_monthly_energy_usage_with_measures(self):
        for building in BUILDINGS:
            result_without_measures = building.get_past_and_future_year_of_monthly_energy_usage_without_measures()
            result_with_measures = building.get_past_and_future_year_of_monthly_energy_usage_with_measures()
            # because the Challenge Task is not implemented, this assert will fail
            self.assertLess(result_with_measures[0]['value'], result_without_measures[0]['value'])


if __name__ == '__main__':
    unittest.main()
