import re
from typing import Self

from playwright.sync_api import Page, expect


class SideBarComponent:

    def __init__(self, page: Page):
        self.page = page
        self.root = page.locator(".mainnav-menu")

        self.tests_link = self.root.locator("a").filter(has_text=re.compile(r"\bTests\b"))
        self.requirements_link = self.root.locator("a").filter(has_text=re.compile(r"\bRequirements\b"))
        self.runs_link = self.root.locator("a").filter(has_text=re.compile(r"\bRuns\b"))
        self.plans_link = self.root.locator("a").filter(has_text=re.compile(r"\bPlans\b"))
        self.steps_link = self.root.locator("a").filter(has_text=re.compile(r"\bSteps\b"))
        self.pulse_link = self.root.locator("a").filter(has_text=re.compile(r"\bPulse\b"))
        self.imports_link = self.root.locator("a").filter(has_text=re.compile(r"\bImports\b"))
        self.analytics_link = self.root.locator("a").filter(has_text=re.compile(r"\bAnalytics\b"))
        self.branches_link = self.root.locator("a").filter(has_text=re.compile(r"\bBranches\b"))
        self.settings_link = self.root.locator("a").filter(has_text=re.compile(r"\bSettings\b"))

        self.help_link = self.root.locator("a").filter(has_text=re.compile(r"\bHelp\b"))
        self.projects_link = self.root.locator("a").filter(has_text=re.compile(r"\bProjects\b"))
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
            self.root.locator("button.btn-open").click(force=True)
            expect(self.root).not_to_have_class(re.compile(r"mainnav-menu-not-expanded"))
        return self

    def tab_is_active(self, tab_name: str) -> Self:
        link = self.root.locator("a").filter(has_text=re.compile(rf"\b{tab_name}\b"))
        expect(link).to_have_class(re.compile(r"\bactive\b"))
        return self


    def click_tests(self):
        self.tests_link.click()

    def click_requirements(self):
        self.requirements_link.click()

    def click_runs(self):
        self.runs_link.click()

    def click_plans(self):
        self.plans_link.click()

    def click_steps(self):
        self.steps_link.click()

    def click_pulse(self):
        self.pulse_link.click()

    def click_imports(self):
        self.imports_link.click()

    def click_analytics(self):
        self.analytics_link.click()

    def click_branches(self):
        self.branches_link.click()

    def click_settings(self):
        self.settings_link.click()

    def click_help(self):
        self.help_link.click()

    def click_projects(self):
        self.projects_link.click()

    def toggle_sidebar(self):
        self.close_button.click()
