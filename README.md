
## Project overview
This project extends a weather-based activity agent into a
health-aware decision support system.

## AI concepts demonstrated
1. Rule-based health-risk assessment using AQI and heat index.
2. Forward chaining for recommendations.
3. Backward chaining for questions about a selected activity.
4. Uncertain forecast reasoning using illustrative safety estimates.
5. Expected utility for comparing activity choices.
6. Constraint Satisfaction Problem (CSP) for weekly activity planning.
7. AC-3 constraint propagation.
8. Backtracking search with a smallest-domain-first heuristic.
9. Explanations and a medical disclaimer.

## Inputs
For each day, the user enters:
- Rain probability
- Temperature
- Air Quality Index (AQI)
- Heat index
- Availability

## Run the project
From the project root:

```bash
python src/main.py
```

## Run tests

```bash
python -m unittest discover -s tests -v
```

## Important limitation
This is an educational prototype. The safety estimates and health
thresholds are illustrative, not medically validated. The system
does not diagnose conditions and does not replace professional
medical advice or official weather and air-quality guidance.
