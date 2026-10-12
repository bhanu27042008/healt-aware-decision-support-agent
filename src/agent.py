"""Decision rules for the Weather-Based Activity Agent."""


def recommend_activities(
    temperature=None,
    rain_chance=None,
    wind_speed=None,
    condition=None,
):
    """Recommend activities using the available weather information."""

    recommendations = []
    reasons = []
    warnings = []

    # Validate optional numeric inputs.
    values = {
        "temperature": (temperature, -50, 60),
        "rain chance": (rain_chance, 0, 100),
        "wind speed": (wind_speed, 0, 300),
    }

    for name, (value, minimum, maximum) in values.items():
        if value is not None:
            if not isinstance(value, (int, float)) or isinstance(value, bool):
                raise ValueError(f"{name} must be a number.")
            if not minimum <= value <= maximum:
                raise ValueError(
                    f"{name} must be between {minimum} and {maximum}."
                )

    if condition is not None:
        condition = condition.strip().lower()
        if not condition:
            condition = None

    # Rule 1: Handle missing information.
    if all(
        value is None
        for value in (temperature, rain_chance, wind_speed, condition)
    ):
        return {
            "recommendations": ["Indoor study or reading"],
            "reasons": ["Weather data is missing; an indoor activity is a cautious default."],
            "warnings": ["Enter weather information for a more reliable recommendation."],
        }

    if temperature is None:
        warnings.append("Temperature is missing.")
    if rain_chance is None:
        warnings.append("Rain probability is missing.")
    if wind_speed is None:
        warnings.append("Wind speed is missing.")

    # Rule 2: Identify conditions that make outdoor activities unsuitable.
    severe_weather = condition in {
        "thunderstorm", "storm", "cyclone", "heavy rain"
    }

    too_hot = temperature is not None and temperature >= 38
    too_cold = temperature is not None and temperature < 5
    windy = wind_speed is not None and wind_speed >= 30
    rainy = rain_chance is not None and rain_chance >= 50

    if severe_weather:
        reasons.append("Severe weather reported; avoid outdoor activities.")

    if too_hot:
        reasons.append("High temperature; avoid strenuous outdoor activity.")

    if too_cold:
        reasons.append("Very low temperature; prefer a comfortable indoor setting.")

    if windy:
        reasons.append("Strong winds make some outdoor activities less suitable.")

    if rainy:
        reasons.append("High chance of rain; outdoor plans may be disrupted.")

    unsafe_outdoors = (
        severe_weather or too_hot or too_cold or windy or rainy
    )

    # Rule 3: Recommend indoor activities when conditions are unsuitable.
    if unsafe_outdoors:
        recommendations.extend([
            "Indoor study or reading",
            "Indoor games or exercise",
        ])

    # Rule 4: Recommend outdoor activities when the known conditions are suitable.
    else:
        enough_data = (
            temperature is not None
            and rain_chance is not None
            and wind_speed is not None
        )

        if enough_data:
            if condition in {"sunny", "clear", "partly cloudy", "cloudy"} or condition is None:
                recommendations.extend([
                    "Walking or cycling",
                    "Outdoor sports or a picnic",
                ])
                reasons.append(
                    "Available weather data indicates conditions suitable "
                    "for ordinary outdoor activities."
                )
        else:
            recommendations.append("Indoor study or reading")
            reasons.append(
                "Some weather data is missing; indoor activity is the safer default."
            )

    # Rule 5: Explain when a recommendation is based on limited data.
    if not reasons:
        reasons.append("Recommendations are based on the available weather data.")

    return {
        "recommendations": recommendations,
        "reasons": reasons,
        "warnings": warnings,
    }
