import os
from pathlib import Path
import psycopg
from dotenv import load_dotenv

file_path = Path(__file__).parent.parent / "test.env"
load_dotenv(file_path)


def create_db():
    try:
        # Connect to the default database (e.g. 'postgres')
        with psycopg.connect(
                host=os.environ.get('DB_HOST'),
                dbname=os.environ.get('DB_NAME_DEFAULT'),
                user=os.environ.get('DB_USER'),
                password=os.environ.get('DB_PASSWORD'),
                port=os.environ.get('DB_PORT')
        ) as conn:
            # Enable autocommit mode
            conn.autocommit = True

            with conn.cursor() as cur:
                db_name = os.environ.get('DB_NAME')
                cur.execute(f"CREATE DATABASE {db_name};")
                print("Database created successfully!")

    except psycopg.Error as e:
        print(f"Duplicate DB: {e}")


def create_table():
    # Connect to your target database
    with psycopg.connect(
            dbname=os.environ.get('DB_NAME'),
            user=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PASSWORD'),
            host=os.environ.get('DB_HOST'),
            port=os.environ.get('DB_PORT')
    ) as conn:
        conn.autocommit = True  # Apply changes immediately (no explicit commit needed)

        with conn.cursor() as cur:
            # task table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS flights (
                    flight_id SERIAL PRIMARY KEY,
                    flight_number VARCHAR(10) NOT NULL,
                    origin VARCHAR(3) NOT NULL,
                    destination VARCHAR(3) NOT NULL,
                    departure_date DATE NOT NULL,
                    departure_time TIME NOT NULL,
                    price DECIMAL(10, 2) NOT NULL,
                    total_seats INTEGER NOT NULL,
                    status VARCHAR(20) NOT NULL DEFAULT 'SCHEDULED'
                );
            """)

            cur.execute("""
                CREATE TABLE IF NOT EXISTS bookings (
                    booking_id SERIAL PRIMARY KEY,
                    flight_id INTEGER NOT NULL REFERENCES flights(flight_id),
                    firstname VARCHAR(100) NOT NULL,
                    lastname VARCHAR(100) NOT NULL,
                    email VARCHAR(255) NOT NULL,
                    seats_booked INTEGER NOT NULL DEFAULT 1,
                    booking_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    status VARCHAR(20) NOT NULL DEFAULT 'CONFIRMED'
                );
            """)
