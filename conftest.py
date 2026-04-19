import json
import os
from pathlib import Path

import pytest
from dotenv import load_dotenv

# Load .env file: ENV=dev11 -> .env.dev11, default -> .env
_env_name = os.getenv("ENV", "")
_env_file = Path(f"env/.env.{_env_name}") if _env_name else Path("env/.env")
load_dotenv(_env_file)

pytest_plugins = [
    "fixtures.config",
    "fixtures.faker_fixtures",
    "fixtures.playwright_fixtures",
    "fixtures.app_fixtures",
    "fixtures.api_fixtures",
]


# this is config from pytest, not from config fixture
def pytest_configure(config):
    """Inject browser list from .env into pytest-playwright.

    .env example: BROWSERS=["chromium","firefox"]
    Default: ["chromium"]
    CLI --browser flags take priority over .env.
    """
    cli_browsers = config.getoption("--browser", default=None)
    if not cli_browsers:
        raw = os.getenv("BROWSERS", "")
        try:
            browsers = json.loads(raw) if raw else ["chromium"]
        except json.JSONDecodeError:
            browsers = ["chromium"]
        config.option.browser = browsers


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Store test outcome on the item node so fixtures can detect failures.

    After this hook, fixtures can check:
        failed = hasattr(request.node, "rep_call") and request.node.rep_call.failed
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
