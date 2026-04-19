import os
from dataclasses import dataclass
import pytest

@dataclass(frozen=True)
class Config:
    base_url: str
    base_app_url: str
    sign_in_url: str
    email: str
    password: str
    general_api_token: str

@pytest.fixture(scope="session")
def configs():
    return Config(
        base_url=os.getenv("BASE_URL"),
        base_app_url=os.getenv("BASE_APP_URL"),
        sign_in_url=os.getenv('SIGN_IN_URL'),
        email=os.getenv("EMAIL"),
        password=os.getenv("PASSWORD"),
        general_api_token=os.getenv("GENERAL_API_TOKEN")
    )
