from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CartPage(BasePage):
    CART_ITEMS   = (By.CLASS_NAME, 'cart_item')
    REMOVE_BTNS  = (By.CSS_SELECTOR, '[data-test^=remove]')
    CHECKOUT_BTN = (By.CSS_SELECTOR, '[data-test=checkout]')
    CONTINUE_BTN = (By.CSS_SELECTOR, '[data-test=continue-shopping]')

    def get_cart_item_count(self):
        return len(self.driver.find_elements(*self.CART_ITEMS))

    def remove_item(self, index=0):
        btns = self.driver.find_elements(*self.REMOVE_BTNS)
        btns[index].click()

    def go_to_checkout(self):
        self.click(self.CHECKOUT_BTN)

    def continue_shopping(self):
        self.click(self.CONTINUE_BTN)
