import os

from dotenv import load_dotenv
from playwright.sync_api import Page, expect

load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")


def test_login_error_wrong_password(page: Page):
    page.goto('https://testomat.io')

    expect(page.get_by_text("Log in", exact=True)).to_be_visible()
    expect(page).to_have_title("AI Test Management Tool | Testomat.io")

    page.get_by_role("link", name="Log in").click()

    page.locator("#content-desktop #user_email").fill(EMAIL)
    page.locator("#content-desktop #user_password").fill("wrong_password")
    page.get_by_role("button", name="Sign In").click()

    expect(page.locator("#content-desktop").get_by_text("Invalid Email or password.")).to_be_visible()
    expect(page.locator("#content-desktop .common-flash-info")).to_have_text("Invalid Email or password.")




def test_successful_login(page: Page):
    page.goto('https://testomat.io')

    expect(page.get_by_text("Log in", exact=True)).to_be_visible()
    expect(page).to_have_title("AI Test Management Tool | Testomat.io")

    page.get_by_role("link", name="Log in").click()

    page.locator("#content-desktop #user_email").fill(EMAIL)
    page.locator("#content-desktop #user_password").fill(PASSWORD)
    page.get_by_role("button", name="Sign In").click()

    expect(page.locator("#content-desktop").get_by_text("Signed in successfully")).to_be_visible()
    expect(page.locator("#content-desktop .common-flash-success")).to_have_text("Signed in successfully")

    expect(page.get_by_role("link", name="Create")).to_be_visible()

