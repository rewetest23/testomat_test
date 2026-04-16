from typing import Self

from playwright.sync_api import Page, expect


class SuiteDetailModal:
    def __init__(self, page: Page):
        self.page = page

        self.title = page.locator(".edit-in-place")

        self.new_test_button = page.get_by_role("link", name="New Test", exact=True)
        self.edit_button = page.get_by_role("button", name="Edit")
        self.comments_button = page.locator('a[href$="/comments"]')

    def is_loaded(self) -> Self:
        expect(self.title).to_be_visible()
        expect(self.new_test_button).to_be_visible()
        expect(self.edit_button).to_be_visible()
        expect(self.comments_button).to_be_visible()
        return self

    def add_new_test(self) -> Self:
        self.new_test_button.click()
        return self

    def check_have_title(self, title: str) -> Self:
        expect(self.title).to_have_text(title)
        return self
