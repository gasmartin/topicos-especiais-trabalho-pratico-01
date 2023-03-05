import random

from page_objects import HomePage


def test_consult_book(driver):
    home_page = HomePage(driver)
    selected_book = random.choice(home_page.get_registered_books())
    book_info = home_page.search_book(selected_book['isbn'])
    assert book_info['name'] == selected_book['name'], 'Retrieved book name is incorrect'
    assert book_info['author'] == selected_book['author'], 'Retrieved book author is incorrect'
    assert book_info['num_pages'] == selected_book['num_pages'], 'Retrieved book name is incorrect'
    assert book_info['num_copies'] == selected_book['num_copies'], 'Retrieved book name is incorrect'
