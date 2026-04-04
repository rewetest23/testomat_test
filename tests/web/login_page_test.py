from faker import Faker

from conftest import Config
from src.web.App import App


def test_login_invalid(app: App, configs: Config):
    app.home_page.open()
    app.home_page.is_loaded()
    app.home_page.click_login()

    app.login_page.is_loaded()
    app.login_page.login(configs.email, Faker().password(length=12))
    app.login_page.invalid_login_message_visible()


def test_login_valid_password(app: App, configs: Config):
    app.home_page.open()
    app.home_page.is_loaded()
    app.home_page.click_login()

    app.login_page.is_loaded()
    app.login_page.login(configs.email, configs.password)

    app.projects_page.is_loaded()