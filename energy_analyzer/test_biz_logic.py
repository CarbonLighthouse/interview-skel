import unittest
from datetime import datetime

from dateutil.relativedelta import relativedelta

from models_and_fixtures import BUILDINGS


class TestPart0(unittest.TestCase):
    def test_get_baseline_energy_usage_kwh(self):
        end = datetime.now()
        start = end - relativedelta(hours=4)
        for building in BUILDINGS:
            result = building.get_baseline_energy_usage_kwh(start, end)
            # print(result)
            # should have two years of monthly results
            self.assertEqual(len(result), 17)

    def test_get_baseline_past_and_future_year_of_monthly_energy_usage(self):
        for building in BUILDINGS:
            result = building.get_baseline_past_and_future_year_of_monthly_energy_usage()
            # print(result)
            # should have 4h of 15m results
            self.assertEqual(len(result), 24)


class TestPart1(unittest.TestCase):
    pass

if __name__ == '__main__':
    unittest.main()
