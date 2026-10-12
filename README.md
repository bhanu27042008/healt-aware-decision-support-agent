Weather-Based Activity Agent 🌦️

A Python-based Artificial Intelligence project that recommends suitable indoor and outdoor activities according to weather conditions entered by the user.

1. Project Overview

The Weather-Based Activity Agent is a rule-based rational agent developed for IA-1. It observes weather information, applies predefined decision rules, and recommends activities based on the available conditions.

The objective is to demonstrate how an intelligent agent perceives its environment and chooses an appropriate action to achieve a simple goal: recommending suitable activities while considering weather-related risks.

Current version: 1.0
Programming language: Python
Interface: Command-line / terminal application
Weather input: Manual user input

2. Objectives

- Develop a simple rational agent using Python.
- Recommend activities based on temperature, rain probability, wind speed, and weather conditions.
- Apply decision rules to select suitable activities.
- Handle missing or incomplete weather information.
- Explain the reasons behind the agent's recommendations.
- Verify the program using automated unit tests.

3. Technologies Used

- Python 3
- Visual Studio Code (VS Code)
- Git and GitHub
- Python "unittest" module

No external Python packages are required for the current implementation.

4. Repository Structure

WEATHER-ACTIVITY-DECISION-MAKING/
├── src/
│   ├── agent.py
│   └── main.py
├── tests/
│   └── test_agent.py
├── docs/
│   └── (project report and screenshots)
├── README.md
├── requirements.txt
├── .gitignore
└── LICENSE

5. How the Agent Works

The application follows these steps:

1. Perceive: Collect temperature, probability of rain, wind speed, and a weather description from the user.
2. Validate: Check numerical inputs and reject values outside the accepted ranges.
3. Reason: Apply predefined rules to evaluate weather conditions.
4. Decide: Recommend indoor activities when conditions are unsuitable for outdoor plans, or outdoor activities when the available data indicates suitable conditions.
5. Explain: Display the recommendations, reasons, and warnings about missing information.

Decision Rules

Weather condition| Agent's response
Suitable temperature, low rain chance, and light wind| Recommend outdoor activities
High probability of rain| Prefer indoor activities
Very high temperature| Prefer indoor activities and avoid strenuous outdoor activity
Very low temperature| Prefer a comfortable indoor setting
Strong wind| Prefer indoor activities
Thunderstorm or other configured severe-weather conditions| Recommend indoor activities
Missing weather information| Display warnings and use a cautious fallback

These rules are simplified educational rules, not a substitute for official weather alerts or professional health advice.

6. Installation and Execution

Prerequisites

Install Python 3 and Visual Studio Code. Ensure Python is available from your terminal.

Run the application

Clone the repository and enter the project directory:

git clone <YOUR_GITHUB_REPOSITORY_URL>
cd WEATHER-ACTIVITY-DECISION-MAKING

Run the program from the project root:

python src/main.py

On Windows, use "py src/main.py" if the "python" command is unavailable.

The program will ask you to enter the weather details in the terminal.

7. Example Input and Output

Example input

Temperature in °C: 28
Chance of rain in %: 10
Wind speed in km/h: 8
Weather condition: sunny

Expected recommendations

Walking or cycling
Outdoor sports or a picnic

The application also provides reasons for its decisions. Exact output depends on the implementation and the values entered.

This example uses manually entered sample data; it is not a live forecast.

8. Testing

The project includes automated tests in "tests/test_agent.py".

The tests cover:

- Suitable weather and outdoor recommendations.
- High probability of rain.
- Severe weather.
- Missing weather information.
- Invalid temperature values.
- Empty weather input.

Run the tests from the project root:

python -m unittest discover -s tests -p "test_*.py" -v

A successful run should report six tests and finish with "OK".

9. Limitations

- Weather data is entered manually rather than retrieved from a live API.
- The decision rules cover only selected weather conditions.
- The system does not guarantee that an activity is safe in every situation.
- Air quality, humidity, official weather warnings, and individual health needs are not currently evaluated.

Users should follow official weather alerts and relevant safety guidance.

10. Future Enhancements — IA-2

The project can be extended into a Health-Aware Decision Support Agent with:

- A weekly activity planner using Constraint Satisfaction Problems (CSP).
- Backtracking and AC-3 constraint propagation.
- Forward chaining and backward chaining for rule-based reasoning.
- Heat-stress and air-quality risk indicators.
- Bayesian reasoning or certainty factors for uncertain forecasts.
- Expected-utility calculations to compare activity choices.
- Clear explanations and responsible-AI safeguards.

11. References

- Python documentation: https://docs.python.org/3/
- Python "unittest" documentation: https://docs.python.org/3/library/unittest.html
- Git documentation: https://git-scm.com/doc

12. Academic Integrity

This project is intended for educational use. The author should understand the implementation, verify the results, and acknowledge external resources used in the project.

---

Developed as an Artificial Intelligence IA-1 project.