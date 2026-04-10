from src.web.app import App
from src.web.components.project_card_component import Badges


def test_projects_page_header(shared_logged_in_app: App):
    app = shared_logged_in_app
    app.projects_page.navigate()

    app.projects_page.is_loaded()

    app.projects_page.check_selected_company("QA Club Lviv")
    app.projects_page.get_plan_name("Enterprise plan")

    target_project_name = "TestCafe Demo Project"
    app.projects_page.search_project(target_project_name)
    app.projects_page.count_of_projects_visible(1)
    target_project = app.projects_page.get_project_by_title(target_project_name)
    target_project.badges_has(Badges.DEMO)
    print(target_project.get_test_count_text())
