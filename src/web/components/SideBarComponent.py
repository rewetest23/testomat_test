import re
from typing import Self

from playwright.sync_api import Page, expect


class SideBarComponent:

    def __init__(self, page: Page):
        self.page = page
        self.__root = page.locator(".mainnav-menu")

        self.__open_button = self.__root.locator("button.btn-open")
        self.__tests_link = self.__root.locator("a").filter(has_text="Tests")
        self.__requirements_link = self.__root.locator("a").filter(has_text="Requirements")
        self.__runs_link = self.__root.locator("a").filter(has_text="Runs")
        self.__plans_link = self.__root.locator("a").filter(has_text="Plans")
        self.__steps_link = self.__root.locator("a").filter(has_text="Steps")
        self.__pulse_link = self.__root.locator("a").filter(has_text="Pulse")
        self.__imports_link = self.__root.locator("a").filter(has_text="Imports")
        self.__analytics_link = self.__root.locator("a").filter(has_text="Analytics")
        self.__branches_link = self.__root.locator("a").filter(has_text="Branches")
        self.__settings_link = self.__root.locator("a").filter(has_text="Settings")

        self.__help_link = self.__root.locator("a").filter(has_text="Help")
        self.__projects_link = self.__root.locator("a").filter(has_text="Projects")
        self.__user_profile_link = self.__root.locator(".mainnav-menu-footer a").last

        self.__close_button = self.__root.get_by_role("button")

    def is_loaded(self) -> Self:
        expect(self.__root).to_be_visible()
        expect(self.__tests_link).to_be_visible()
        expect(self.__runs_link).to_be_visible()
        expect(self.__projects_link).to_be_visible()
        expect(self.__user_profile_link).to_be_visible()
        return self

    def expand(self) -> Self:
        menu_class = self.__root.get_attribute("class") or ""
        if "mainnav-menu-not-expanded" in menu_class:
            self.__open_button.click()
            expect(self.__root).not_to_have_class("mainnav-menu-not-expanded")
        return self

    def tab_is_active(self, tab_name: str) -> Self:
        link = self.__root.locator("a").filter(has_text=f"{tab_name}")
        expect(link).to_have_class(re.compile(r"\bactive\b"))
        return self

    def click_tests(self) -> Self:
        self.__tests_link.click()
        return self

    def click_requirements(self) -> Self:
        self.__requirements_link.click()
        return self

    def click_runs(self) -> Self:
        self.__runs_link.click()
        return self

    def click_plans(self) -> Self:
        self.__plans_link.click()
        return self

    def click_steps(self) -> Self:
        self.__steps_link.click()
        return self

    def click_pulse(self) -> Self:
        self.__pulse_link.click()
        return self

    def click_imports(self) -> Self:
        self.__imports_link.click()
        return self

    def click_analytics(self) -> Self:
        self.__analytics_link.click()
        return self

    def click_branches(self) -> Self:
        self.__branches_link.click()
        return self

    def click_settings(self) -> Self:
        self.__settings_link.click()
        return self

    def click_help(self) -> Self:
        self.__help_link.click()
        return self

    def click_projects(self) -> Self:
        self.__projects_link.click()
        return self

    def toggle_sidebar(self) -> Self:
        self.__close_button.click()
        return self
