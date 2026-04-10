import re
from typing import Self

from playwright.sync_api import Page, expect


class SideBarComponent:

    def __init__(self, page: Page):
        self.page = page
        self._root = page.locator(".mainnav-menu")

        self._open_button = self._root.locator("button.btn-open")
        self._tests_link = self._root.locator("a").filter(has_text="Tests")
        self._requirements_link = self._root.locator("a").filter(has_text="Requirements")
        self._runs_link = self._root.locator("a").filter(has_text="Runs")
        self._plans_link = self._root.locator("a").filter(has_text="Plans")
        self._steps_link = self._root.locator("a").filter(has_text="Steps")
        self._pulse_link = self._root.locator("a").filter(has_text="Pulse")
        self._imports_link = self._root.locator("a").filter(has_text="Imports")
        self._analytics_link = self._root.locator("a").filter(has_text="Analytics")
        self._branches_link = self._root.locator("a").filter(has_text="Branches")
        self._settings_link = self._root.locator("a").filter(has_text="Settings")

        self._help_link = self._root.locator("a").filter(has_text="Help")
        self._projects_link = self._root.locator("a").filter(has_text="Projects")
        self._user_profile_link = self._root.locator(".mainnav-menu-footer a").last

        self._close_button = self._root.get_by_role("button")

    def is_loaded(self) -> Self:
        expect(self._root).to_be_visible()
        expect(self._tests_link).to_be_visible()
        expect(self._runs_link).to_be_visible()
        expect(self._projects_link).to_be_visible()
        expect(self._user_profile_link).to_be_visible()
        return self

    def expand(self) -> Self:
        menu_class = self._root.get_attribute("class") or ""
        if "mainnav-menu-not-expanded" in menu_class:
            self._open_button.click()
            expect(self._root).not_to_have_class("mainnav-menu-not-expanded")
        return self

    def tab_is_active(self, tab_name: str) -> Self:
        link = self._root.locator("a").filter(has_text=f"{tab_name}")
        expect(link).to_have_class(re.compile(r"\bactive\b"))
        return self

    def click_tests(self) -> Self:
        self._tests_link.click()
        return self

    def click_requirements(self) -> Self:
        self._requirements_link.click()
        return self

    def click_runs(self) -> Self:
        self._runs_link.click()
        return self

    def click_plans(self) -> Self:
        self._plans_link.click()
        return self

    def click_steps(self) -> Self:
        self._steps_link.click()
        return self

    def click_pulse(self) -> Self:
        self._pulse_link.click()
        return self

    def click_imports(self) -> Self:
        self._imports_link.click()
        return self

    def click_analytics(self) -> Self:
        self._analytics_link.click()
        return self

    def click_branches(self) -> Self:
        self._branches_link.click()
        return self

    def click_settings(self) -> Self:
        self._settings_link.click()
        return self

    def click_help(self) -> Self:
        self._help_link.click()
        return self

    def click_projects(self) -> Self:
        self._projects_link.click()
        return self

    def toggle_sidebar(self) -> Self:
        self._close_button.click()
        return self
