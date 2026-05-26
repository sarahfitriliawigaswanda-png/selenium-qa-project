import pytest
import allure
import csv
import os
from pages.saucedemo_login_page import SauceDemoLoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage

def load_csv(filename):
    filepath = os.path.join('data', filename)
    with open(filepath, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return [row for row in reader]

csv_data = load_csv('saucedemo_login.csv')

@allure.feature('E-Commerce SauceDemo')
class TestSauceDemo:

    @allure.story('Login')
    @allure.title('TC-EC-001: Login valid standard_user')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_valid(self, driver):
        page = SauceDemoLoginPage(driver)
        page.login('standard_user', 'secret_sauce')
        assert page.is_login_successful(), 'Login valid harus berhasil'

    @allure.story('Login')
    @allure.title('TC-EC-002: Login user yang dikunci')
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_locked_user(self, driver):
        page = SauceDemoLoginPage(driver)
        page.login('locked_out_user', 'secret_sauce')
        assert page.is_login_failed(), 'Login locked user harus gagal'

    @allure.story('Login')
    @allure.title('TC-EC-003: Login kredensial invalid')
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_invalid(self, driver):
        page = SauceDemoLoginPage(driver)
        page.login('invalid_user', 'wrong_pass')
        assert page.is_login_failed(), 'Login invalid harus gagal'

    @allure.story('Produk')
    @allure.title('TC-EC-004: Verifikasi jumlah produk 6 item')
    @allure.severity(allure.severity_level.MINOR)
    def test_product_count(self, driver):
        login = SauceDemoLoginPage(driver)
        login.login('standard_user', 'secret_sauce')
        inv = InventoryPage(driver)
        assert inv.get_product_count() == 6, 'Jumlah produk harus 6'

    @allure.story('Produk')
    @allure.title('TC-EC-005: Urutkan produk harga terendah ke tertinggi')
    @allure.severity(allure.severity_level.MINOR)
    def test_sort_price_low_high(self, driver):
        login = SauceDemoLoginPage(driver)
        login.login('standard_user', 'secret_sauce')
        inv = InventoryPage(driver)
        inv.sort_by('lohi')
        prices = inv.get_product_prices()
        assert prices == sorted(prices), 'Produk harus urut dari harga terendah'

    @allure.story('Cart')
    @allure.title('TC-EC-006: Tambah 1 produk ke cart')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_add_one_to_cart(self, driver):
        login = SauceDemoLoginPage(driver)
        login.login('standard_user', 'secret_sauce')
        inv = InventoryPage(driver)
        inv.add_product_to_cart(0)
        assert inv.get_cart_count() == 1, 'Badge cart harus 1'

    @allure.story('Cart')
    @allure.title('TC-EC-007: Tambah 3 produk hapus 1 verifikasi badge 2')
    @allure.severity(allure.severity_level.NORMAL)
    def test_add_three_remove_one(self, driver):
        login = SauceDemoLoginPage(driver)
        login.login('standard_user', 'secret_sauce')
        inv = InventoryPage(driver)
        inv.add_product_to_cart(0)
        inv.add_product_to_cart(1)
        inv.add_product_to_cart(2)
        assert inv.get_cart_count() == 3
        inv.remove_product_from_cart(0)
        assert inv.get_cart_count() == 2, 'Badge cart harus 2 setelah hapus 1'

    @allure.story('Checkout')
    @allure.title('TC-EC-008: Checkout berhasil dengan data lengkap')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_checkout_success(self, driver):
        login = SauceDemoLoginPage(driver)
        login.login('standard_user', 'secret_sauce')
        inv = InventoryPage(driver)
        inv.add_product_to_cart(0)
        inv.go_to_cart()
        cart = CartPage(driver)
        cart.go_to_checkout()
        checkout = CheckoutPage(driver)
        checkout.fill_info('Budi', 'Santoso', '40123')
        checkout.continue_checkout()
        checkout.finish_checkout()
        assert checkout.is_order_confirmed(), 'Order harus terkonfirmasi'

    @allure.story('Checkout')
    @allure.title('TC-EC-009: Checkout gagal field nama kosong')
    @allure.severity(allure.severity_level.NORMAL)
    def test_checkout_empty_name(self, driver):
        login = SauceDemoLoginPage(driver)
        login.login('standard_user', 'secret_sauce')
        inv = InventoryPage(driver)
        inv.add_product_to_cart(0)
        inv.go_to_cart()
        cart = CartPage(driver)
        cart.go_to_checkout()
        checkout = CheckoutPage(driver)
        checkout.fill_info('', 'Santoso', '40123')
        checkout.continue_checkout()
        assert 'checkout-step-one' in driver.current_url, 'Harus tetap di halaman checkout'

    @allure.story('Checkout')
    @allure.title('TC-EC-010: Verifikasi total harga di confirmation page')
    @allure.severity(allure.severity_level.NORMAL)
    def test_checkout_total_price(self, driver):
        login = SauceDemoLoginPage(driver)
        login.login('standard_user', 'secret_sauce')
        inv = InventoryPage(driver)
        inv.add_product_to_cart(0)
        inv.go_to_cart()
        cart = CartPage(driver)
        cart.go_to_checkout()
        checkout = CheckoutPage(driver)
        checkout.fill_info('Budi', 'Santoso', '40123')
        checkout.continue_checkout()
        total = checkout.get_total()
        assert 'Total' in total, 'Harus ada informasi total harga'

    @allure.story('Logout')
    @allure.title('TC-EC-011: User dapat logout setelah login')
    @allure.severity(allure.severity_level.MINOR)
    def test_logout(self, driver):
        login = SauceDemoLoginPage(driver)
        login.login('standard_user', 'secret_sauce')
        inv = InventoryPage(driver)
        inv.logout()
        assert login.is_login_failed() == False
        assert 'saucedemo.com' in driver.current_url

    @allure.story('End-to-End')
    @allure.title('TC-EC-012: Alur penuh Login-Cart-Checkout-Logout')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_full_e2e_flow(self, driver):
        with allure.step('1. Login'):
            login = SauceDemoLoginPage(driver)
            login.login('standard_user', 'secret_sauce')
            assert login.is_login_successful()

        with allure.step('2. Tambah produk ke cart'):
            inv = InventoryPage(driver)
            inv.add_product_to_cart(0)
            assert inv.get_cart_count() == 1

        with allure.step('3. Checkout'):
            inv.go_to_cart()
            cart = CartPage(driver)
            cart.go_to_checkout()
            checkout = CheckoutPage(driver)
            checkout.fill_info('Budi', 'Santoso', '40123')
            checkout.continue_checkout()
            checkout.finish_checkout()
            assert checkout.is_order_confirmed()

        with allure.step('4. Logout'):
            driver.get('https://www.saucedemo.com/inventory.html')
            inv2 = InventoryPage(driver)
            inv2.logout()
            assert 'saucedemo.com' in driver.current_url

        allure.attach(
            driver.get_screenshot_as_png(),
            name='e2e_complete',
            attachment_type=allure.attachment_type.PNG
        )
