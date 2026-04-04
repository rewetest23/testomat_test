from typing import Self

from playwright.sync_api import Page, expect


class FilterBarComponent:
    def __init__(self, page: Page):
        self.page = page
        self.__search_input = self.page.locator("#search")
        self.__sub_wrapper = page.locator(".sticky-header .second")

        # Tabs
        self.__global_tab = self.__sub_wrapper.get_by_role("link", name="Global")
        self.__linked_tab = self.__sub_wrapper.get_by_role("link", name="Linked")
        self.__orphaned_tab = self.__sub_wrapper.get_by_role("link", name="Orphaned")
        self.__jira_tab = self.__sub_wrapper.get_by_role("link", name="Jira")
        self.__confluence_tab = self.__sub_wrapper.get_by_role("link", name="Confluence")
        self.__file_tab = self.__sub_wrapper.get_by_role("link", name="File")
        self.__text_tab = self.__sub_wrapper.get_by_role("link", name="Text")

        self.__display_by_suites_button = self.__sub_wrapper.locator(".width-settings")

    def is_loaded(self) -> Self:
        expect(self.__search_input).to_be_visible()
        expect(self.__global_tab).to_be_visible()
        return self

    def search(self, query: str) -> Self:
        self.__search_input.fill(query)
        return self

    def click_global_tab(self) -> Self:
        self.__global_tab.click()
        return self

    def click_linked_tab(self) -> Self:
        self.__linked_tab.click()
        return self

    def click_orphaned_tab(self) -> Self:
        self.__orphaned_tab.click()
        return self

    def click_jira_tab(self) -> Self:
        self.__jira_tab.click()
        return self

    def click_confluence_tab(self) -> Self:
        self.__confluence_tab.click()
        return self

    def click_file_tab(self) -> Self:
        self.__file_tab.click()
        return self

    def click_text_tab(self) -> Self:
        self.__text_tab.click()
        return self

    def click_display_by_suites(self) -> Self:
        self.__display_by_suites_button.click()
        return self
