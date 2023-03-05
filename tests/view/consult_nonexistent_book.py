from page_objects import HomePage, BookDoesNotExist


def test_consult_nonexistent_book(driver):
    home_page = HomePage(driver)
    try:
        home_page.search_book('12345')
    except BookDoesNotExist:
        pass
    else:
        raise AssertionError('A nonexistent book was found')
