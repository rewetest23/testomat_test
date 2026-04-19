from typing import Self

from playwright.sync_api import Page, expect


class TestDetailModal:
    def __init__(self, page: Page):
        self.page = page

        self.title = page.locator(".edit-in-place")

        self.edit_button = page.get_by_role("button", name="Edit", exact=True)
        self.comments_button = page.locator('a[href$="/comments"]')

    def is_loaded(self) -> Self:
        expect(self.title).to_be_visible()
        expect(self.edit_button).to_be_visible()
        expect(self.comments_button).to_be_visible()
        return self

    def check_have_title(self, test_title: str) -> Self:
        expect(self.title).to_have_text(test_title)
        return self
