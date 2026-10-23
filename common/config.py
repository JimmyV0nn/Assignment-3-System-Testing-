"""Shared settings for all test modules."""
import os

BASE_URL = "https://opencart.abstracta.us/"

# Seconds to wait for elements before failing
DEFAULT_TIMEOUT = 15

# Set HEADLESS=1 to run without opening a browser window
HEADLESS = os.getenv("HEADLESS", "0") == "1"

# Password used for freshly registered test accounts
DEFAULT_PASSWORD = "Test@12345"

SCREENSHOT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "screenshots")


def url(route: str) -> str:
    """Build a full URL for an OpenCart route, e.g. url("account/login")."""
    return f"{BASE_URL}?route={route}"
