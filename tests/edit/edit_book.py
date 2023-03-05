import random
import time

from page_objects import HomePage


def test_edit_book(driver):
    home_page = HomePage(driver)
    selected_book = random.choice(home_page.get_registered_books())
    home_page.edit_book(selected_book['isbn'], 'The Philosophy of Jean-Paul Sartre', 'Jean-Paul Sartre', 200, 13)
    time.sleep(3)
    home_page.is_book_on_table(selected_book['isbn'])
    book_info = home_page.search_book(selected_book['isbn'])
    assert book_info['name'] == 'The Philosophy of Jean-Paul Sartre', 'Book name was not updated successfully'
    assert book_info['author'] == 'Jean-Paul Sartre', 'Book author was not updated successfully'
    assert book_info['num_pages'] == 200, 'Book number of pages was not updated successfully'
    assert book_info['num_copies'] == 13, 'Book number of copies was not updated successfully'
