from typing import Self

from playwright.sync_api import Page, expect

from src.web.components import ProjectCardComponent


# AI generated
class ProjectsPage:
    def __init__(self, page: Page):
        self.page = page

        self.page_title = page.get_by_role("heading", name="Projects")
        self.flash_success_message = page.locator(".common-flash-success-right p")
        self.enterprise_plan_label = page.get_by_text("Enterprise plan")
        self.free_plan_label = page.get_by_text("Free plan")
        self.company_dropdown = page.locator("#company_id")
        self.plan_badge = page.locator(".tooltip-project-plan > span")
        self.search_input = page.locator("#search")
        self.create_button = page.get_by_role("link", name="Create")
        self.list_view_type = page.locator(".tab-content")
        self.grid_view_button = page.locator("#grid-view")
        self.table_view_button = page.locator("#table-view")

        self.project_items_locator = page.locator("ul.grid > li")

    def navigate(self) -> Self:
        self.page.goto("/projects")
        return self

    def is_loaded(self) -> Self:
        expect(self.page_title).to_be_visible()
        return self

    def search_for_project(self, project_name: str) -> Self:
        self.search_input.fill(project_name)
        return self

    def select_company(self, value: str) -> Self:
        self.company_dropdown.select_option(value)
        return self

    def click_create_project(self) -> Self:
        self.create_button.click()
        return self

    def check_selected_company(self, expected_value: str) -> Self:
        expect(self.company_dropdown.locator("option[selected]")).to_have_text(expected_value)
        return self

    def get_plan_name(self, expected_value: str) -> Self:
        expect(self.plan_badge).to_have_text(expected_value)
        return self

    def search_project(self, project_name: str) -> Self:
        self.search_input.fill(project_name)
        return self

    def click_create(self) -> Self:
        self.create_button.click()
        return self

    def count_of_projects_visible(self, expected_count: int) -> Self:
        expect(self.project_items_locator.filter(visible=True)).to_have_count(expected_count)
        return self

    def get_all_projects(self) -> list[ProjectCardComponent]:
        visible_projects = self.project_items_locator.filter(visible=True)
        count = visible_projects.count()

        return [ProjectCardComponent(visible_projects.nth(i)) for i in range(count)]

    def get_project_by_title(self, title: str) -> ProjectCardComponent | None:
        expect(self.page.locator("h3", has_text=title).first).to_be_visible()
        for project in self.get_all_projects():
            project_title = project.get_title()
            if project_title and title in project_title:
                return project
        return None

    def change_list_view_type_to_grid(self) -> Self:
        if self.list_view_type.get_attribute("id") == "table":
            self.grid_view_button.click()

        expect(self.list_view_type).to_have_attribute("id", "grid")
        return self

    def change_list_view_type_to_table(self) -> Self:
        if self.list_view_type.get_attribute("id") == "grid":
            self.table_view_button.click()

        expect(self.list_view_type).to_have_attribute("id", "table")
        return self

    def open_first_project_with_single_member(self) -> bool:
        rows = self.page.locator("tbody tr")

        try:
            rows.first.wait_for(state="visible", timeout=3000)
        except TimeoutError:
            return False

        for i in range(rows.count()):
            row = rows.nth(i)
            member_images = row.locator("td div img")

            if member_images.count() == 1:
                row.locator("a").first.click()
                return True

        return False
