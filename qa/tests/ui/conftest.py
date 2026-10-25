from playwright.sync_api import sync_playwright
import pytest
import os
from pathlib import Path
from dotenv import load_dotenv

# Load test.env from the project root
PROJECT_ROOT = Path(__file__).resolve().parents[3]
load_dotenv(PROJECT_ROOT / "test.env")


@pytest.fixture(scope="function")
def page_instance():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        base_url = os.environ["BASE_URL"]
        page.goto(base_url)
        yield page
        context.close()
        browser.close()
