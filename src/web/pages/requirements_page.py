import re
from typing import Self

from playwright.sync_api import Page, expect

from src.web.components import (
    FilterBarComponent,
    NewRequirementComponent,
    RequirementDetailsComponent,
    SideBarComponent,
)


class RequirementsPage:
    def __init__(self, page: Page):
        self.page = page
        self.side_bar = SideBarComponent(page)
        self.filter_bar = FilterBarComponent(page)
        self.new_requirement_panel = NewRequirementComponent(page)
        self.requirement_details_panel = RequirementDetailsComponent(page)

        self._breadcrumbs = page.locator(".breadcrumbs-page")
        self._add_requirement_button = page.locator("a", has_text="Add Requirement")
        self._chat_with_requirements_button = page.get_by_role("button", name="Chat with Requirements")
        
        self._empty_state_header = page.get_by_role("heading", name="Requirements")
        self._empty_state_text = page.get_by_text("No requirements yet! Create your first requirement to get started.")
        self._new_requirements_button = page.locator("a", has_text="New Requirements")

    def is_loaded(self) -> Self:
        expect(self._breadcrumbs).to_be_visible()
        self.filter_bar.is_loaded()
        expect(self._add_requirement_button).to_be_visible()
        return self

    def empty_state_is_visible(self) -> Self:
        expect(self._empty_state_header).to_be_visible()
        expect(self._empty_state_text).to_be_visible()
        return self

    def click_add_requirement(self) -> Self:
        self._add_requirement_button.click()
        return self

    def click_chat_with_requirements(self) -> Self:
        self._chat_with_requirements_button.click()
        return self

    def click_new_requirements(self) -> Self:
        self._new_requirements_button.click()
        return self
        
    def requirement_is_in_list(self, title: str) -> Self:
        expect(self.page.locator("li.list-item-border").filter(has_text=re.compile(title))).to_be_visible()
        return self
