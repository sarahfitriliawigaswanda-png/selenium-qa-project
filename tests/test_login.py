import pytest
from pages.dashboard_page import DashboardPage

class TestLogin:
    def test_login_valid(self, login_page):
        login_page.login('tomsmith', 'SuperSecretPassword!')
        assert login_page.is_login_successful(), 'Login valid harus berhasil'

    def test_login_invalid_password(self, login_page):
        login_page.login('tomsmith', 'wrongpassword')
        assert login_page.is_login_failed(), 'Login dengan password salah harus gagal'

    def test_login_empty_username(self, login_page):
        login_page.login('', 'SuperSecretPassword!')
        assert login_page.is_login_failed(), 'Login tanpa username harus gagal'

    def test_flash_message_content(self, login_page):
        login_page.login('wronguser', 'wrongpass')
        msg = login_page.get_flash_message()
        assert 'invalid' in msg.lower(), f'Pesan error tidak sesuai: {msg}'

    def test_user_can_logout(self, login_page):
        login_page.login('tomsmith', 'SuperSecretPassword!')
        assert login_page.is_login_successful(), 'Precondition gagal: login tidak berhasil'

        dashboard = DashboardPage(login_page.driver)
        assert dashboard.is_on_dashboard(), 'User seharusnya berada di halaman dashboard'

        dashboard.logout()

        current_url = login_page.get_current_url()
        assert 'login' in current_url or 'secure' not in current_url, \
            f'Setelah logout, user harus keluar dari dashboard. URL: {current_url}'
