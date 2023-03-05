import time

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


class BookDoesNotExist(Exception):
    def __init__(self, isbn):
        Exception.__init__(self, f'Book with ISBN = {repr(isbn)} does not exist')


class HomePage(object):
    title_by = (By.XPATH, '/html/body/div/div/div/div[1]/h1')

    # Buttons at the top of the page
    register_button_by = (By.XPATH, '/html/body/div/div/div/div[2]/div/div[1]/button')
    search_button_by = (By.XPATH, '/html/body/div/div/div/div[2]/div/div[2]/button')

    # Register modal
    isbn_input_by = (By.XPATH, '/html/body/div[3]/div/div/form/div[1]/div/div[1]/input')
    name_input_by = (By.XPATH, '/html/body/div[3]/div/div/form/div[1]/div/div[2]/input')
    author_input_by = (By.XPATH, '/html/body/div[3]/div/div/form/div[1]/div/div[3]/input')
    num_pages_input_by = (By.XPATH, '/html/body/div[3]/div/div/form/div[1]/div/div[4]/input')
    num_copies_input_by = (By.XPATH, '/html/body/div[3]/div/div/form/div[1]/div/div[5]/input')
    save_button_by = (By.XPATH, '/html/body/div[3]/div/div/form/div[2]/button')

    # Search modal
    search_modal_isbn_input_by = (By.XPATH, '/html/body/div[3]/div/div/div[2]/div/form/div/div/div/input')
    search_modal_search_button_by = (By.XPATH, '//*[@id="button-search"]')
    search_modal_book_data_container_by = (By.XPATH, '/html/body/div[3]/div/div/div[2]/div/div')

    def __init__(self, driver):
        self.driver = driver

    def get_title(self):
        return self.driver.find_element(*self.title_by).text

    def insert_book(self, isbn, name, author, num_pages, num_copies):
        self.driver.find_element(*self.register_button_by).click()
        time.sleep(1)
        self.driver.find_element(*self.isbn_input_by).send_keys(isbn)
        time.sleep(1)
        self.driver.find_element(*self.name_input_by).send_keys(name)
        time.sleep(1)
        self.driver.find_element(*self.author_input_by).send_keys(author)
        time.sleep(1)
        self.driver.find_element(*self.num_pages_input_by).send_keys(num_pages)
        time.sleep(1)
        self.driver.find_element(*self.num_copies_input_by).send_keys(num_copies)
        time.sleep(5)
        self.driver.find_element(*self.save_button_by).click()

    def search_book(self, isbn):
        self.driver.find_element(*self.search_button_by).click()
        time.sleep(1)
        self.driver.find_element(*self.search_modal_isbn_input_by).send_keys(isbn)
        time.sleep(1)
        self.driver.find_element(*self.search_modal_search_button_by).click()
        time.sleep(2)
        try:
            self.driver.find_element(By.XPATH, '//*[text()=\'The book does not exist on database\']')
        except NoSuchElementException:
            pass
        else:
            raise BookDoesNotExist(isbn)
        book_data_container = self.driver.find_element(*self.search_modal_book_data_container_by)
        book_data_elements = book_data_container.find_elements(By.TAG_NAME, 'p')
        return dict(
            name=book_data_elements[0].text,
            author=book_data_elements[1].text,
            num_pages=int(book_data_elements[2].text),
            num_copies=int(book_data_elements[3].text)
        )

    def __get_registered_book_elements(self):
        return self.driver.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')

    def get_registered_books(self):
        books = []

        for element in self.__get_registered_book_elements():
            book_data_elements = element.find_elements(By.TAG_NAME, 'td')
            books.append(dict(
                isbn=book_data_elements[0].text,
                name=book_data_elements[1].text,
                author=book_data_elements[2].text,
                num_pages=int(book_data_elements[3].text),
                num_copies=int(book_data_elements[4].text)
            ))

        return books

    def is_book_on_table(self, isbn):
        return any(book for book in self.get_registered_books() if book['isbn'] == isbn)

    def edit_book(self, isbn, name, author, num_pages, num_copies):
        for element in self.__get_registered_book_elements():
            if element.find_elements(By.TAG_NAME, 'td')[0].text == isbn:
                element.find_elements(By.TAG_NAME, 'td')[5].find_element(By.XPATH, "//*[text()='Edit']").click()
                time.sleep(1)
                self.driver.find_element(*self.name_input_by).clear()
                self.driver.find_element(*self.name_input_by).send_keys(name)
                time.sleep(1)
                self.driver.find_element(*self.author_input_by).clear()
                self.driver.find_element(*self.author_input_by).send_keys(author)
                time.sleep(1)
                self.driver.find_element(*self.num_pages_input_by).clear()
                self.driver.find_element(*self.num_pages_input_by).send_keys(num_pages)
                time.sleep(1)
                self.driver.find_element(*self.num_copies_input_by).clear()
                self.driver.find_element(*self.num_copies_input_by).send_keys(num_copies)
                time.sleep(5)
                self.driver.find_element(*self.save_button_by).click()

    def delete_book(self, isbn):
        for element in self.__get_registered_book_elements():
            if element.find_elements(By.TAG_NAME, 'td')[0].text == isbn:
                element.find_elements(By.TAG_NAME, 'td')[5].find_element(By.XPATH, "//*[text()='Delete']").click()
                return True

        return False
