from src.web.app import App


def test_fields_validation_new_text_requirement_in_new_project(shared_logged_in_app: App, faker):
    app = shared_logged_in_app
    target_project_name = faker.company()

    (app.new_projects_page
     .open()
     .is_loaded()
     .fill_project_title(target_project_name)
     .click_create())

    (app.project_page
     .is_loaded()
     .side_bar
     .click_requirements())

    (app.requirements_page
     .is_loaded()
     .click_new_requirements())

    (app.requirements_page
     .new_requirement_panel
     .is_loaded()
     .click_text_tab()
     .hover_save_button()
     .tooltip_has_text("Enter a requirement title")
     .save_button_is_disabled()
     .fill_title("Valid Requirement Title")
     .hover_save_button()
     .tooltip_has_text("Description must be at least 500 characters")
     .save_button_is_disabled())


def test_close_new_requirement_panel(shared_logged_in_app: App, faker):
    app = shared_logged_in_app
    target_project_name = faker.company()

    (app.new_projects_page
     .open()
     .is_loaded()
     .fill_project_title(target_project_name)
     .click_create())

    (app.project_page
     .is_loaded()
     .side_bar
     .click_requirements())

    # 1. Close via Back Button
    (app.requirements_page
     .is_loaded()
     .click_new_requirements())

    (app.requirements_page
     .new_requirement_panel
     .is_loaded()
     .click_back()
     .is_hidden())

    # 2. Close via Close Button (Upper right)
    (app.requirements_page
     .click_add_requirement())

    (app.requirements_page
     .new_requirement_panel
     .is_loaded()
     .click_close()
     .is_hidden())

    # 3. Close via Escape Key
    (app.requirements_page
     .click_add_requirement())

    (app.requirements_page
     .new_requirement_panel
     .is_loaded()
     .press_escape()
     .is_hidden())


def test_create_requirement(shared_logged_in_app: App, faker):
    app = shared_logged_in_app
    target_project_name = faker.company()
    requirement_title = faker.catch_phrase()

    requirement_desc = ""
    while len(requirement_desc) <= 500:
        requirement_desc += faker.paragraph(nb_sentences=5) + " "

    (app.new_projects_page
     .open()
     .is_loaded()
     .fill_project_title(target_project_name)
     .click_create())

    (app.project_page
     .is_loaded()
     .side_bar
     .click_requirements())

    # Open panel, fill and cancel
    (app.requirements_page
     .is_loaded()
     .click_new_requirements())

    (app.requirements_page
     .new_requirement_panel
     .is_loaded()
     .click_text_tab()
     .fill_title(requirement_title)
     .fill_description(requirement_desc)
     .click_cancel()
     .is_hidden())

    # Re-open and create for real
    (app.requirements_page
     .click_add_requirement())

    (app.requirements_page
     .new_requirement_panel
     .is_loaded()
     .click_text_tab()
     .fill_title(requirement_title)
     .fill_description(requirement_desc)
     .click_save())

    # Verify Detail View
    (app.requirements_page
     .requirement_details_panel
     .is_loaded()
     .click_close()
     .is_hidden())

    # Verify list
    # TODO: BUG - No title after a new requirement
    """ After successfully saving a new requirement, its title does not
    automatically appear in the list view. The item only becomes visible
    after manually refreshing the page (F5). """
    (app.requirements_page
     .is_loaded()
     .requirement_is_in_list(requirement_title))


def test_search_and_open_requirement(shared_logged_in_app: App):
    app = shared_logged_in_app
    project_name = "Gray Group"
    requirement_title = "Expanded asymmetric synergy"

    (app.projects_page
     .navigate())

    app.projects_page.is_loaded()
    app.projects_page.search_project(project_name)

    project_card = app.projects_page.get_project_by_title(project_name)
    project_card.click()

    (app.project_page
     .is_loaded()
     .side_bar
     .click_requirements())

    (app.requirements_page
     .is_loaded()
     .requirement_is_in_list(requirement_title))
