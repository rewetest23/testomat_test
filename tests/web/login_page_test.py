import pytest
from faker import Faker

from conftest import Config
from src.web.app import App

fake = Faker()

invalid_login_data = [
    pytest.param("", "", id="empty_email-empty_password"),
    pytest.param("", fake.pystr(min_chars=1, max_chars=1), id="empty_email-single_char_password"),
    pytest.param(fake.user_name(), fake.password(length=10), id="no_at_sign_email-wrong_password"),
    pytest.param(f"@{fake.domain_name()}", fake.password(length=10), id="missing_local_part-wrong_password"),
    pytest.param(fake.email(), fake.password(length=12), id="valid_format_email-wrong_password"),
    pytest.param(fake.email(), fake.pystr(min_chars=256, max_chars=256), id="valid_format_email-256_char_password"),
    pytest.param("   ", "   ", id="whitespace_email-whitespace_password"),
    pytest.param("' OR 1=1 --", fake.password(length=10), id="sql_injection_email-wrong_password"),
    pytest.param("<script>alert(1)</script>", fake.password(length=10), id="xss_email-wrong_password"),
    pytest.param(fake.email(), "🔑🔒💀", id="valid_format_email-emoji_password"),
    pytest.param(f"{fake.user_name()}@@{fake.domain_name()}", fake.password(length=10), id="double_at_email-wrong_password"),
    pytest.param(fake.email(), f"  {fake.password(length=8)}  ", id="valid_format_email-password_with_spaces"),
]

@pytest.mark.regression
@pytest.mark.parametrize("email, password", invalid_login_data)
def test_login_invalid(shared_app: App, email: str, password: str):
    shared_app.login_page.wait_if_rate_limit(5000)
    shared_app.login_page.open()
    shared_app.login_page.is_loaded()
    shared_app.login_page.login_user(email, password)
    shared_app.login_page.invalid_login_message_visible()



@pytest.mark.regression
def test_login_valid_password(app: App, configs: Config):
    (app.home_page
     .open()
     .is_loaded()
     .click_login())

    (app.login_page
     .is_loaded()
     .login_user(configs.email, configs.password))

    app.projects_page.is_loaded()