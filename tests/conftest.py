import pytest
import os
from selenium import webdriver

@pytest.fixture(scope='function')
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    d = webdriver.Chrome(options=options)
    yield d
    d.quit()

@pytest.fixture(scope='function')
def login_page(driver):
    from pages.login_page import LoginPage
    return LoginPage(driver)
