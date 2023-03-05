import random
import time

from page_objects import HomePage


def test_delete_book(driver):
    home_page = HomePage(driver)
    selected_book = random.choice(home_page.get_registered_books())
    home_page.delete_book(selected_book['isbn'])
    time.sleep(3)
    assert not home_page.is_book_on_table(selected_book['isbn']), 'Book was not removed from table'
