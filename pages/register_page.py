from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from pages.base_page import BasePage

class RegisterPage(BasePage):
    URL = 'https://demoqa.com/register'

    FIRST_NAME   = (By.ID, 'firstname')
    LAST_NAME    = (By.ID, 'lastname')
    USERNAME     = (By.ID, 'userName')
    PASSWORD     = (By.ID, 'password')
    REGISTER_BTN = (By.ID, 'register')
    SUCCESS_MSG  = (By.ID, 'name')
    ERROR_MSG    = (By.CSS_SELECTOR, 'p.mb-1')

    def navigate(self):
        self.open(self.URL)

    def fill_form(self, first_name, last_name, username, password):
        if first_name:
            self.type(self.FIRST_NAME, first_name)
        if last_name:
            self.type(self.LAST_NAME, last_name)
        if username:
            self.type(self.USERNAME, username)
        if password:
            self.type(self.PASSWORD, password)

    def click_register(self):
        btn = self.find_clickable(self.REGISTER_BTN)
        self.driver.execute_script('arguments[0].scrollIntoView(true);', btn)
        self.driver.execute_script('arguments[0].click();', btn)

    def is_register_successful(self):
        return self.is_visible(self.SUCCESS_MSG)

    def is_register_failed(self):
        if self.is_visible(self.ERROR_MSG):
            return True
        return 'register' in self.get_current_url()
