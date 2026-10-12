

DAYS = [
    "Monday", "Tuesday", "Wednesday", "Thursday",
    "Friday", "Saturday", "Sunday"
]

ACTIVITIES = [
    "Sports practice",
    "Cycling",
    "Picnic",
    "Laundry drying",
    "Outdoor study",
    "Indoor study"
]


def health_risks(weather):
    """Apply simple educational heat and air-quality rules."""
    risks = []

    if weather["aqi"] > 100:
        risks.append("AQI warning: sensitive people may be affected.")

    if weather["heat"] >= 40:
        risks.append("High heat-stress risk under the example rule.")
    elif weather["heat"] >= 35:
        risks.append("Heat caution: reduce strenuous outdoor activity.")

    if weather["rain"] >= 50:
        risks.append("High chance of rain.")

    if not risks:
        risks.append("No warning threshold triggered by these rules.")

    return risks


def allowed(activity, weather):
    """Check whether an activity satisfies the project's constraints."""

    if not weather["available"]:
        return False

    if activity == "Indoor study":
        return True

    # Avoid outdoor activities under these example risk thresholds.
    if weather["rain"] >= 50:
        return False
    if weather["aqi"] > 100:
        return False
    if weather["heat"] >= 40:
        return False

    if activity == "Sports practice":
        return 15 <= weather["temp"] <= 35 and weather["heat"] < 35

    if activity == "Cycling":
        return (
            10 <= weather["temp"] <= 35
            and weather["rain"] <= 20
            and weather["heat"] < 35
        )

    if activity == "Picnic":
        return (
            18 <= weather["temp"] <= 32
            and weather["rain"] <= 20
            and weather["heat"] < 35
        )

    if activity == "Laundry drying":
        return weather["temp"] >= 15 and weather["rain"] <= 20

    if activity == "Outdoor study":
        return (
            15 <= weather["temp"] <= 35
            and weather["rain"] <= 30
            and weather["heat"] < 35
        )

    return False


def probability_safe(weather):
    """
    Illustrative certainty estimate, not a trained Bayesian network
    or a medically validated probability.
    """
    risk = 0.0

    if weather["rain"] >= 40:
        risk += 0.30
    if weather["aqi"] > 100:
        risk += 0.35
    if weather["heat"] >= 35:
        risk += 0.35

    return max(0.0, 1.0 - risk)


def expected_utility(activity, weather):
    """EU = P(safe)*U(safe) + P(unsafe)*U(unsafe)."""

    utilities = {
        "Sports practice": (9, -10),
        "Cycling": (8, -10),
        "Picnic": (10, -8),
        "Laundry drying": (7, -4),
        "Outdoor study": (7, -5),
        "Indoor study": (5, 5),
    }

    p_safe = probability_safe(weather)
    safe_utility, unsafe_utility = utilities[activity]

    return (
        p_safe * safe_utility
        + (1 - p_safe) * unsafe_utility
    )


def recommend_activity(weather):
    """Choose the allowed activity with the highest expected utility."""

    if not weather["available"]:
        return "Unavailable"

    candidates = [
        activity for activity in ACTIVITIES
        if allowed(activity, weather)
    ]

    if not candidates:
        return "No suitable activity"

    return max(
        candidates,
        key=lambda activity: expected_utility(activity, weather)
    )


def forward_chaining(weather):
    """Infer warnings and a recommendation from known weather facts."""

    facts = []
    trace = []

    if weather["rain"] >= 50:
        facts.append("high_rain")
        trace.append("Rule: rain >= 50% -> high_rain.")

    if weather["aqi"] > 100:
        facts.append("poor_air_quality")
        trace.append("Rule: AQI > 100 -> poor_air_quality.")

    if weather["heat"] >= 35:
        facts.append("heat_warning")
        trace.append("Rule: heat index >= 35 C -> heat_warning.")

    if not weather["available"]:
        facts.append("unavailable")
        trace.append("Rule: user unavailable -> no activity.")

    recommendation = recommend_activity(weather)
    trace.append("Inferred recommendation: " + recommendation)

    return facts, recommendation, trace


def backward_chaining(day, activity, forecasts):
    """Answer a query such as: Can I go cycling on Saturday?"""

    weather = forecasts[day]
    trace = [f"Goal: Can I do {activity} on {day}?"]

    if not weather["available"]:
        trace.append("Failed: user is unavailable.")
        return False, trace

    trace.append("Availability condition passed.")

    if activity not in ACTIVITIES:
        trace.append("Failed: unknown activity.")
        return False, trace

    if not allowed(activity, weather):
        trace.append("Failed: activity violates a programmed constraint.")
        return False, trace

    trace.append("Weather and activity constraints passed.")
    trace.append("The rules support this activity, not a guarantee of safety.")
    return True, trace


# ---------- Constraint Satisfaction Problem (CSP) ----------


def compatible(activity_a, activity_b):
    """Constraint for activities on consecutive days."""

    if "Unavailable" in (activity_a, activity_b):
        return True

    if activity_a == "Indoor study" or activity_b == "Indoor study":
        return True

    return activity_a != activity_b



def make_domains(forecasts):
    domains = {}

    for day in DAYS:
        weather = forecasts[day]

        if not weather["available"]:
            domains[day] = ["Unavailable"]
            continue

        choices = [
            activity for activity in ACTIVITIES
            if allowed(activity, weather)
        ]

        # Ensure the planner always has an indoor fallback.
        if not choices:
            choices = ["Indoor study"]

        domains[day] = choices

    return domains


def revise(domains, x, y):
    changed = False

    for activity in domains[x][:]:
        if not any(
            compatible(activity, other)
            for other in domains[y]
        ):
            domains[x].remove(activity)
            changed = True

    return changed


def ac3(domains):
    """AC-3: propagate constraints between adjacent days."""

    queue = [
        (DAYS[i], DAYS[j])
        for i in range(len(DAYS))
        for j in range(len(DAYS))
        if abs(i - j) == 1
    ]

    while queue:
        x, y = queue.pop(0)

        if revise(domains, x, y):
            if not domains[x]:
                return False

            for z in DAYS:
                if z != y and abs(DAYS.index(z) - DAYS.index(x)) == 1:
                    queue.append((z, x))

    return True


def backtrack(plan, domains, forecasts, counter):
    """Backtracking search with the smallest-domain-first heuristic."""

    counter[0] += 1

    if len(plan) == len(DAYS):
        return plan.copy()

    unassigned = [day for day in DAYS if day not in plan]
    day = min(unassigned, key=lambda d: len(domains[d]))

    candidates = sorted(
        domains[day],
        key=lambda a: expected_utility(a, forecasts[day])
        if a in ACTIVITIES else 0,
        reverse=True
    )

    for activity in candidates:
        consistent = True

        for other_day, other_activity in plan.items():
            if abs(DAYS.index(day) - DAYS.index(other_day)) == 1:
                if not compatible(activity, other_activity):
                    consistent = False
                    break

        if consistent:
            plan[day] = activity
            result = backtrack(plan, domains, forecasts, counter)

            if result is not None:
                return result

            del plan[day]

    return None


def create_weekly_plan(forecasts):
    """Compare domain sizes before and after AC-3, then search."""

    before = make_domains(forecasts)
    after = {day: values[:] for day, values in before.items()}

    before_count = sum(len(values) for values in before.values())
    consistent = ac3(after)
    after_count = sum(len(values) for values in after.values())

    counter = [0]

    if consistent:
        plan = backtrack({}, after, forecasts, counter)
    else:
        plan = None

    return {
        "plan": plan,
        "domains_before": before,
        "domains_after": after,
        "before_count": before_count,
        "after_count": after_count,
        "search_calls": counter[0],
    }
