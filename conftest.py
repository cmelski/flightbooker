import os
import pytest
import psycopg
from playwright.sync_api import sync_playwright
from pathlib import Path
from dotenv import load_dotenv
from qa.services.flight_service import FlightService
from qa.core.db_client import DBClient
from qa.test_data.flight_data_generator import get_initial_flight_records_for_db

PROJECT_ROOT = Path(__file__).resolve().parent
ENV_PATH = PROJECT_ROOT / "test.env"
load_dotenv(ENV_PATH, override=True)
TABLES_TO_TRUNCATE = ['bookings', 'flights']


def get_db_connection_params():
    return {
        "host": os.environ["DB_HOST"],
        "dbname": os.environ["DB_NAME"],
        "user": os.environ["DB_USER"],
        "password": os.environ["DB_PASSWORD"],
        "port": os.getenv("DB_PORT"),
    }


@pytest.fixture()
def db_client():

    client = DBClient(get_db_connection_params())
    yield client
    client.close()


@pytest.fixture(autouse=True)
def reset_database(db_client):
    """Reset the test data before every test."""

    for table in TABLES_TO_TRUNCATE:
        db_client.cursor.execute(
            f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE"
        )

    db_client.cursor.executemany(
        """
        INSERT INTO flights (
            flight_id,
            flight_number,
            origin,
            destination,
            departure_date,
            departure_time,
            price,
            total_seats,
            status
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        get_initial_flight_records_for_db()
    )

    db_client.commit()

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
