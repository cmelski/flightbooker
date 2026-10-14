import os
from flask import Flask, render_template, redirect, url_for, flash, Response, jsonify, request, send_from_directory
import psycopg
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

@app.route('/')
def home():
    return render_template("index.html")

@app.route("/api/v1/flights/search", methods=["GET"])
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
            f.total_seats - COALESCE(
                (
                    SELECT SUM(b.seats_booked)
                    FROM bookings b
                    WHERE b.flight_id = f.flight_id
                      AND b.status = 'CONFIRMED'
                ), 0
            ) AS seats_available
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





if __name__ == "__main__":
    init_db()
    # app.run(debug=app.config.get("DEBUG", False), port=5002)
    app.run(host="0.0.0.0", port=5002, debug=app.config.get("DEBUG", False))
