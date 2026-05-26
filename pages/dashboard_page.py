from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class DashboardPage(BasePage):
    URL = 'https://the-internet.herokuapp.com/secure'
    LOGOUT_BTN = (By.CSS_SELECTOR, 'a[href="/logout"]')
    DASHBOARD_HEADER = (By.TAG_NAME, 'h2')

    def logout(self):
        self.click(self.LOGOUT_BTN)

    def is_on_dashboard(self):
        return self.get_current_url() == self.URL and \
               self.is_visible(self.LOGOUT_BTN)
