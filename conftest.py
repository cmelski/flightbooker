import os
import pytest
from pathlib import Path
from dotenv import load_dotenv
from qa.services.flight_service import FlightService

PROJECT_ROOT = Path(__file__).resolve().parent
ENV_PATH = PROJECT_ROOT / "test.env"
load_dotenv(ENV_PATH, override=True)


@pytest.fixture(scope="session")
def base_url():
    return os.environ["BASE_URL"]


@pytest.fixture
def flight_service(base_url):
    return FlightService(base_url)
