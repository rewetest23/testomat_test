import pytest
from playwright.sync_api import Browser, BrowserContext, Page

from fixtures.config import Config


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args: dict) -> dict:
    return {
        **browser_type_launch_args,
        "channel": "chrome",
        "headless": False,
        "slow_mo": 0,
        "timeout": 30000,  # Timeout for Browser-Start
    }


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: dict, configs: Config) -> dict:
    return {
        **browser_context_args,
        "base_url": configs.base_app_url,
        "viewport": {"width": 1920, "height": 1080},
        "locale": "uk_UA",
        "timezone_id": "Europe/Kyiv",
        "record_video_dir": "/videos",
        "permissions": ["geolocation"],
        "timeout": 30000,  # Standard-Action-Timeout
    }


def create_context_and_page(browser: Browser, context_args: dict) -> tuple[BrowserContext, Page]:
    """Helper to create a new browser context and page with the configured args."""
    context = browser.new_context(**context_args)
    page = context.new_page()
    return context, page
