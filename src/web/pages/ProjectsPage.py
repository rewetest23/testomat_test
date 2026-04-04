from playwright.sync_api import Page, expect

from src.web.components import ProjectCardComponent


# AI generated
class ProjectsPage:
    def __init__(self, page: Page):
        self.page = page

        self.page_title = page.get_by_role("heading", name="Projects")
        self.flash_success_message = page.locator(".common-flash-success-right p")
        self.company_dropdown = page.locator("#company_id")
        self.plan_badge = page.locator(".tooltip-project-plan > span")
        self.search_input = page.get_by_placeholder("Search Project")
        self.create_button = page.get_by_role("link", name="Create")
        self.grid_view_button = page.locator("#grid-view")
        self.table_view_button = page.locator("#table-view")

        self._project_items_locator = page.locator("ul.grid > li")

    def navigate(self):
        self.page.goto("/projects")

    def is_loaded(self):
        expect(self.page_title).to_be_visible()

    def search_for_project(self, project_name: str):
        self.search_input.fill(project_name)

    def select_company(self, value: str):
        self.company_dropdown.select_option(value)

    def click_create_project(self):
        self.create_button.click()

    def check_selected_company(self, expected_value: str):
        expect(self.company_dropdown.locator("option[selected]")).to_have_text(expected_value)

    def get_plan_name(self, expected_value: str):
        expect(self.plan_badge).to_have_text(expected_value)

    def search_project(self, project_name: str):
        self.search_input.fill(project_name)

    def click_create(self):
        self.create_button.click()

    def count_of_projects_visible(self, expected_count: int):
        expect(self._project_items_locator.filter(visible=True)).to_have_count(expected_count)

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
