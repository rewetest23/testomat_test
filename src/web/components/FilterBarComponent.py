import re
from typing import Self

from playwright.sync_api import Page, expect


class FilterBarComponent:
    def __init__(self, page: Page):
        self.page = page
        self.root = page.locator(".filterbar-v2")
        self.sub_wrapper = page.locator(".filterbar-v2-sub-wrapper")
        
        self.search_input = self.root.get_by_placeholder("Search [Ctrl + K]")
        
        # Tabs
        self.global_tab = self.sub_wrapper.get_by_role("link", name=re.compile(r"Global"))
        self.linked_tab = self.sub_wrapper.get_by_role("link", name=re.compile(r"Linked"))
        self.orphaned_tab = self.sub_wrapper.get_by_role("link", name=re.compile(r"Orphaned"))
        self.jira_tab = self.sub_wrapper.get_by_role("link", name=re.compile(r"Jira"))
        self.confluence_tab = self.sub_wrapper.get_by_role("link", name=re.compile(r"Confluence"))
        self.file_tab = self.sub_wrapper.get_by_role("link", name=re.compile(r"File"))
        self.text_tab = self.sub_wrapper.get_by_role("link", name=re.compile(r"Text"))
        
        self.display_by_suites_button = self.sub_wrapper.get_by_role("button", name=re.compile(r"Display by Suites|Display by Tree"))

    def is_loaded(self) -> Self:
        expect(self.search_input).to_be_visible()
        expect(self.global_tab).to_be_visible()
        return self

    def search(self, query: str):
        self.search_input.fill(query)

    def click_global_tab(self):
        self.global_tab.click()

    def click_linked_tab(self):
        self.linked_tab.click()
        
    def click_orphaned_tab(self):
        self.orphaned_tab.click()

    def click_jira_tab(self):
        self.jira_tab.click()

    def click_confluence_tab(self):
        self.confluence_tab.click()

    def click_file_tab(self):
        self.file_tab.click()

    def click_text_tab(self):
        self.text_tab.click()

    def click_display_by_suites(self):
        self.display_by_suites_button.click()
