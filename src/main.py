
"""IA-2: Health-Aware Decision Support Agent - User Interface."""

from agent import (
    DAYS,
    ACTIVITIES,
    health_risks,
    probability_safe,
    expected_utility,
    recommend_activity,
    forward_chaining,
    backward_chaining,
    create_weekly_plan,
)


def get_number(prompt, minimum, maximum):
    while True:
        try:
            value = float(input(prompt))
            if minimum <= value <= maximum:
                return value
            print(f"Enter a value between {minimum} and {maximum}.")
        except ValueError:
            print("Please enter a valid number.")


def get_yes_no(prompt):
    while True:
        value = input(prompt).strip().lower()
        if value in ("yes", "no"):
            return value == "yes"
        print("Please enter yes or no.")


def get_weather(day):
    print(f"\n--- {day} forecast ---")

    return {
        "rain": get_number("Rain probability (0-100%): ", 0, 100),
        "temp": get_number("Temperature (C): ", -20, 60),
        "aqi": get_number("AQI (0-500): ", 0, 500),
        "heat": get_number("Heat index (C): ", -20, 70),
        "available": get_yes_no("Are you available? (yes/no): "),
    }


def main():
    print("=" * 60)
    print("HEALTH-AWARE DECISION SUPPORT AGENT")
    print("=" * 60)
    print("Enter the forecast for each day of the week.")
    print("AQI and heat-index values should come from your forecast source.")
    forecasts = {day: get_weather(day) for day in DAYS}

    # 1. Expected-utility table
    print("\n1. EXPECTED-UTILITY TABLE")
    print(
        f"{'Day':<12}{'Recommended activity':<23}"
        f"{'P(safe)':>10}{'Expected utility':>19}"
    )

    for day in DAYS:
        weather = forecasts[day]
        activity = recommend_activity(weather)

        if activity in ACTIVITIES:
            utility = expected_utility(activity, weather)
        else:
            utility = 0.0

        print(
            f"{day:<12}{activity:<23}"
            f"{probability_safe(weather):>10.2f}{utility:>19.2f}"
        )

    # 2. Health rules and explanations
    print("\n2. HEALTH-RISK RULES AND EXPLANATIONS")

    for day in DAYS:
        print(f"\n{day}:")
        for risk in health_risks(forecasts[day]):
            print(" -", risk)

    # 3. Forward chaining
    print("\n3. FORWARD-CHAINING TRACE")

    for day in DAYS:
        facts, recommendation, trace = forward_chaining(forecasts[day])
        print(f"\n{day} facts: {facts or ['no warning facts']}")
        for step in trace:
            print(" -", step)

    # 4. Backward chaining
    print("\n4. BACKWARD-CHAINING QUERY")
    print("Available activities:", ", ".join(ACTIVITIES))

    while True:
        day = input("Choose a day (e.g. Saturday): ").strip().title()
        if day in DAYS:
            break
        print("Please enter a valid weekday.")

    while True:
        activity = input("Activity to check (exact name): ").strip()
        if activity in ACTIVITIES:
            break
        print("Choose an activity from the list.")

    answer, trace = backward_chaining(day, activity, forecasts)

    for step in trace:
        print(" -", step)

    print("Conclusion:", "YES, rules permit it." if answer else "NO, rules do not permit it.")

    # 5. CSP, AC-3 and backtracking
    print("\n5. WEEKLY CSP PLANNER")
    result = create_weekly_plan(forecasts)

    print("\nDomains before AC-3:")
    for day in DAYS:
        print(f" {day}: {result['domains_before'][day]}")

    print("\nDomains after AC-3:")
    for day in DAYS:
        print(f" {day}: {result['domains_after'][day]}")

    print("\nTotal domain values before AC-3:", result["before_count"])
    print("Total domain values after AC-3:", result["after_count"])
    print("Backtracking search calls:", result["search_calls"])

    if result["plan"] is None:
        print("No valid weekly plan found under the current constraints.")
    else:
        print("\nFinal weekly plan:")
        for day in DAYS:
            print(f" {day}: {result['plan'][day]}")

    print("\nDISCLAIMER")
    print(
        "This is an educational demonstration, not medical advice. "
        "Risk thresholds and safety estimates are illustrative, not "
        "medically validated. Follow official weather and air-quality "
        "alerts and consult a qualified healthcare professional for "
        "personal health concerns."
    )


if __name__ == "__main__":
    main()
