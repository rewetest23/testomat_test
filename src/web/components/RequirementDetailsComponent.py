from typing import Self

from playwright.sync_api import Page, expect


class RequirementDetailsComponent:
    def __init__(self, page: Page):
        self.page = page

        self.__close_button = self.page.locator(".back").get_by_role("button")

        # Tabs
        self.__summary_tab = self.page.get_by_role("tab", name="Summary")
        self.__suites_tab = self.page.get_by_role("tab", name="Suites")
        self.__source_tab = self.page.get_by_role("tab", name="Source")
        self.__attachments_tab = self.page.get_by_role("tab", name="Attachments")

    def is_loaded(self) -> Self:
        expect(self.__summary_tab).to_be_visible()
        expect(self.__suites_tab).to_be_visible()
        expect(self.__source_tab).to_be_visible()
        expect(self.__attachments_tab).to_be_visible()
        return self

    def click_close(self) -> Self:
        self.__close_button.click()
        return self

    def is_hidden(self) -> Self:
        expect(self.__summary_tab).to_be_hidden()
        expect(self.__suites_tab).to_be_hidden()
        expect(self.__source_tab).to_be_hidden()
        expect(self.__attachments_tab).to_be_hidden()
        return self
