
import os
from pathlib import Path

import psycopg
import pytest
from dotenv import load_dotenv


# Load test.env from the project root
PROJECT_ROOT = Path(__file__).resolve().parents[3]
load_dotenv(PROJECT_ROOT / "test.env")


FLIGHTS = [
    ("TS101", "YYZ", "YVR", "2026-11-01", "08:30:00", 289.99, 180, "SCHEDULED"),
    ("TS102", "YYZ", "YVR", "2026-11-01", "14:15:00", 319.50, 180, "SCHEDULED"),
    ("TS103", "YYZ", "YVR", "2026-11-02", "09:00:00", 259.99, 180, "SCHEDULED"),
    ("TS201", "YYZ", "YUL", "2026-11-01", "07:45:00", 149.50, 120, "SCHEDULED"),
    ("TS202", "YYZ", "YUL", "2026-11-02", "16:30:00", 175.00, 120, "SCHEDULED"),
    ("TS301", "YVR", "YYZ", "2026-11-03", "10:00:00", 310.00, 180, "SCHEDULED"),
    ("TS401", "YYZ", "YYC", "2026-11-05", "11:20:00", 225.75, 150, "SCHEDULED"),
    ("TS402", "YYZ", "YYC", "2026-11-05", "18:45:00", 199.99, 150, "SCHEDULED"),
    ("TS501", "YUL", "YYZ", "2026-11-07", "13:00:00", 139.00, 120, "SCHEDULED"),
    ("TS601", "YYZ", "JFK", "2026-11-10", "09:15:00", 275.00, 160, "SCHEDULED"),
    ("TS701", "YYZ", "LHR", "2026-11-12", "21:30:00", 799.99, 250, "SCHEDULED"),
    ("TS801", "YYZ", "YVR", "2026-11-15", "06:00:00", 0.00, 0, "SCHEDULED"),
]


@pytest.fixture(autouse=True)
def reset_database():
    """Reset the test data before every API test."""

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