from typing import Self

from playwright.sync_api import Page, expect


class TestEditModal:
    def __init__(self, page: Page):
        self.page = page

        # The main wrapper that contains BOTH the header (save/back buttons) and the content
        self.container = page.locator(".detail-view-resizable")

        self.heading = self.container.get_by_role("heading", name="Edit Test")
        self.save_button = self.container.get_by_role("button", name="Save")
        self.go_back_button = self.container.get_by_role("button", name="Go Back")
        self.title = self.container.get_by_role("combobox", name="Title")

    def is_loaded(self) -> Self:
        expect(self.heading).to_be_visible()
        expect(self.title).to_be_visible()
        expect(self.save_button).to_be_visible()
        expect(self.go_back_button).to_be_visible()
        return self

    def set_title(self, title: str) -> Self:
        self.title.fill(title)
        return self

    def save(self) -> Self:
        self.save_button.click()
        return self
