import os
import pytest
import psycopg
from playwright.sync_api import sync_playwright
from pathlib import Path
from dotenv import load_dotenv
from qa.services.flight_service import FlightService
from qa.core.utilities.common_utilities import flight_date
PROJECT_ROOT = Path(__file__).resolve().parent
ENV_PATH = PROJECT_ROOT / "test.env"
load_dotenv(ENV_PATH, override=True)


@pytest.fixture(autouse=True)
def reset_database():
    """Reset the test data before every test."""

    FLIGHTS = [
        # Today
        ("TS101", "YYZ", "YVR", flight_date(0), "08:30:00", 289.99, 180, "SCHEDULED"),
        ("TS102", "YYZ", "YVR", flight_date(0), "14:15:00", 319.50, 180, "SCHEDULED"),

        # Tomorrow
        ("TS103", "YYZ", "YVR", flight_date(1), "09:00:00", 259.99, 180, "SCHEDULED"),
        ("TS201", "YYZ", "YUL", flight_date(1), "07:45:00", 149.50, 120, "SCHEDULED"),

        # Two days from now
        ("TS202", "YYZ", "YUL", flight_date(2), "16:30:00", 175.00, 120, "SCHEDULED"),

        # Three days from now
        ("TS301", "YVR", "YYZ", flight_date(3), "10:00:00", 310.00, 180, "SCHEDULED"),

        # Five days from now
        ("TS401", "YYZ", "YYC", flight_date(5), "11:20:00", 225.75, 150, "SCHEDULED"),
        ("TS402", "YYZ", "YYC", flight_date(5), "18:45:00", 199.99, 150, "SCHEDULED"),

        # Seven days from now
        ("TS501", "YUL", "YYZ", flight_date(7), "13:00:00", 139.00, 120, "SCHEDULED"),

        # Ten days from now
        ("TS601", "YYZ", "JFK", flight_date(10), "09:15:00", 275.00, 160, "SCHEDULED"),

        # Twelve days from now
        ("TS701", "YYZ", "LHR", flight_date(12), "21:30:00", 799.99, 250, "SCHEDULED"),

        # Fifteen days from now
        ("TS801", "YYZ", "YVR", flight_date(15), "06:00:00", 0.00, 0, "SCHEDULED"),
    ]

    connection_params = {
        "host": os.environ["DB_HOST"],
        "dbname": os.environ["DB_NAME"],
        "user": os.environ["DB_USER"],
        "password": os.environ["DB_PASSWORD"],
        "port": os.getenv("DB_PORT"),
    }

    with psycopg.connect(**connection_params) as conn:
        with conn.cursor() as cur:
            # Remove existing data and reset generated IDs
            cur.execute(
                "TRUNCATE TABLE bookings, flights "
                "RESTART IDENTITY CASCADE"
            )

            # Insert the standard test flights
            cur.executemany(
                """
                INSERT INTO flights (
                    flight_number,
                    origin,
                    destination,
                    departure_date,
                    departure_time,
                    price,
                    total_seats,
                    status
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                FLIGHTS,
            )


@pytest.fixture(scope="session")
def base_url():
    return os.environ["BASE_URL"]


@pytest.fixture(scope="session")
def api_key():
    return os.environ["API_KEY"]


@pytest.fixture
def flight_service(base_url, api_key):
    headers = {
        'x-api-key': api_key
    }
    flight_service = FlightService(base_url, headers)
    yield flight_service
    flight_service.api_client.session.close()


@pytest.fixture(scope="function")
def page_instance():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        base_url = os.environ["BASE_URL"]
        page.goto(base_url)
        try:
            yield page
        finally:
            context.close()
            browser.close()
