import time
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

from features.lib.page_constants.task_page_constants import TaskPageConstants


class TaskPage:
    def __init__(self, context):
        self.browser = context.browser
        self.title = self.browser.find_element(By.TAG_NAME, TaskPageConstants.TASK_PAGE_TITLE_ID)
        self.chart_div = self.browser.find_element(By.ID, TaskPageConstants.TASK_PAGE_CHART_ID)
        self.chart_data_table = self.chart_data()

    def title_double_click(self):
        ActionChains(self.browser).double_click(self.title).perform()
        time.sleep(15)

    def chart_data(self):
        data = {}
        table_reader = BeautifulSoup(self.browser.page_source, 'html.parser')
        tbody = table_reader.find('tbody')
        if tbody is not None:
            rows = tbody.find_all('tr')
            for row in rows:
                cells = row.find_all('td')
                if cells[0].text == '':
                    data[' '] = int(cells[1].text)
                else:
                    data[cells[0].text] = int(cells[1].text)
        return data
