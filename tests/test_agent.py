"""Automated tests for the Weather-Based Activity Agent."""

import sys
import unittest
from pathlib import Path

# Make the src folder available to Python during testing.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from agent import recommend_activities


class TestWeatherAgent(unittest.TestCase):

    def test_suitable_weather_recommends_outdoor_activities(self):
        result = recommend_activities(
            temperature=28,
            rain_chance=10,
            wind_speed=8,
            condition="sunny",
        )
        self.assertIn("Walking or cycling", result["recommendations"])

    def test_high_rain_chance_prefers_indoor_activities(self):
        result = recommend_activities(
            temperature=25,
            rain_chance=80,
            wind_speed=5,
            condition="cloudy",
        )
        self.assertIn("Indoor study or reading", result["recommendations"])

    def test_severe_weather_prefers_indoor_activities(self):
        result = recommend_activities(
            temperature=25,
            rain_chance=20,
            wind_speed=5,
            condition="thunderstorm",
        )
        self.assertIn("Indoor study or reading", result["recommendations"])

    def test_missing_weather_data_returns_warning(self):
        result = recommend_activities(
            temperature=25,
            rain_chance=None,
            wind_speed=5,
            condition="sunny",
        )
        self.assertTrue(result["warnings"])

    def test_invalid_temperature_is_rejected(self):
        with self.assertRaises(ValueError):
            recommend_activities(temperature=100)

    def test_empty_weather_data_uses_safe_default(self):
        result = recommend_activities()
        self.assertIn("Indoor study or reading", result["recommendations"])


if __name__ == "__main__":
    unittest.main()
