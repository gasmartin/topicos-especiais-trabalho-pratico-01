import time

from page_objects import HomePage


def test_insert_book(driver):
    home_page = HomePage(driver)
    home_page.insert_book('9780330491198', 'The Hitchhiker\'s Guide to the Galaxy', 'Douglas Adams', 10, 15)
    time.sleep(3)
    assert home_page.is_book_on_table('9780330491198'), 'Book was not added to the table'
