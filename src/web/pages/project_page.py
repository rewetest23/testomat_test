from typing import Self

from playwright.sync_api import Page, expect

from src.web.components import (
    SideBarComponent,
    SuiteDetailModal,
    SuiteEditModal,
    SuiteNewModal,
    TestDetailModal,
    TestEditModal,
    TestNewModal,
)


class ProjectPage:
    def __init__(self, page: Page):
        self.page = page
        self.side_bar = SideBarComponent(page)

        self.suite_new_modal = SuiteNewModal(page)
        self.suite_edit_modal = SuiteEditModal(page)
        self.suite_detail_modal = SuiteDetailModal(page)

        self.test_new_modal = TestNewModal(page)
        self.test_edit_modal = TestEditModal(page)
        self.test_detail_modal = TestDetailModal(page)

        self.suites_container = page.locator(".mainNestedItem")

        self.create_menu_button = page.locator(".md-icon-chevron-down")

    def open_by_id(self, project_id: str) -> Self:
        self.page.goto(f"/projects/{project_id}")
        return self

    def is_loaded(self) -> Self:
        expect(self.page.locator(".sticky-header")).to_be_visible()
        expect(self.page.locator(".mainnav-menu")).to_be_visible()
        expect(self.page.get_by_role("button", name="Suite"))
        return self

    def empty_project_name_is(self, expected_project_name: str) -> Self:
        expect(self.page.locator(".sticky-header h2")).to_have_text(expected_project_name)
        return self

    def close_read_me(self) -> Self:
        self.page.locator(".back .third-btn").click()
        return self

    def create_test_via_popup(self):
        self.page.locator(".sticky-header").get_by_role("button", name="Test  ", exact=True).click()
        return self

    def create_test_via_first_suite_detail_page(self, test_name: str) -> Self:
        self.suites_container.locator("a").first.click()
        self.suite_detail_modal.is_loaded().add_new_test()
        self.test_new_modal.is_loaded().fill_title_and_save(test_name)
        self.test_edit_modal.is_loaded()
        expect(self.suites_container.get_by_text(test_name)).to_be_visible()
        return self

    def create_suite_via_create_menu(self, suite_name: str) -> Self:
        self.create_menu_button.click()
        self.page.get_by_text("Collection of test cases").click()

        self.suite_new_modal.is_loaded().fill_title_and_save(suite_name)
        self.suite_detail_modal.is_loaded().check_have_title(suite_name)
        expect(self.suites_container.get_by_text(suite_name)).to_be_visible()
        return self
