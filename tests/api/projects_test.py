import pytest

from src.api.client import ApiClient

def test_get_projects(api_client: ApiClient):
    """
    Test that the get_projects endpoint returns a successful response
    and contains a list of projects.
    """
    projects = api_client.get_projects()

    # Assert that the response is a list
    assert isinstance(projects, list)

    # Print the number of projects found for debugging purposes
    print(f"Found {len(projects)} projects.")

