from enum import Enum

from playwright.sync_api import Locator, expect


# AI generated
class ProjectCardComponent:

    def __init__(self, root_locator: Locator):
        self.__root = root_locator

        self.__link = self.__root.locator("a")
        self.__title = self.__root.locator("h3")
        self.__test_count = self.__root.locator("p").filter(has_text="tests")
        self.__badges = self.__root.locator(".project-badges")

    def get_title(self) -> str:
        return self.__title.inner_text()

    def get_test_count_text(self) -> str:
        return self.__test_count.inner_text()

    def badges_has(self, expected_badge: Badges):
        expect(self.__badges).to_contain_text(expected_badge.value)

    def click(self):
        self.__link.click()


class Badges(Enum):
    DEMO = "Demo"
    CLASSICAL = "Classical"
    TEST = "Test"
