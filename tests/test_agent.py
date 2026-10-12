
import os
import sys
import unittest

sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)

from agent import (
    DAYS,
    health_risks,
    allowed,
    probability_safe,
    forward_chaining,
    backward_chaining,
    create_weekly_plan,
)


def sample_weather():
    return {
        "rain": 10,
        "temp": 25,
        "aqi": 40,
        "heat": 26,
        "available": True,
    }


class TestHealthAwareAgent(unittest.TestCase):

    def test_high_aqi_triggers_warning(self):
        weather = sample_weather()
        weather["aqi"] = 150
        self.assertTrue(
            any("AQI warning" in risk for risk in health_risks(weather))
        )

    def test_high_heat_triggers_warning(self):
        weather = sample_weather()
        weather["heat"] = 41
        self.assertTrue(
            any("heat-stress" in risk for risk in health_risks(weather))
        )

    def test_rain_blocks_cycling(self):
        weather = sample_weather()
        weather["rain"] = 80
        self.assertFalse(allowed("Cycling", weather))

    def test_indoor_study_is_allowed(self):
        weather = sample_weather()
        weather["rain"] = 90
        weather["aqi"] = 200
        self.assertTrue(allowed("Indoor study", weather))

    def test_unavailable_user_cannot_do_activity(self):
        weather = sample_weather()
        weather["available"] = False
        self.assertFalse(allowed("Cycling", weather))

    def test_safety_estimate_is_in_range(self):
        value = probability_safe(sample_weather())
        self.assertGreaterEqual(value, 0)
        self.assertLessEqual(value, 1)

    def test_forward_chaining_returns_recommendation(self):
        facts, recommendation, trace = forward_chaining(sample_weather())
        self.assertIsInstance(facts, list)
        self.assertTrue(recommendation)
        self.assertTrue(trace)

    def test_backward_chaining_rejects_heavy_rain(self):
        weather = sample_weather()
        weather["rain"] = 90
        forecasts = {day: sample_weather() for day in DAYS}
        forecasts["Saturday"] = weather

        answer, trace = backward_chaining(
            "Saturday", "Cycling", forecasts
        )
        self.assertFalse(answer)
        self.assertTrue(trace)

    def test_weekly_plan_contains_all_days(self):
        forecasts = {day: sample_weather() for day in DAYS}
        result = create_weekly_plan(forecasts)

        self.assertIsNotNone(result["plan"])
        self.assertEqual(set(result["plan"]), set(DAYS))

    def test_ac3_reports_domain_counts(self):
        forecasts = {day: sample_weather() for day in DAYS}
        result = create_weekly_plan(forecasts)

        self.assertGreater(result["before_count"], 0)
        self.assertGreater(result["after_count"], 0)


if __name__ == "__main__":
    unittest.main()
