import pytest
from playwright.sync_api import Page

from conftest import Config
from src.web.components.ProjectCardComponent import Badges
from src.web.pages.LoginPage import LoginPage
from src.web.pages.ProjectsPage import ProjectsPage


@pytest.fixture(scope="function")
def login(page: Page, configs: Config):
    login_page = LoginPage(page)
    login_page.open()
    login_page.is_loaded()
    login_page.login(configs.email, configs.password)


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
