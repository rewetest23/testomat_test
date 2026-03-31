from faker import Faker
from playwright.sync_api import Page

from conftest import Config
from src.web.pages.HomePage import HomePage
from src.web.pages.LoginPage import LoginPage
from src.web.pages.ProjectsPage import ProjectsPage


def test_login_invalid(page: Page, configs: Config):
    home_page = HomePage(page)
    home_page.open()
    home_page.is_loaded()
    home_page.click_login()

    login_page = LoginPage(page)
    login_page.is_loaded()
    login_page.login(configs.email, Faker().password(length=12))
    login_page.invalid_login_message_visible()


def test_login_valid_password(page: Page, configs: Config):
    home_page = HomePage(page)
    home_page.open()
    home_page.is_loaded()
    home_page.click_login()

    login_page = LoginPage(page)
    login_page.is_loaded()
    login_page.login(configs.email, configs.password)

    ProjectsPage(page).is_loaded()