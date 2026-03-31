import re
from typing import Self

from playwright.sync_api import Page, expect


class RequirementDetailsComponent:
    def __init__(self, page: Page):
        self.page = page
        self.root = page.locator(".detail-view-resizable:not(#_clone)")
        
        self.__close_button = self.root.locator(".back").get_by_role("button")

        # Tabs
        self.__summary_tab = self.root.get_by_role("tab", name=re.compile(r"Summary", re.IGNORECASE))
        self.__suites_tab = self.root.get_by_role("tab", name=re.compile(r"Suites", re.IGNORECASE))
        self.__source_tab = self.root.get_by_role("tab", name=re.compile(r"Source", re.IGNORECASE))
        self.__attachments_tab = self.root.get_by_role("tab", name=re.compile(r"Attachments", re.IGNORECASE))

    def is_loaded(self) -> Self:
        expect(self.root).to_be_visible()
        expect(self.__summary_tab).to_be_visible()
        expect(self.__suites_tab).to_be_visible()
        expect(self.__source_tab).to_be_visible()
        expect(self.__attachments_tab).to_be_visible()
        return self

    def click_close(self) -> Self:
        self.__close_button.click()
        return self

    def is_hidden(self) -> Self:
        expect(self.root).to_be_hidden()
        return self

