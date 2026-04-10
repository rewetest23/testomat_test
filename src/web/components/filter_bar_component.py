from typing import Self

from playwright.sync_api import Page, expect


class FilterBarComponent:
    def __init__(self, page: Page):
        self.page = page
        self._search_input = self.page.locator("#search")
        self._sub_wrapper = page.locator(".sticky-header .second")

        # Tabs
        self._global_tab = self._sub_wrapper.get_by_role("link", name="Global")
        self._linked_tab = self._sub_wrapper.get_by_role("link", name="Linked")
        self._orphaned_tab = self._sub_wrapper.get_by_role("link", name="Orphaned")
        self._jira_tab = self._sub_wrapper.get_by_role("link", name="Jira")
        self._confluence_tab = self._sub_wrapper.get_by_role("link", name="Confluence")
        self._file_tab = self._sub_wrapper.get_by_role("link", name="File")
        self._text_tab = self._sub_wrapper.get_by_role("link", name="Text")

        self._display_by_suites_button = self._sub_wrapper.locator(".width-settings")

    def is_loaded(self) -> Self:
        expect(self._search_input).to_be_visible()
        expect(self._global_tab).to_be_visible()
        return self

    def search(self, query: str) -> Self:
        self._search_input.fill(query)
        return self

    def click_global_tab(self) -> Self:
        self._global_tab.click()
        return self

    def click_linked_tab(self) -> Self:
        self._linked_tab.click()
        return self

    def click_orphaned_tab(self) -> Self:
        self._orphaned_tab.click()
        return self

    def click_jira_tab(self) -> Self:
        self._jira_tab.click()
        return self

    def click_confluence_tab(self) -> Self:
        self._confluence_tab.click()
        return self

    def click_file_tab(self) -> Self:
        self._file_tab.click()
        return self

    def click_text_tab(self) -> Self:
        self._text_tab.click()
        return self

    def click_display_by_suites(self) -> Self:
        self._display_by_suites_button.click()
        return self
