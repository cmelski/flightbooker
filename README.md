# SkyTrail – Flight Booking & Test Automation

## Overview

SkyTrail is a flight booking application built with Flask, PostgreSQL, HTML, CSS and JavaScript.

The project includes an automated testing framework using Python, pytest, Requests and Playwright. It covers API testing and browser-based UI testing, with a focus on validating flight search functionality and booking workflows.

## Technologies

* Python
* Flask REST API
* PostgreSQL
* pytest
* Requests
* Playwright
* python-dotenv

## Project Structure

```text
skytrail/
├── app.py
├── test.env
├── qa/
│   ├── core/
│   │   └── api_client.py
│   ├── services/
│   │   └── flight_service.py
│   └── tests/
│       ├── conftest.py
│       ├── api/
│       │   └── test_flight_search_api.py
│       └── ui/
│           └── test_flight_search_ui.py
├── templates/
├── static/
└── README.md
```

## Framework Design

The automation framework is organised into three layers:

* **Core:** Shared functionality, including API clients and framework configuration.
* **Services:** Reusable operations for interacting with application functionality, such as searching for flights and creating bookings.
* **Tests:** API and UI test cases that validate application behaviour and expected results.

## API Testing

API tests use pytest and Requests to validate REST endpoints.

Current coverage includes:

* Successful flight searches.
* Response structure and required fields.
* Flight count and returned results.
* Matching origin, destination and departure date.

## UI Testing

UI tests use Playwright with pytest to validate the application through a browser.

Planned coverage includes:

* Flight search form validation.
* Searching for available flights.
* Displaying flight results.
* Selecting a flight and submitting passenger details.
* Booking confirmation and booking history.
* Handling invalid input and unsuccessful searches.

## Configuration

Create a `test.env` file in the project root:

```text
BASE_URL=http://127.0.0.1:5002
```

Configure the PostgreSQL connection settings required by the application.

Install the dependencies:

```bash
pip install flask "psycopg[binary]" pytest requests python-dotenv pytest-playwright
```

Install the Playwright browser:

```bash
playwright install chromium
```

## Running the Application

Start the Flask application:

```bash
python app.py
```

Ensure the application and PostgreSQL database are running before executing the tests.

## Running the Tests

Run all tests:

```bash
python -m pytest -v
```

Run API tests only:

```bash
python -m pytest -v qa/tests/api/
```

Run UI tests only:

```bash
python -m pytest -v qa/tests/ui/
```

## Future Improvements

* Add response schema validation.
* Expand negative and boundary testing.
* Add API and UI booking workflow coverage.
* Generate test reports using Allure.
* Integrate automated tests into GitHub Actions.
