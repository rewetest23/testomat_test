from typing import Self

from playwright.sync_api import Page, expect


class RequirementDetailsComponent:
    def __init__(self, page: Page):
        self.page = page

        self.close_button = self.page.locator(".back").get_by_role("button")

        # Tabs
        self.summary_tab = self.page.get_by_role("tab", name="Summary")
        self.suites_tab = self.page.get_by_role("tab", name="Suites")
        self.source_tab = self.page.get_by_role("tab", name="Source")
        self.attachments_tab = self.page.get_by_role("tab", name="Attachments")

    def is_loaded(self) -> Self:
        expect(self.summary_tab).to_be_visible()
        expect(self.suites_tab).to_be_visible()
        expect(self.source_tab).to_be_visible()
        expect(self.attachments_tab).to_be_visible()
        return self

    def click_close(self) -> Self:
        self.close_button.click()
        return self

    def is_hidden(self) -> Self:
        expect(self.summary_tab).to_be_hidden()
        expect(self.suites_tab).to_be_hidden()
        expect(self.source_tab).to_be_hidden()
        expect(self.attachments_tab).to_be_hidden()
        return self
