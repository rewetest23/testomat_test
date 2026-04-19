import re
from typing import Self

from playwright.sync_api import Page, expect


class SideBarComponent:

    def __init__(self, page: Page):
        self.page = page
        self.root = page.locator(".mainnav-menu")

        self.open_button = self.root.locator("button.btn-open")
        self.tests_link = self.root.locator("a").filter(has_text="Tests")
        self.requirements_link = self.root.locator("a").filter(has_text="Requirements")
        self.runs_link = self.root.locator("a").filter(has_text="Runs")
        self.plans_link = self.root.locator("a").filter(has_text="Plans")
        self.steps_link = self.root.locator("a").filter(has_text="Steps")
        self.pulse_link = self.root.locator("a").filter(has_text="Pulse")
        self.imports_link = self.root.locator("a").filter(has_text="Imports")
        self.analytics_link = self.root.locator("a").filter(has_text="Analytics")
        self.branches_link = self.root.locator("a").filter(has_text="Branches")
        self.settings_link = self.root.locator("a").filter(has_text="Settings")

        self.help_link = self.root.locator("a").filter(has_text="Help")
        self.projects_link = self.root.locator("a").filter(has_text="Projects")
        self.user_profile_link = self.root.locator(".mainnav-menu-footer a").last

        self.close_button = self.root.get_by_role("button")

    def is_loaded(self) -> Self:
        expect(self.root).to_be_visible()
        expect(self.tests_link).to_be_visible()
        expect(self.runs_link).to_be_visible()
        expect(self.projects_link).to_be_visible()
        expect(self.user_profile_link).to_be_visible()
        return self

    def expand(self) -> Self:
        menu_class = self.root.get_attribute("class") or ""
        if "mainnav-menu-not-expanded" in menu_class:
            self.open_button.click()
            expect(self.root).not_to_have_class("mainnav-menu-not-expanded")
        return self

    def tab_is_active(self, tab_name: str) -> Self:
        link = self.root.locator("a").filter(has_text=f"{tab_name}")
        expect(link).to_have_class(re.compile(r"\bactive\b"))
        return self

    def click_tests(self) -> Self:
        self.tests_link.click()
        return self

    def click_requirements(self) -> Self:
        self.requirements_link.click()
        return self

    def click_runs(self) -> Self:
        self.runs_link.click()
        return self

    def click_plans(self) -> Self:
        self.plans_link.click()
        return self

    def click_steps(self) -> Self:
        self.steps_link.click()
        return self

    def click_pulse(self) -> Self:
        self.pulse_link.click()
        return self

    def click_imports(self) -> Self:
        self.imports_link.click()
        return self

    def click_analytics(self) -> Self:
        self.analytics_link.click()
        return self

    def click_branches(self) -> Self:
        self.branches_link.click()
        return self

    def click_settings(self) -> Self:
        self.settings_link.click()
        return self

    def click_help(self) -> Self:
        self.help_link.click()
        return self

    def click_projects(self) -> Self:
        self.projects_link.click()
        return self

    def toggle_sidebar(self) -> Self:
        self.close_button.click()
        return self
