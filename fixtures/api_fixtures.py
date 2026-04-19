import pytest

from fixtures.config import Config
from src.api.client import ApiClient


@pytest.fixture(scope="session")
def api_client(configs: Config) -> ApiClient:
    """Provides an authenticated API client using the GENERAL_API_TOKEN."""
    if not configs.general_api_token:
        pytest.skip("GENERAL_API_TOKEN is not set in the environment.")

    client = ApiClient(base_app_url=configs.base_app_url)
    client.login_with_api_token(configs.general_api_token)
    return client


@pytest.fixture(scope="session")  # autouse=True
def api_cleanup_projects(api_client: ApiClient):
    """Automatically cleans up all single-member projects at the end of the test session via API."""
    yield
    try:
        projects = api_client.get_projects()

        for project in projects:
            project_id = project.id
            if not project_id:
                continue

            try:
                # Fetch users for this specific project
                users = api_client.get_project_users(project_id)

                # Single-member projects (creator only) have exactly 1 user
                if len(users) == 1:
                    api_client.delete_project(project_id)
                    print(f"Cleaned up project via API: {project_id}")
            except Exception as e:
                print(f"Failed to process/delete {project_id}: {e}")
    except Exception as e:
        print(f"API Cleanup failed: {e}")
