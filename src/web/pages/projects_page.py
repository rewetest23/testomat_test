from typing import Self
from playwright.sync_api import Page, expect

from src.web.components import ProjectCardComponent


# AI generated
class ProjectsPage:
    def __init__(self, page: Page):
        self.page = page

        self._page_title = page.get_by_role("heading", name="Projects")
        self._flash_success_message = page.locator(".common-flash-success-right p")
        self._company_dropdown = page.locator("#company_id")
        self._plan_badge = page.locator(".tooltip-project-plan > span")
        self._search_input = page.get_by_placeholder("Search Project")
        self._create_button = page.get_by_role("link", name="Create")
        self._grid_view_button = page.locator("#grid-view")
        self._table_view_button = page.locator("#table-view")

        self._project_items_locator = page.locator("ul.grid > li")

    def navigate(self) -> Self:
        self.page.goto("/projects")
        return self

    def is_loaded(self) -> Self:
        expect(self._page_title).to_be_visible()
        return self

    def search_for_project(self, project_name: str) -> Self:
        self._search_input.fill(project_name)
        return self

    def select_company(self, value: str) -> Self:
        self._company_dropdown.select_option(value)
        return self

    def click_create_project(self) -> Self:
        self._create_button.click()
        return self

    def check_selected_company(self, expected_value: str) -> Self:
        expect(self._company_dropdown.locator("option[selected]")).to_have_text(expected_value)
        return self

    def get_plan_name(self, expected_value: str) -> Self:
        expect(self._plan_badge).to_have_text(expected_value)
        return self

    def search_project(self, project_name: str) -> Self:
        self._search_input.fill(project_name)
        return self

    def click_create(self) -> Self:
        self._create_button.click()
        return self

    def count_of_projects_visible(self, expected_count: int) -> Self:
        expect(self._project_items_locator.filter(visible=True)).to_have_count(expected_count)
        return self

    def get_all_projects(self) -> list[ProjectCardComponent]:
        visible_projects = self._project_items_locator.filter(visible=True)
        count = visible_projects.count()

        return [ProjectCardComponent(visible_projects.nth(i)) for i in range(count)]

    def get_project_by_title(self, title: str) -> ProjectCardComponent | None:
        expect(self.page.locator("h3", has_text=title).first).to_be_visible()
        for project in self.get_all_projects():
            project_title = project.get_title()
            if project_title and title in project_title:
                return project
        return None
