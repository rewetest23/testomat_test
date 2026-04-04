from typing import Self

from playwright.sync_api import Page, expect


class NewRequirementComponent:
    def __init__(self, page: Page):
        self.page = page

        # Header actions
        self.__close_button = self.page.locator(".detail-view-actions").get_by_role("button")
        self.__back_button = self.page.locator(".back").get_by_role("button")

        self.__root = page.locator(".detail-view-content")

        # Tabs
        self.__tab_jira = self.__root.get_by_role("tab", name="Jira")
        self.__tab_confluence = self.__root.get_by_role("tab", name="Confluence")
        self.__tab_file = self.__root.get_by_role("tab", name="File")
        self.__tab_text = self.__root.get_by_role("tab", name="Text")

        self.__active_tab_panel = self.__root.locator("li[role='tabpanel'].active")

        # Common Form Elements within active tab
        self.__title_input = self.__active_tab_panel.locator("input[name='requirement[title]']")

        # Text Tab specific
        self.__description_textarea = self.__active_tab_panel.locator("textarea[name='requirement[description]']")

        # File Tab specific
        self.__file_input = self.__active_tab_panel.locator("#upload-image")

        # Actions
        self.__save_button = self.__active_tab_panel.get_by_role("button", name="Save")
        self.__cancel_button = self.__active_tab_panel.get_by_role("button", name="Cancel")

        # Tooltip
        self.__tooltip = self.page.get_by_role("tooltip")

    def is_loaded(self) -> Self:
        expect(self.__root).to_be_visible()
        expect(self.__root.get_by_role("heading", name="New Requirement")).to_be_visible()
        return self

    def is_hidden(self) -> Self:
        expect(self.__root).to_be_hidden()
        return self

    def click_close(self) -> Self:
        self.__close_button.click()
        return self

    def click_back(self) -> Self:
        self.__back_button.click()
        return self

    def press_escape(self) -> Self:
        self.page.keyboard.press("Escape")
        return self

    def click_jira_tab(self) -> Self:
        self.__tab_jira.click()
        return self

    def click_confluence_tab(self) -> Self:
        self.__tab_confluence.click()
        return self

    def click_file_tab(self) -> Self:
        self.__tab_file.click()
        return self

    def click_text_tab(self) -> Self:
        self.__tab_text.click()
        return self

    # Form actions
    def fill_title(self, title: str) -> Self:
        self.__title_input.fill(title)
        return self

    def fill_description(self, description: str) -> Self:
        self.__description_textarea.fill(description)
        return self

    def upload_file(self, file_path: str) -> Self:
        self.__file_input.set_input_files(file_path)
        return self

    def click_save(self) -> Self:
        self.__save_button.click()
        return self

    def click_cancel(self) -> Self:
        self.__cancel_button.click()
        return self

    def hover_save_button(self) -> Self:
        self.__save_button.hover()
        return self

    def tooltip_has_text(self, expected_text: str) -> Self:
        expect(self.__tooltip).to_contain_text(expected_text)
        return self

    def save_button_is_enabled(self) -> Self:
        expect(self.__save_button).to_be_enabled()
        return self

    def save_button_is_disabled(self) -> Self:
        expect(self.__save_button).to_be_disabled()
        return self
