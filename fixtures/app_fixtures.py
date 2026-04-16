import os

import pytest
from playwright.sync_api import Page, Browser, BrowserContext

from fixtures.config import Config
from fixtures.cookie_helper import CookieHelper
from fixtures.playwright_fixtures import create_context_and_page
from src.web.app import App


import re

@pytest.fixture(scope="session")
def session_storage_state(browser: Browser, browser_context_args: dict, configs: Config) -> str:
    """Perform login once per session via API request and save the storage state."""
    auth_dir = "test-result/.auth"
    auth_path = os.path.join(auth_dir, "storage_state.json")

    # Ensure directory exists
    os.makedirs(auth_dir, exist_ok=True)

    # Create an isolated context for login (no base storage_state here)
    context = browser.new_context(**browser_context_args)

    # Get CSRF token via API request
    response = context.request.get(configs.sign_in_url)
    text = response.text()
    
    match = re.search(r'name="authenticity_token" value="(.*?)"', text)
    if not match:
        raise RuntimeError("Could not find authenticity token on login page")
    csrf_token = match.group(1)

    # Login via Post request instead of UI
    login_response = context.request.post(
        configs.sign_in_url,
        form={
            "authenticity_token": csrf_token,
            "user[email]": configs.email,
            "user[password]": configs.password,
            "user[remember_me]": "1"
        }
    )
    
    if login_response.status not in (200, 302, 303):
        raise RuntimeError(f"API Login failed with status: {login_response.status}")

    # Save session state
    context.storage_state(path=auth_path)
    context.close()
    return auth_path


@pytest.fixture(scope="function")
def app(page: Page) -> App:
    """Fresh App instance per test (new context + page via pytest-playwright)."""
    return App(page)


@pytest.fixture(scope="module")
def _shared_context(browser: Browser, browser_context_args: dict) -> tuple[BrowserContext, Page]:
    """Module-scoped: creates one context + page, closed at module end."""
    context, page = create_context_and_page(browser, browser_context_args)
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


@pytest.fixture(scope="function")
def logged_in_app(browser: Browser, browser_context_args: dict, session_storage_state: str) -> App:
    """Fresh App instance that is already logged in using storage state."""
    # Use the pre-saved storage state
    context_args = {**browser_context_args, "storage_state": session_storage_state}
    context, page = create_context_and_page(browser, context_args)
    app = App(page)
    yield app
    context.close()


@pytest.fixture(scope="module")
def shared_logged_in_app(browser: Browser, browser_context_args: dict, session_storage_state: str) -> App:
    """Shared App instance, logged in once for the entire module via storage state."""
    # Use the pre-saved storage state
    context_args = {**browser_context_args, "storage_state": session_storage_state}
    context, page = create_context_and_page(browser, context_args)
    app = App(page)
    yield app
    context.close()


@pytest.fixture(scope="function")
def cookies(logged_in_app: App) -> CookieHelper:
    """Provides cookie manipulation helper for the logged-in context."""
    return CookieHelper(logged_in_app.page.context)


@pytest.fixture(scope="function")
def login(app: App, configs: Config):
    """Log in using the function-scoped app (legacy helper)."""
    app.login_page.open()
    app.login_page.is_loaded()
    app.login_page.login_user(configs.email, configs.password)
