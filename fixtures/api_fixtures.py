import pytest
from fixtures.config import Config
from src.api.client import ApiClient

@pytest.fixture(scope="session")
def api_client(configs: Config) -> ApiClient:
    """Provides an authenticated API client using the GENERAL_API_TOKEN."""
    if not configs.general_api_token:
        pytest.skip("GENERAL_API_TOKEN is not set in the environment.")
        
    client = ApiClient(base_url=configs.base_app_url)
    client.login_with_api_token(configs.general_api_token)
    return client
