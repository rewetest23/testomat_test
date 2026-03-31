from enum import Enum

from playwright.sync_api import Locator, expect


# AI generated
class ProjectCardComponent:

    def __init__(self, root_locator: Locator):
        self.root = root_locator

        self.link = self.root.locator("a")
        self.title = self.root.locator("h3")
        self.test_count = self.root.locator("p.text-gray-500")
        self.badges = self.root.locator(".project-badges")

    def get_title(self) -> str:
        return self.title.inner_text()

    def get_test_count_text(self) -> str:
        return self.test_count.inner_text()

    def badges_has(self, expected_badge: Badges):
        expect(self.badges).to_contain_text(expected_badge.value)

    def click(self):
        self.link.click()


class Badges(Enum):
    DEMO = "Demo"
    CLASSICAL = "Classical"
    TEST = "Test"
