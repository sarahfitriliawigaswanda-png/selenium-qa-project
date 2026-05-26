import pytest
import csv
import os
from pages.register_page import RegisterPage

def load_csv(filename):
    filepath = os.path.join('data', filename)
    with open(filepath, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return [row for row in reader]

csv_data = load_csv('register_data.csv')

class TestRegisterDDT:
    @pytest.mark.parametrize(
        'row',
        csv_data,
        ids=[row['description'] for row in csv_data]
    )
    def test_register(self, driver, row):
        page = RegisterPage(driver)
        page.navigate()
        page.fill_form(
            first_name=row['first_name'],
            last_name=row['last_name'],
            username=row['username'],
            password=row['password']
        )
        page.click_register()

        if row['expected'] == 'PASS':
            assert page.is_register_successful(), \
                f"[{row['description']}] Registrasi seharusnya BERHASIL"
        else:
            assert page.is_register_failed(), \
                f"[{row['description']}] Registrasi seharusnya GAGAL"
