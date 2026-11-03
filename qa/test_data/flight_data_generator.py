from datetime import date
from qa.core.utilities.common_utilities import flight_date


def get_flight_parameters():
    flight_data = [
        {'origin': 'YYZ',
         'destination': 'YVR',
         'departure_date': date.today().strftime("%Y-%m-%d"),
         'expected_status_code': 200
         },

        {'origin': 'YYZ',
         'destination': 'YVR',
         'departure_date': '2026-11-0',
         'expected_status_code': 500
         },
        {'origin': 'YYZ',
         'destination': 'YVR',
         'departure_date': '',
         'expected_status_code': 400
         },
    ]
    return flight_data

def get_initial_flight_records_for_db():
    return [
        (101, "TS101", "YYZ", "YVR", flight_date(0), "08:30:00", 289.99, 180, "SCHEDULED"),
        (102, "TS102", "YYZ", "YVR", flight_date(0), "14:15:00", 319.50, 180, "SCHEDULED"),

        (103, "TS103", "YYZ", "YVR", flight_date(1), "09:00:00", 259.99, 180, "SCHEDULED"),
        (104, "TS201", "YYZ", "YUL", flight_date(1), "07:45:00", 149.50, 120, "SCHEDULED"),

        (105, "TS202", "YYZ", "YUL", flight_date(2), "16:30:00", 175.00, 120, "SCHEDULED"),

        (106, "TS301", "YVR", "YYZ", flight_date(3), "10:00:00", 310.00, 180, "SCHEDULED"),

        (107, "TS401", "YYZ", "YYC", flight_date(5), "11:20:00", 225.75, 150, "SCHEDULED"),
        (108, "TS402", "YYZ", "YYC", flight_date(5), "18:45:00", 199.99, 150, "SCHEDULED"),

        (109, "TS501", "YUL", "YYZ", flight_date(7), "13:00:00", 139.00, 120, "SCHEDULED"),

        (110, "TS601", "YYZ", "JFK", flight_date(10), "09:15:00", 275.00, 160, "SCHEDULED"),

        (111, "TS701", "YYZ", "LHR", flight_date(12), "21:30:00", 799.99, 250, "SCHEDULED"),

        (112, "TS801", "YYZ", "YVR", flight_date(15), "06:00:00", 0.00, 0, "SCHEDULED"),
    ]
