import pytest
from playwright.sync_api import expect

from src.web.app import App


@pytest.mark.smoke
@pytest.mark.web
def test_switch_from_enterprise_to_free_company(logged_in_app: App):
    logged_in_app.projects_page.navigate()
    expect(logged_in_app.projects_page.enterprise_plan_label).to_be_visible()
    logged_in_app.projects_page.select_company("Free Projects")
    expect(logged_in_app.page.get_by_text("You have not created any projects yet")).to_be_visible()
    expect(logged_in_app.projects_page.free_plan_label).to_be_visible()
    logged_in_app.projects_page.free_plan_label.hover(timeout=500)
    expect(logged_in_app.page.get_by_text("You have a free subscription")).to_be_visible()
