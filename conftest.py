import pytest

pytest_plugins = [
    "fixtures.config",
    "fixtures.faker_fixtures",
    "fixtures.playwright_fixtures",
    "fixtures.app_fixtures",
    "fixtures.api_fixtures",
]


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Store test outcome on the item node so fixtures can detect failures.

    After this hook, fixtures can check:
        failed = hasattr(request.node, "rep_call") and request.node.rep_call.failed
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
