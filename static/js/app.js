
// ==========================================
// SkyTrail - Flight Booking
// ==========================================

var API_BASE = "/api/v1";

var searchForm = document.getElementById("flight-search-form");
var originSelect = document.getElementById("origin");
var destinationSelect = document.getElementById("destination");
var departureDateInput = document.getElementById("departure-date");
var passengersSelect = document.getElementById("passengers");
var swapButton = document.getElementById("swap-airports");
var searchButton = document.getElementById("search-flights-button");
var searchMessage = document.getElementById("search-message");

var resultsSection = document.getElementById("flight-results-section");
var resultsContainer = document.getElementById("flight-results");
var resultsCount = document.getElementById("results-count");

var bookingPanel = document.getElementById("booking-panel");
var bookingForm = document.getElementById("booking-form");
var bookingMessage = document.getElementById("booking-message");
var flightIdInput = document.getElementById("flight-id");
var selectedFlightSummary =
    document.getElementById("selected-flight-summary");

var confirmationPanel = document.getElementById("confirmation-panel");
var confirmationDetails =
    document.getElementById("confirmation-details");

var bookingsList = document.getElementById("bookings-list");
var bookingsMessage = document.getElementById("bookings-message");

var availableFlights = [];
var selectedFlight = null;


// ==========================================
// Helper functions
// ==========================================

function formatPrice(price) {
    return new Intl.NumberFormat("en-CA", {
        style: "currency",
        currency: "CAD"
    }).format(Number(price));
}


function formatDate(dateString) {
    var date = new Date(dateString + "T00:00:00");

    return date.toLocaleDateString("en-CA", {
        year: "numeric",
        month: "short",
        day: "numeric"
    });
}


function setMessage(element, message, isError) {
    element.textContent = message;
    element.classList.toggle("error", Boolean(isError));
}


function getFlightId(flight) {
    return flight.flight_id || flight.flightid;
}


function getAvailableSeats(flight) {
    var seats = flight.seats_available;

    if (seats === undefined || seats === null) {
        seats = flight.available_seats;
    }

    return Number(seats || 0);
}


function clearElement(element) {
    while (element.firstChild) {
        element.removeChild(element.firstChild);
    }
}


function addTextElement(parent, tagName, className, text) {
    var element = document.createElement(tagName);

    if (className) {
        element.className = className;
    }

    element.textContent = text;
    parent.appendChild(element);

    return element;
}


function hideBookingSections() {
    bookingPanel.hidden = true;
    confirmationPanel.hidden = true;
}


// ==========================================
// API request helper
// ==========================================

async function apiRequest(url, options) {
    options = options || {};

    var requestHeaders = {
        "Accept": "application/json"
    };

    var requestOptions = {
        method: options.method || "GET",
        headers: requestHeaders
    };

    if (options.body !== undefined) {
        requestHeaders["Content-Type"] = "application/json";
        requestOptions.body = options.body;
    }

    var response = await fetch(url, requestOptions);

    var data = await response.json().catch(function () {
        return {};
    });

    if (!response.ok) {
        var errorMessage =
            data.error ||
            data.message ||
            ("Request failed with status " + response.status);

        throw new Error(errorMessage);
    }

    return data;
}


// ==========================================
// Date setup
// ==========================================

function getLocalDateString() {
    var date = new Date();
    var year = date.getFullYear();
    var month = String(date.getMonth() + 1).padStart(2, "0");
    var day = String(date.getDate()).padStart(2, "0");

    return year + "-" + month + "-" + day;
}

departureDateInput.min = getLocalDateString();


// ==========================================
// Swap airports
// ==========================================

swapButton.addEventListener("click", function () {
    var originalOrigin = originSelect.value;

    originSelect.value = destinationSelect.value;
    destinationSelect.value = originalOrigin;
});


// ==========================================
// Search flights
// GET /api/v1/flights/search
// ==========================================

searchForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    var origin = originSelect.value;
    var destination = destinationSelect.value;
    var departureDate = departureDateInput.value;
    var passengers = Number(passengersSelect.value);

    if (origin === destination) {
        setMessage(
            searchMessage,
            "Origin and destination must be different.",
            true
        );
        return;
    }

    if (!departureDate) {
        setMessage(
            searchMessage,
            "Please select a departure date.",
            true
        );
        return;
    }

    if (departureDate < getLocalDateString()) {
        setMessage(
            searchMessage,
            "Departure date cannot be in the past.",
            true
        );
        return;
    }

    availableFlights = [];
    selectedFlight = null;

    clearElement(resultsContainer);
    resultsSection.hidden = true;
    hideBookingSections();

    searchButton.disabled = true;

    setMessage(searchMessage, "Searching for flights...", false);

    var queryString =
        "origin=" + encodeURIComponent(origin) +
        "&destination=" + encodeURIComponent(destination) +
        "&departure_date=" + encodeURIComponent(departureDate);

    var searchUrl = API_BASE + "/flights/search?" + queryString;

    try {
        var data = await apiRequest(searchUrl);
        var flights = Array.isArray(data) ? data : data.flights;

        if (!Array.isArray(flights)) {
            throw new Error("Unexpected response from the flight search API.");
        }

        availableFlights = flights.filter(function (flight) {
            return getAvailableSeats(flight) >= passengers;
        });

        resultsSection.hidden = false;

        if (availableFlights.length === 0) {
            resultsCount.textContent = "0 flights";

            if (flights.length === 0) {
                setMessage(
                    searchMessage,
                    "No flights found for your search.",
                    false
                );
            } else {
                setMessage(
                    searchMessage,
                    "Flights were found, but there are not enough seats for your passengers.",
                    false
                );
            }

            return;
        }

        var countText = availableFlights.length === 1
            ? "1 flight"
            : availableFlights.length + " flights";

        resultsCount.textContent = countText;

        renderFlights(availableFlights, passengers);

        setMessage(
            searchMessage,
            countText + " found.",
            false
        );

    } catch (error) {
        console.error("Flight search failed:", error);

        setMessage(
            searchMessage,
            "Unable to search flights: " + error.message,
            true
        );

    } finally {
        searchButton.disabled = false;
    }
});


// ==========================================
// Display search results
// ==========================================

function renderFlights(flights, passengers) {
    clearElement(resultsContainer);

    flights.forEach(function (flight) {
        var card = document.createElement("article");
        card.className = "flight-card";

        var details = document.createElement("div");
        details.className = "flight-details";

        addTextElement(
            details,
            "p",
            "eyebrow",
            flight.flight_number
        );

        addTextElement(
            details,
            "h3",
            "",
            flight.origin + " \u2192 " + flight.destination
        );

        addTextElement(
            details,
            "p",
            "",
            formatDate(flight.departure_date)
        );

        addTextElement(
            details,
            "p",
            "",
            "Departure: " + flight.departure_time
        );

        addTextElement(
            details,
            "p",
            "",
            getAvailableSeats(flight) + " seat(s) available"
        );

        var priceDetails = document.createElement("div");
        priceDetails.className = "flight-price";

        addTextElement(
            priceDetails,
            "h3",
            "",
            formatPrice(flight.price)
        );

        addTextElement(
            priceDetails,
            "p",
            "",
            "per passenger"
        );

        var totalPrice = Number(flight.price) * passengers;

        addTextElement(
            priceDetails,
            "p",
            "",
            "Total: " + formatPrice(totalPrice)
        );

        var selectButton = document.createElement("button");
        selectButton.type = "button";
        selectButton.className = "primary-button";
        selectButton.textContent = "Select flight";

        selectButton.addEventListener("click", function () {
            selectFlight(flight, passengers);
        });

        priceDetails.appendChild(selectButton);
        card.appendChild(details);
        card.appendChild(priceDetails);
        resultsContainer.appendChild(card);
    });
}


// ==========================================
// Select a flight
// ==========================================

function selectFlight(flight, passengers) {
    selectedFlight = flight;

    bookingForm.reset();
    flightIdInput.value = getFlightId(flight);

    clearElement(selectedFlightSummary);

    addTextElement(
        selectedFlightSummary,
        "h3",
        "",
        flight.origin + " \u2192 " + flight.destination
    );

    addTextElement(
        selectedFlightSummary,
        "p",
        "",
        "Flight: " + flight.flight_number
    );

    addTextElement(
        selectedFlightSummary,
        "p",
        "",
        "Date: " + formatDate(flight.departure_date)
    );

    addTextElement(
        selectedFlightSummary,
        "p",
        "",
        "Departure: " + flight.departure_time
    );

    addTextElement(
        selectedFlightSummary,
        "p",
        "",
        "Passengers: " + passengers
    );

    addTextElement(
        selectedFlightSummary,
        "p",
        "",
        "Total: " + formatPrice(Number(flight.price) * passengers)
    );

    document.getElementById("checkin").value = flight.departure_date;
    document.getElementById("checkout").value = "";

    setMessage(bookingMessage, "", false);

    bookingPanel.hidden = false;
    confirmationPanel.hidden = true;

    bookingPanel.scrollIntoView({
        behavior: "smooth",
        block: "start"
    });
}


// ==========================================
// Return to flight results
// ==========================================

document.getElementById("back-to-results").addEventListener(
    "click",
    function () {
        bookingPanel.hidden = true;
        resultsSection.hidden = false;

        resultsSection.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });
    }
);


// ==========================================
// Create booking
// POST /api/v1/bookings
// ==========================================

bookingForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    if (!selectedFlight) {
        setMessage(
            bookingMessage,
            "Please select a flight first.",
            true
        );
        return;
    }

    var passengers = Number(passengersSelect.value);

    if (getAvailableSeats(selectedFlight) < passengers) {
        setMessage(
            bookingMessage,
            "There are not enough seats available.",
            true
        );
        return;
    }

    var checkin = document.getElementById("checkin").value;
    var checkout = document.getElementById("checkout").value;

    if (checkout && checkin && checkout <= checkin) {
        setMessage(
            bookingMessage,
            "Check-out date must be after check-in date.",
            true
        );
        return;
    }

    var booking = {
        flight_id: getFlightId(selectedFlight),
        firstname: document.getElementById("firstname").value.trim(),
        lastname: document.getElementById("lastname").value.trim(),
        email: document.getElementById("email").value.trim(),
        seats_booked: passengers,
        checkin: checkin,
        checkout: checkout,
        additionalneeds:
            document.getElementById("additionalneeds").value.trim(),
        depositpaid: document.getElementById("depositpaid").checked
    };

    var confirmButton =
        document.getElementById("confirm-booking-button");

    confirmButton.disabled = true;

    setMessage(bookingMessage, "Creating your booking...", false);

    try {
        var data = await apiRequest(API_BASE + "/bookings", {
            method: "POST",
            body: JSON.stringify(booking)
        });

        var savedBooking = data.booking || data;

        showConfirmation(savedBooking, selectedFlight, passengers);

        loadBookings();

    } catch (error) {
        console.error("Booking failed:", error);

        setMessage(
            bookingMessage,
            "Unable to create booking: " + error.message,
            true
        );

    } finally {
        confirmButton.disabled = false;
    }
});


// ==========================================
// Booking confirmation
// ==========================================

function showConfirmation(booking, flight, passengers) {
    clearElement(confirmationDetails);

    var reference =
        booking.bookingid ||
        booking.booking_id ||
        booking.id ||
        "Created";

    addTextElement(
        confirmationDetails,
        "p",
        "",
        "Booking reference: " + reference
    );

    addTextElement(
        confirmationDetails,
        "p",
        "",
        "Route: " + flight.origin + " \u2192 " + flight.destination
    );

    addTextElement(
        confirmationDetails,
        "p",
        "",
        "Flight: " + flight.flight_number
    );

    addTextElement(
        confirmationDetails,
        "p",
        "",
        "Passengers: " + passengers
    );

    addTextElement(
        confirmationDetails,
        "p",
        "",
        "Total: " + formatPrice(Number(flight.price) * passengers)
    );

    bookingPanel.hidden = true;
    resultsSection.hidden = true;
    confirmationPanel.hidden = false;

    confirmationPanel.scrollIntoView({
        behavior: "smooth",
        block: "start"
    });
}


// ==========================================
// Book another flight
// ==========================================

document.getElementById("book-another-flight").addEventListener(
    "click",
    function () {
        selectedFlight = null;

        bookingForm.reset();

        confirmationPanel.hidden = true;
        bookingPanel.hidden = true;
        resultsSection.hidden = true;

        clearElement(resultsContainer);

        setMessage(searchMessage, "", false);

        document.getElementById("search-panel").scrollIntoView({
            behavior: "smooth",
            block: "start"
        });
    }
);


// ==========================================
// Retrieve bookings
// GET /api/v1/bookings
// ==========================================

document.getElementById("refresh-bookings").addEventListener(
    "click",
    function () {
        loadBookings();
    }
);


async function loadBookings() {
    clearElement(bookingsList);

    setMessage(bookingsMessage, "Loading bookings...", false);

    try {
        var data = await apiRequest(API_BASE + "/bookings");
        var bookings = Array.isArray(data) ? data : data.bookings;

        if (!Array.isArray(bookings)) {
            throw new Error("Unexpected response from the bookings API.");
        }

        if (bookings.length === 0) {
            addTextElement(
                bookingsList,
                "p",
                "muted",
                "No bookings found."
            );

            setMessage(bookingsMessage, "", false);
            return;
        }

        bookings.forEach(function (booking) {
            var card = document.createElement("article");
            card.className = "booking-card";

            var reference =
                booking.bookingid ||
                booking.booking_id ||
                booking.id ||
                "N/A";

            addTextElement(
                card,
                "h3",
                "",
                "Booking #" + reference
            );

            addTextElement(
                card,
                "p",
                "",
                ((booking.firstname || "") + " " +
                (booking.lastname || "")).trim()
            );

            addTextElement(
                card,
                "p",
                "",
                "Flight: " +
                (booking.flight_number ||
                booking.flight_id ||
                booking.flightid ||
                "N/A")
            );

            addTextElement(
                card,
                "p",
                "",
                "Status: " + (booking.status || "CONFIRMED")
            );

            addTextElement(
                card,
                "p",
                "",
                "Passengers: " + (booking.seats_booked || 1)
            );

            bookingsList.appendChild(card);
        });

        setMessage(
            bookingsMessage,
            bookings.length + " booking(s) loaded.",
            false
        );

    } catch (error) {
        console.error("Loading bookings failed:", error);

        setMessage(
            bookingsMessage,
            "Unable to load bookings: " + error.message,
            true
        );
    }
}
