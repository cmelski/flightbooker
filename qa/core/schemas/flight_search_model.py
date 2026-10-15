
from datetime import date, time
from pydantic import BaseModel, ConfigDict, Field, model_validator


class Flight(BaseModel):
    model_config = ConfigDict(extra="forbid")

    flight_id: int
    flight_number: str
    origin: str
    destination: str
    departure_date: date
    departure_time: time
    price: float = Field(ge=0)
    seats_available: int = Field(ge=0)


class FlightSearchResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    count: int = Field(ge=0)
    flights: list[Flight]

    @model_validator(mode="after")
    def validate_count(self):
        if self.count != len(self.flights):
            raise ValueError(
                "count must match the number of flights returned"
            )
        return self