import pytest
from playwright.sync_api import Page, Browser, BrowserContext
from src.web.app import App
from fixtures.config import Config
from fixtures.playwright_fixtures import create_context_and_page

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
def logged_in_app(browser: Browser, browser_context_args: dict, configs: Config) -> App:
    """Fresh App instance that is already logged in."""
    context, page = create_context_and_page(browser, browser_context_args)
    app = App(page)
    app.login_page.open()
    app.login_page.is_loaded()
    app.login_page.login_user(configs.email, configs.password)
    yield app
    context.close()

@pytest.fixture(scope="module")
def shared_logged_in_app(browser: Browser, browser_context_args: dict, configs: Config) -> App:
    """Shared App instance, logged in once for the entire module."""
    context, page = create_context_and_page(browser, browser_context_args)
    app = App(page)
    app.login_page.open()
    app.login_page.is_loaded()
    app.login_page.login_user(configs.email, configs.password)
    yield app
    context.close()

@pytest.fixture(scope="function")
def login(app: App, configs: Config):
    """Log in using the function-scoped app (legacy helper)."""
    app.login_page.open()
    app.login_page.is_loaded()
    app.login_page.login_user(configs.email, configs.password)
