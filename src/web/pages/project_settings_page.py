from typing import Self

from playwright.sync_api import Page, expect

from src.web.components import SideBarComponent


class ProjectSettingsPage:
    def __init__(self, page: Page):
        self.page = page
        self.side_bar = SideBarComponent(page)

        self.administration_button = page.get_by_role("button", name="Administration")
        self.delete_project_button = page.get_by_role("button", name="Delete Project")

    def is_loaded(self) -> Self:
        expect(self.administration_button).to_be_visible()
        return self

    def click_administration_button_and_confirm(self) -> Self:
        self.page.on("dialog", lambda dialog: dialog.accept())
        self.administration_button.click()
        return self

    def click_delete_project_button_and_confirm(self) -> Self:
        self.page.on("dialog", lambda dialog: dialog.accept())
        self.delete_project_button.click()
        return self

    def delete_project(self) -> Self:
        self.click_administration_button_and_confirm()
        self.click_delete_project_button_and_confirm()
        expect(self.page.get_by_text("Project will be deleted in few minutes")).to_be_visible()
        return self
