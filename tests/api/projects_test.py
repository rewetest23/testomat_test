import pytest

from src.api.client import ApiClient
from src.api.models import ProjectsResponse

def test_get_projects(api_client: ApiClient):
    """
    Test that the get_projects endpoint returns a successful response
    and contains a list of projects.
    """
    response = api_client.get_projects()

    # Assert that the response is of type ProjectsResponse
    assert isinstance(response, ProjectsResponse)

    # Assert that data is a list
    assert isinstance(response.data, list)

    # Print the number of projects found for debugging purposes
    print(f"Found {len(response.data)} projects.")

