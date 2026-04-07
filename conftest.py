import os
from dataclasses import dataclass

import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page

from src.web.App import App

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


@pytest.fixture(scope="session")
def browser_type_launch_arg(browser_type_launch_arg: dict) -> dict:
    return {
        **browser_type_launch_arg,
        "channel": "chrome",
        "headless": False,
        "slow_mo": 0,
        "timeout": 30000,
    }


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: dict) -> dict:
    return {
        **browser_context_args,
        "base_url": "https://app.testomat.io",
        "viewport": {"width": 1920, "height": 1080},
        "locale": "uk_UA",
        "timezone": "Europe/Kyiv",
        "record_video_dir": "/videos",
        "permissions": ["geolocation"],
    }


@pytest.fixture(scope="function")
def app(page: Page) -> App:
    return App(page)


@pytest.fixture(scope="function")
def login(app: App, configs: Config):
    app.login_page.open()
    app.login_page.is_loaded()
    app.login_page.login(configs.email, configs.password)
