from playwright.sync_api import Page

from src.web.pages import (
    HomePage,
    LoginPage,
    NewProjectsPage,
    ProjectPage,
    ProjectSettingsPage,
    ProjectsPage,
    RequirementsPage,
)


class App:
    def __init__(self, page: Page):
        self.page = page
        self.home_page = HomePage(self.page)
        self.login_page = LoginPage(self.page)
        self.new_projects_page = NewProjectsPage(self.page)
        self.projects_page = ProjectsPage(self.page)
        self.project_page = ProjectPage(self.page)
        self.project_settings_page = ProjectSettingsPage(self.page)
        self.requirements_page = RequirementsPage(self.page)
