import pytest

from selenium.webdriver import Chrome


@pytest.fixture
def driver():
    driver = Chrome()
    driver.maximize_window()
    driver.get('http://localhost:3000')
    yield driver
    driver.quit()
