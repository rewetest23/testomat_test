import pytest

from src.web.app import App


@pytest.mark.skip("in app_fixtures.py as last run")
def test_delete_all_projects_with_one_user_in_team(shared_logged_in_app: App):
    app = shared_logged_in_app

    (app.projects_page
     .navigate()
     .is_loaded()
     .change_list_view_type_to_table())

    while app.projects_page.open_first_project_with_single_member():
        app.project_page.is_loaded()
        app.project_page.side_bar.click_settings()

        (app.project_settings_page
         .is_loaded()
         .delete_project())

        (app.project_settings_page.side_bar
         .expand()
         .click_projects())

        app.projects_page.is_loaded()
