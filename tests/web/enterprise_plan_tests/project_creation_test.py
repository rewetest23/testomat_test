import pytest

from src.api.client import ApiClient
from src.web.app import App


@pytest.mark.smoke
@pytest.mark.web
def test_new_projects_creation(logged_in_app: App, faker):
    app = logged_in_app
    target_project_name = faker.company()

    (app.new_projects_page
     .open()
     .is_loaded()
     .fill_project_title(target_project_name)
     .click_create())

    (app.project_page
     .is_loaded()
     .close_read_me()
     .empty_project_name_is(target_project_name))

    (app.project_page.side_bar
     .expand()
     .is_loaded()
     .tab_is_active("Tests"))


@pytest.mark.smoke
@pytest.mark.web
def test_open_project_and_create_test_from_suite_modal(api_client: ApiClient, logged_in_app: App, faker):
    projects_with_suites = api_client.get_projects_with_suites()
    target_project_id = projects_with_suites[0].id

    logged_in_app.project_page.open_by_id(target_project_id).is_loaded()
    logged_in_app.project_page.create_test_via_first_suite_detail_page(test_name=faker.sentence())


@pytest.mark.smoke
@pytest.mark.web
def test_open_project_and_create_suite_from_create_menu(api_client: ApiClient, logged_in_app: App, faker):
    projects_with_suites = api_client.get_projects_with_suites()
    target_project_id = projects_with_suites[0].id

    logged_in_app.project_page.open_by_id(target_project_id).is_loaded()
    logged_in_app.project_page.create_suite_via_create_menu(suite_name=faker.sentence())
