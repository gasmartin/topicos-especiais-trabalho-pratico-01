import random
import time

from page_objects import HomePage


def test_delete_book(driver):
    home_page = HomePage(driver)
    isbn = random.choice(home_page.get_registered_books())['isbn']
    home_page.delete_book(isbn)
    time.sleep(3)
    deleted = not home_page.is_book_on_table(isbn)
    assert deleted, 'Book was not removed from table'
