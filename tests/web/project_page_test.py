from playwright.sync_api import Page

from src.web.components.ProjectCardComponent import Badges
from src.web.pages.ProjectsPage import ProjectsPage


def test_projects_page_header(page: Page, login):
    projects_page = ProjectsPage(page)
    projects_page.navigate()

    projects_page.is_loaded()

    projects_page.check_selected_company("QA Club Lviv")
    projects_page.get_plan_name("Enterprise plan")

    target_project_name = "TestCafe Demo Project"
    projects_page.search_project(target_project_name)
    projects_page.count_of_projects_visible(1)
    target_project = projects_page.get_project_by_title(target_project_name)
    target_project.badges_has(Badges.DEMO)
