from typing import Self

from playwright.sync_api import Page, expect


class RequirementDetailsComponent:
    def __init__(self, page: Page):
        self.page = page

        self._close_button = self.page.locator(".back").get_by_role("button")

        # Tabs
        self._summary_tab = self.page.get_by_role("tab", name="Summary")
        self._suites_tab = self.page.get_by_role("tab", name="Suites")
        self._source_tab = self.page.get_by_role("tab", name="Source")
        self._attachments_tab = self.page.get_by_role("tab", name="Attachments")

    def is_loaded(self) -> Self:
        expect(self._summary_tab).to_be_visible()
        expect(self._suites_tab).to_be_visible()
        expect(self._source_tab).to_be_visible()
        expect(self._attachments_tab).to_be_visible()
        return self

    def click_close(self) -> Self:
        self._close_button.click()
        return self

    def is_hidden(self) -> Self:
        expect(self._summary_tab).to_be_hidden()
        expect(self._suites_tab).to_be_hidden()
        expect(self._source_tab).to_be_hidden()
        expect(self._attachments_tab).to_be_hidden()
        return self
