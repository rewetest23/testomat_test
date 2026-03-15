import pytest
from faker import Faker
from playwright.sync_api import Page, expect

from conftest import Config

TARGET_PROJECT = "nbb"
DEMO_PROJECT = "Cypress Demo Project"


@pytest.fixture(scope="function")
def login(page: Page, configs: Config):
    page.goto(configs.sign_in_url)
    login_user(page, configs.email, configs.password)


def test_login_error_wrong_password(page: Page, configs: Config):
    open_home_page(page, configs)

    expect(page.get_by_text("Log in", exact=True)).to_be_visible()
    page.get_by_role("link", name="Log in").click()

    login_user(page, configs.email, Faker().password(length=10))

    expect(page.locator("#content-desktop").get_by_text("Invalid Email or password.")).to_be_visible()
    expect(page.locator("#content-desktop .common-flash-info")).to_have_text("Invalid Email or password.")


def test_successful_login(page: Page, login):
    expect(page.locator("#content-desktop").get_by_text("Signed in successfully")).to_be_visible()
    expect(page.locator("#content-desktop .common-flash-success")).to_have_text("Signed in successfully")

    expect(page.get_by_role("link", name="Create")).to_be_visible()


def test_search_project_in_company(page: Page, login):
    search_for_project(page, TARGET_PROJECT)

    expect(page.get_by_role("heading", name=TARGET_PROJECT)).to_be_visible()


def test_should_be_possible_to_open_free_project(page: Page, login):
    # page.locator("#company_id").click()
    page.locator("#company_id").select_option("Free Projects")

    search_for_project(page, TARGET_PROJECT)
    expect(page.get_by_role("heading", name=TARGET_PROJECT)).to_be_hidden()

    expect(page.get_by_text("You have not created any projects yet")).to_be_visible(timeout=10000)


def test_all_projects_should_be_visible_after_delete_input_search(page: Page, login):
    all_projects = page.locator('#grid li')
    hidden_projects = page.locator('#grid li[style*="display: none"]')

    page.locator("#company_id").select_option("QA Club Lviv")

    expect(page.locator('#grid')).to_be_visible()

    assert all_projects.count() > 0, "Expected at least one project (li element) to be in the grid!"
    expect(hidden_projects).to_have_count(0)

    search_for_project(page, TARGET_PROJECT)
    expect(hidden_projects).to_have_count(all_projects.count() - 1)

    page.locator("#content-desktop #search").clear()
    expect(hidden_projects).to_have_count(0)


def test_create_classical_cypress_demo_project(page: Page, login):
    page.get_by_role("link", name="Create").click()

    page.locator("#classical").click()
    page.locator("#project_title").fill(DEMO_PROJECT)

    page.locator("#demo-btn").check()
    page.get_by_role("button", name="Cypress Demo Project").click()

    page.get_by_role("button", name="Create Demo").click()

    expect(page.get_by_role("link", name="Out of sync", exact=True)).to_be_visible()
    expect(page.get_by_role("link", name="Detached", exact=True)).to_be_visible()


def test_delete_classical_cypress_demo_project(page: Page, configs: Config, login):
    search_for_project(page, DEMO_PROJECT)
    expect(page.get_by_role("heading", name=DEMO_PROJECT)).to_be_visible()

    page.get_by_role("link", name=DEMO_PROJECT).first.click()

    page.locator('a:has(svg.md-icon-cog)').click()  # Click Settings

    page.on("dialog", lambda dialog: dialog.accept())
    page.get_by_role("button", name="Administration").click()

    page.on("dialog", lambda dialog: dialog.accept())
    page.get_by_role("button", name="Delete Project").click()

    expect(page.get_by_text("Project will be deleted in few minutes")).to_be_visible()

    page.goto(configs.base_app_url)
    search_for_project(page, DEMO_PROJECT)
    expect(page.get_by_role("heading", name=DEMO_PROJECT)).not_to_be_visible()


def search_for_project(page: Page, target_project: str):
    expect(page.get_by_role("searchbox", name="Search")).to_be_visible()
    page.locator("#content-desktop #search").fill(target_project)


def open_home_page(page: Page, configs: Config):
    page.goto(configs.base_url)
    expect(page).to_have_title("AI Test Management Tool | Testomat.io")


def login_user(page: Page, email: str, password: str):
    page.locator("#content-desktop #user_email").fill(email)
    page.locator("#content-desktop #user_password").fill(password)
    page.get_by_role("button", name="Sign In").click()
