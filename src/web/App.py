from playwright.sync_api import Page
from src.web.pages.HomePage import HomePage
from src.web.pages.LoginPage import LoginPage
from src.web.pages.NewProjectsPage import NewProjectsPage
from src.web.pages.ProjectPage import ProjectPage
from src.web.pages.ProjectsPage import ProjectsPage
from src.web.pages.RequirementsPage import RequirementsPage


class App:
    def __init__(self, page: Page):
        self.page = page
        self.home_page = HomePage(self.page)
        self.login_page = LoginPage(self.page)
        self.new_projects_page = NewProjectsPage(self.page)
        self.project_page = ProjectPage(self.page)
        self.projects_page = ProjectsPage(self.page)
        self.requirements_page = RequirementsPage(self.page)
