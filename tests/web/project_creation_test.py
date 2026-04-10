from faker.proxy import Faker

from src.web.App import App


def test_new_projects_creation(shared_logged_in_app: App):
    app = shared_logged_in_app
    target_project_name = Faker().company()

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
