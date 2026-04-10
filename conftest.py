import os
from dataclasses import dataclass

import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page, Browser, BrowserContext

from src.web.app import App

load_dotenv()


@dataclass(frozen=True)
class Config:
    base_url: str
    base_app_url: str
    sign_in_url: str
    email: str
    password: str


@pytest.fixture(scope="session")
def configs():
    return Config(
        base_url=os.getenv("BASE_URL"),
        base_app_url=os.getenv("BASE_APP_URL"),
        sign_in_url=f"{os.getenv('BASE_APP_URL')}/users/sign_in",
        email=os.getenv("EMAIL"),
        password=os.getenv("PASSWORD")
    )


# ---------------------------------------------------------------------------
# Browser launch & context configuration (pytest-playwright overrides)
# ---------------------------------------------------------------------------
@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args: dict) -> dict:
    return {
        **browser_type_launch_args,
        "channel": "chrome",
        "headless": False,
        "slow_mo": 0,
        "timeout": 30000,
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
    }


# ---------------------------------------------------------------------------
# Helper: create a context + page from a browser using the standard args
# ---------------------------------------------------------------------------
def _create_context_and_page(browser: Browser, context_args: dict) -> tuple[BrowserContext, Page]:
    """Create a new browser context and page with the configured args."""
    context = browser.new_context(**context_args)
    context.set_default_timeout(30000)
    page = context.new_page()
    return context, page


# ---------------------------------------------------------------------------
# 1. app (function scope) – isolated browser context & page per test
#    This is the DEFAULT fixture. Each test gets a completely fresh state.
# ---------------------------------------------------------------------------
@pytest.fixture(scope="function")
def app(page: Page) -> App:
    """Fresh App instance per test (new context + page via pytest-playwright)."""
    return App(page)


# ---------------------------------------------------------------------------
# 2. shared_app – reuses the SAME page across tests in a module but
#    clears cookies & localStorage after every test for a clean state.
#    Perfect for parametrized tests where browser startup overhead matters.
# ---------------------------------------------------------------------------
@pytest.fixture(scope="module")
def _shared_context(browser: Browser, browser_context_args: dict) -> tuple[BrowserContext, Page]:
    """Module-scoped: creates one context + page, closed at module end."""
    context, page = _create_context_and_page(browser, browser_context_args)
    yield context, page
    context.close()


@pytest.fixture(scope="function")
def shared_app(_shared_context: tuple[BrowserContext, Page]) -> App:
    """Function-scoped wrapper: same page, but cookies & localStorage cleared after each test."""
    context, page = _shared_context
    app = App(page)
    yield app
    # Cleanup: clear cookies and localStorage so the next test starts clean
    context.clear_cookies()
    page.evaluate("window.localStorage.clear()")
    page.evaluate("window.sessionStorage.clear()")


# ---------------------------------------------------------------------------
# 3. logged_in_app (function scope) – fresh context, pre-authenticated
#    Identical to `app` but already logged in before the test body runs.
# ---------------------------------------------------------------------------
@pytest.fixture(scope="function")
def logged_in_app(
    browser: Browser, browser_context_args: dict, configs: Config) -> App:
    """Fresh App instance that is already logged in."""
    context, page = _create_context_and_page(browser, browser_context_args)
    app = App(page)
    app.login_page.open()
    app.login_page.is_loaded()
    app.login_page.login_user(configs.email, configs.password)
    yield app
    context.close()


# ---------------------------------------------------------------------------
# 4. shared_logged_in_app (module scope) – shared context, pre-authenticated
#    Same as shared_app but logged-in once for the entire module.
#    ⚠️  Tests must be aware they share state (session, cookies, etc.)
# ---------------------------------------------------------------------------
@pytest.fixture(scope="module")
def shared_logged_in_app(browser: Browser, browser_context_args: dict, configs: Config) -> App:
    """Shared App instance, logged in once for the entire module."""
    context, page = _create_context_and_page(browser, browser_context_args)
    app = App(page)
    app.login_page.open()
    app.login_page.is_loaded()
    app.login_page.login_user(configs.email, configs.password)
    yield app
    context.close()


# ---------------------------------------------------------------------------
# Legacy: login fixture (function scope) – kept for backward compatibility
# Tests that use `app` + `login` continue to work as before.
# ---------------------------------------------------------------------------
@pytest.fixture(scope="function")
def login(app: App, configs: Config):
    """Log in using the function-scoped app (legacy helper)."""
    app.login_page.open()
    app.login_page.is_loaded()
    app.login_page.login_user(configs.email, configs.password)
