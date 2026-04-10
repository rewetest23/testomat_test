from enum import Enum
from typing import Self

from playwright.sync_api import Locator, expect


# AI generated
class ProjectCardComponent:

    def __init__(self, root_locator: Locator):
        self._root = root_locator

        self._link = self._root.locator("a")
        self._title = self._root.locator("h3")
        self._test_count = self._root.locator("p").filter(has_text="tests")
        self._badges = self._root.locator(".project-badges")

    def get_title(self) -> str:
        return self._title.inner_text()

    def get_test_count_text(self) -> str:
        return self._test_count.inner_text()

    def badges_has(self, expected_badge: Badges) -> Self:
        expect(self._badges).to_contain_text(expected_badge.value)
        return self

    def click(self) -> Self:
        self._link.click()
        return self


class Badges(Enum):
    DEMO = "Demo"
    CLASSICAL = "Classical"
    TEST = "Test"
