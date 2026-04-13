import pytest

from src.api.client import ApiClient


@pytest.mark.api
def test_get_projects(api_client: ApiClient):
    """
    Test that the get_projects endpoint returns a successful response
    and contains a list of projects.
    """
    response = api_client.get_projects()

    # Assert that the response is a dictionary
    assert isinstance(response, dict)

    # JSON:API responses usually have a 'data' array
    assert "data" in response
    assert isinstance(response["data"], list)

    # Print the number of projects found for debugging purposes
    print(f"Found {len(response['data'])} projects.")
