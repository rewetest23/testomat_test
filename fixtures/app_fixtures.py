import json
import re
from pathlib import Path

import pytest
from playwright.sync_api import Page, Browser, BrowserContext

from fixtures.config import Config
from fixtures.cookie_helper import CookieHelper
from fixtures.playwright_fixtures import create_context_and_page
from src.web.app import App

STORAGE_STATE_DIR = Path("test-result/.auth")
TRACES_DIR = Path("test-result/traces")
STORAGE_STATE_PATH = STORAGE_STATE_DIR / "storage_state.json"
FREE_PROJECT_STORAGE_PATH = STORAGE_STATE_DIR / "free_project_state.json"


def _perform_login_and_save_both_states(
    browser: Browser, browser_context_args: dict, configs: Config
) -> None:
    """Perform login once via API and save both storage states (app + free_project)."""
    STORAGE_STATE_DIR.mkdir(parents=True, exist_ok=True)

    # Create an isolated context for login
    context = browser.new_context(**browser_context_args)

    # Get CSRF token via API request
    response = context.request.get(configs.sign_in_url)
    text = response.text()

    match = re.search(r'name="authenticity_token" value="(.*?)"', text)
    if not match:
        raise RuntimeError("Could not find authenticity token on login page")
    csrf_token = match.group(1)

    # Login via POST request instead of UI
    login_response = context.request.post(
        configs.sign_in_url,
        form={
            "authenticity_token": csrf_token,
            "user[email]": configs.email,
            "user[password]": configs.password,
            "user[remember_me]": "1",
        },
    )

    if login_response.status not in (200, 302, 303):
        raise RuntimeError(f"API Login failed with status: {login_response.status}")

    # Save the main (enterprise/company) storage state
    context.storage_state(path=str(STORAGE_STATE_PATH))

    # Derive free project state: copy state with empty company_id
    state = json.loads(STORAGE_STATE_PATH.read_text())
    for cookie in state.get("cookies", []):
        if cookie.get("name") == "company_id":
            cookie["value"] = ""
            break
    FREE_PROJECT_STORAGE_PATH.write_text(json.dumps(state, indent=2))

    context.close()


def _start_tracing(context: BrowserContext) -> None:
    """Start Playwright tracing with screenshots, snapshots and sources."""
    context.tracing.start(screenshots=True, snapshots=True, sources=True)


def _stop_tracing(context: BrowserContext, request: pytest.FixtureRequest) -> None:
    """Stop tracing and save the trace ZIP only if the test failed."""
    failed = hasattr(request.node, "rep_call") and request.node.rep_call.failed
    if failed:
        trace_path = TRACES_DIR / f"{request.node.name}.zip"
        trace_path.parent.mkdir(parents=True, exist_ok=True)
        context.tracing.stop(path=str(trace_path))
    else:
        context.tracing.stop()


def _ensure_storage_states(
    browser: Browser, browser_context_args: dict, configs: Config
) -> None:
    """Ensure both storage state files exist; perform login if either is missing."""
    if not STORAGE_STATE_PATH.exists() or not FREE_PROJECT_STORAGE_PATH.exists():
        _perform_login_and_save_both_states(browser, browser_context_args, configs)


# ---------------------------------------------------------------------------
# App fixtures (enterprise / with company)
# ---------------------------------------------------------------------------

@pytest.fixture(scope="function")
def app(
    browser: Browser, browser_context_args: dict, configs: Config,
    request: pytest.FixtureRequest,
) -> App:
    """Logged-in App with company context (enterprise). Reuses cached storage state."""
    _ensure_storage_states(browser, browser_context_args, configs)

    context_args = {**browser_context_args, "storage_state": str(STORAGE_STATE_PATH)}
    context, page = create_context_and_page(browser, context_args)
    _start_tracing(context)
    app = App(page)
    yield app
    _stop_tracing(context, request)
    context.close()


@pytest.fixture(scope="function")
def unauthenticated_app(
    browser: Browser, browser_context_args: dict,
    request: pytest.FixtureRequest,
) -> App:
    """Fresh App instance without any auth state (for login-flow tests)."""
    context, page = create_context_and_page(browser, browser_context_args)
    _start_tracing(context)
    app = App(page)
    yield app
    _stop_tracing(context, request)
    context.close()


# ---------------------------------------------------------------------------
# Free-project App fixtures (no company)
# ---------------------------------------------------------------------------

@pytest.fixture(scope="function")
def free_project_app(
    browser: Browser, browser_context_args: dict, configs: Config,
    request: pytest.FixtureRequest,
) -> App:
    """Logged-in App without company context (free project). Reuses cached storage state."""
    _ensure_storage_states(browser, browser_context_args, configs)

    context_args = {**browser_context_args, "storage_state": str(FREE_PROJECT_STORAGE_PATH)}
    context, page = create_context_and_page(browser, context_args)
    _start_tracing(context)
    app = App(page)
    yield app
    _stop_tracing(context, request)
    context.close()


# ---------------------------------------------------------------------------
# Shared (module-scoped) variants
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def _shared_context(browser: Browser, browser_context_args: dict, configs: Config) -> tuple[BrowserContext, Page]:
    """Module-scoped: creates one logged-in context + page, closed at module end."""
    _ensure_storage_states(browser, browser_context_args, configs)

    context_args = {**browser_context_args, "storage_state": str(STORAGE_STATE_PATH)}
    context, page = create_context_and_page(browser, context_args)
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


@pytest.fixture(scope="module")
def shared_logged_in_app(browser: Browser, browser_context_args: dict, configs: Config) -> App:
    """Shared App instance, logged in once for the entire module via storage state."""
    _ensure_storage_states(browser, browser_context_args, configs)

    context_args = {**browser_context_args, "storage_state": str(STORAGE_STATE_PATH)}
    context, page = create_context_and_page(browser, context_args)
    app = App(page)
    yield app
    context.close()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

@pytest.fixture(scope="function")
def cookies(app: App) -> CookieHelper:
    """Provides cookie manipulation helper for the logged-in context."""
    return CookieHelper(app.page.context)

