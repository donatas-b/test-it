import os

from behave import *
from features.constants import *
from selenium import webdriver
from pathlib import Path

from features.lib.page_constants.task_page_constants import TaskPageConstants
from features.lib.pages.task_page import TaskPage


def initialize_page(context):
    current_folder = os.path.dirname(__file__)
    chrome_driver_path = os.path.join(current_folder, CHROME_DRIVER)
    driver = webdriver.Chrome(chrome_driver_path)
    driver.maximize_window()
    driver.get(UI_URL)
    context.browser = driver
    context.page = TaskPage(context)


def validate_page(context):
    assert context.page.title.is_displayed(), 'title element not found'
    assert context.page.title.text == TaskPageConstants.TASK_PAGE_TITLE_TEXT, 'title element: expected text "{}", actual "{}"'.format(TaskPageConstants.TASK_PAGE_TITLE_TEXT, context.page.title.text)
    assert context.page.chart_div.is_displayed(), 'chart element not found'
    chart_data = context.page.chart_data()
    assert len(chart_data) > 0, 'chart data not found'


@given(u'I have UI file')
def step_impl(context):
    current_folder = os.path.dirname(__file__)
    ui_file_name = os.path.join(current_folder, UI_SERVER)
    ui_file = Path(ui_file_name)
    assert ui_file.is_file(), "UI file '{}' not found".format(ui_file_name)
    context.ui_file = ui_file


@when(u'I try to open UI page')
def step_impl(context):
    initialize_page(context)


@then(u'UI page should be opened')
def step_impl(context):
    validate_page(context)


@then(u'UI chart should show correct data')
def step_impl(context):
    chart_data = context.page.chart_data()
    print("UI chart data: {}".format(chart_data))
    assert context.csv_counts == chart_data, "Character counts are not correct in UI - expected '{}', actual '{}'".format(context.csv_counts, chart_data)