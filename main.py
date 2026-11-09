import os
from datetime import date

from flask import Flask, render_template, redirect, url_for, flash, Response, jsonify, request, send_from_directory
import psycopg
from functools import wraps
from db.db_create import create_db, create_table
from flask import Flask, jsonify, request, render_template
from psycopg import connect
from psycopg.rows import dict_row
from dotenv import load_dotenv
from pathlib import Path


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')


# Load test.env from the project root
env_path = Path(__file__).resolve().parent.parent / "test.env"
load_dotenv(env_path)
API_KEY = os.getenv("API_KEY")

def init_db():
    create_db()
    create_table()


def get_db_connection():
    return connect(
        host=os.environ.get("DB_HOST"),
        dbname=os.environ.get("DB_NAME"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        port=os.environ.get("DB_PORT"),
        row_factory=dict_row
    )

def require_api_key(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        api_key = request.headers.get("x-api-key")

        if not API_KEY or api_key != API_KEY:
            return jsonify({"error": "Unauthorized"}), 401

        return func(*args, **kwargs)

    return wrapper
@app.route('/')
def home():
    return render_template("index.html")

@app.route("/api/v1/flights/search", methods=["GET"])
@require_api_key
def search_flights():
    origin = request.args.get("origin", "").strip().upper()
    destination = request.args.get("destination", "").strip().upper()
    departure_date = request.args.get("departure_date", "").strip()

    if not origin or not destination or not departure_date:
        return jsonify({
            "error": "Origin, destination and departure date are required"
        }), 400

    query = """
        SELECT
            f.flight_id,
            f.flight_number,
            f.origin,
            f.destination,
            f.departure_date,
            f.departure_time,
            f.price,
            f.total_seats AS seats_available
        FROM flights f
        WHERE f.origin = %s
          AND f.destination = %s
          AND f.departure_date = %s
          AND f.status = 'SCHEDULED'
        ORDER BY f.departure_time;
    """

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (origin, destination, departure_date))
                flights = cur.fetchall()

        results = [
            {
                "flight_id": flight["flight_id"],
                "flight_number": flight["flight_number"],
                "origin": flight["origin"],
                "destination": flight["destination"],
                "departure_date": flight["departure_date"].isoformat(),
                "departure_time": flight["departure_time"].strftime("%H:%M"),
                "price": float(flight["price"]),
                "seats_available": flight["seats_available"]
            }
            for flight in flights
        ]

        return jsonify({
            "count": len(results),
            "flights": results
        })

    except Exception:
        app.logger.exception("Flight search failed")
        return jsonify({"error": "Unable to search flights"}), 500


@app.route("/api/v1/bookings", methods=["POST"])
def create_booking():

    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid request"}), 400

    required_fields = [
        "flight_id",
        "firstname",
        "lastname",
        "email",
        "seats_booked"
    ]

    for field in required_fields:
        if field not in data:
            return jsonify({
                "error": f"Missing required field: {field}"
            }), 400

    conn = get_db_connection()
    cursor = None

    try:
        cursor = conn.cursor()

        seats_booked = int(data["seats_booked"])

        if seats_booked <= 0:
            return jsonify({"error": "Invalid passenger count"}), 400

        # Check flight exists and lock its row
        cursor.execute("""
            SELECT flight_id, total_seats
            FROM flights
            WHERE flight_id = %s
            FOR UPDATE
        """, (data["flight_id"],))

        flight = cursor.fetchone()
        print(flight)

        if not flight:
            return jsonify({"error": "Flight not found"}), 404

        # Check available seats
        if flight['total_seats'] < seats_booked:
            return jsonify({"error": "Not enough seats available"}), 409

        # Create booking
        cursor.execute("""
            INSERT INTO bookings (
                flight_id,
                firstname,
                lastname,
                email,
                seats_booked,
                booking_date,
                status,
                total_price
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING booking_id
        """, (
            data["flight_id"],
            data["firstname"],
            data["lastname"],
            data["email"],
            seats_booked,
            date.today(),
            "CONFIRMED",
            data["total_price"]
        ))

        booking_id = cursor.fetchone()

        # Update remaining seats in flights table
        cursor.execute("""
            UPDATE flights
            SET total_seats = total_seats - %s
            WHERE flight_id = %s
        """, (seats_booked, data["flight_id"]))

        conn.commit()

        return jsonify({
            "booking": {
                "booking_id": booking_id,
                "flight_id": data["flight_id"],
                "firstname": data["firstname"],
                "lastname": data["lastname"],
                "email": data["email"],
                "seats_booked": seats_booked,
                "booking_date": date.today().isoformat(),
                "status": "CONFIRMED",
                "total_price": data["total_price"]
            }
        }), 201

    except Exception as e:
        conn.rollback()
        app.logger.exception("Booking creation failed")
        return jsonify({"error": str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        conn.close()



@app.route("/api/v1/bookings", methods=["GET"])
def get_bookings():

    conn = get_db_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                booking_id,
                flight_id,
                firstname,
                lastname,
                email,
                seats_booked,
                booking_date,
                status
            FROM bookings
            ORDER BY booking_date DESC, booking_id DESC
        """)

        rows = cursor.fetchall()

        bookings = []

        for row in rows:
            bookings.append({
                "booking_id": row["booking_id"],
                "flight_id": row["flight_id"],
                "firstname": row["firstname"],
                "lastname": row["lastname"],
                "email": row["email"],
                "seats_booked": row["seats_booked"],
                "booking_date": row["booking_date"].isoformat()
                    if row["booking_date"] else None,
                "status": row["status"]
            })

        return jsonify({
            "bookings": bookings,
            "count": len(bookings)
        }), 200

    except Exception as e:
        app.logger.exception("Retrieving bookings failed")
        return jsonify({"error": str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        conn.close()


if __name__ == "__main__":
    init_db()
    # app.run(debug=app.config.get("DEBUG", False), port=5002)
    app.run(host="0.0.0.0", port=5002, debug=app.config.get("DEBUG", False))
