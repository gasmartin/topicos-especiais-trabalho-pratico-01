import time

from page_objects import HomePage


def test_insert_book_with_invalid_properties(driver):
    home_page = HomePage(driver)
    home_page.insert_book('xxxxxx', '-1', '-1', 10, 2)
    time.sleep(3)
    assert not home_page.is_book_on_table('xxxxxx')
