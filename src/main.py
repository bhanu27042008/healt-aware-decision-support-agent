"""Terminal interface for the Weather-Based Activity Agent."""

from agent import recommend_activities


def get_number(prompt, minimum, maximum):
    """Read an optional number and validate its range."""
    while True:
        value = input(prompt).strip()

        if value == "":
            return None

        try:
            number = float(value)
        except ValueError:
            print("Please enter a valid number, or press Enter to skip.")
            continue

        if not minimum <= number <= maximum:
            print(f"Enter a value between {minimum} and {maximum}.")
            continue

        return number


def main():
    print("\n======================================")
    print("   WEATHER-BASED ACTIVITY AGENT")
    print("======================================")
    print("Enter the weather details below.")
    print("Optional fields can be left blank.\n")

    temperature = get_number(
        "Temperature in °C (-50 to 60): ", -50, 60
    )
    rain_chance = get_number(
        "Chance of rain in % (0 to 100): ", 0, 100
    )
    wind_speed = get_number(
        "Wind speed in km/h (0 to 300): ", 0, 300
    )
    condition = input(
        "Weather condition (sunny/cloudy/rainy/storm): "
    ).strip()

    try:
        result = recommend_activities(
            temperature=temperature,
            rain_chance=rain_chance,
            wind_speed=wind_speed,
            condition=condition or None,
        )
    except ValueError as error:
        print(f"\nInvalid weather data: {error}")
        return

    print("\n---------- RECOMMENDATIONS ----------")

    for activity in result["recommendations"]:
        print(f"• {activity}")

    print("\nReasons:")
    for reason in result["reasons"]:
        print(f"• {reason}")

    if result["warnings"]:
        print("\nMissing data / warnings:")
        for warning in result["warnings"]:
            print(f"• {warning}")

    print("\nThank you for using the agent!")


if __name__ == "__main__":
    main()
