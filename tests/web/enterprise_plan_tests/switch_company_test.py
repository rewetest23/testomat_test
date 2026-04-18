import pytest
from playwright.sync_api import expect

from src.web.app import App


@pytest.mark.smoke
@pytest.mark.web
def test_switch_from_enterprise_to_free_company(app: App):
    app.projects_page.navigate()
    expect(app.projects_page.enterprise_plan_label).to_be_visible()
    app.projects_page.select_company("Free Projects")
    expect(app.page.get_by_text("You have not created any projects yet")).to_be_visible()
    expect(app.projects_page.free_plan_label).to_be_visible()
    app.projects_page.free_plan_label.hover(timeout=500)
    expect(app.page.get_by_text("You have a free subscription")).to_be_visible()
