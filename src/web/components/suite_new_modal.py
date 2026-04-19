from typing import Self

from playwright.sync_api import Page, expect


class SuiteNewModal:
    def __init__(self, page: Page):
        self.page = page

        self.heading = page.get_by_role("heading", name="New Suite")

        self.title = page.get_by_role("combobox", name="Title")
        self.save_button = page.get_by_role("button", name="Save")
        self.cancel_button = page.get_by_role("link", name="Cancel")

    def is_loaded(self) -> Self:
        expect(self.title).to_be_visible()
        expect(self.save_button).to_be_visible()
        expect(self.cancel_button).to_be_visible()
        return self

    def fill_title_and_save(self, suite_title: str) -> Self:
        self.title.fill(suite_title)
        self.save_button.click()
        return self
