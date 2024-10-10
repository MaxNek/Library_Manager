import sqlite3
import os
from source.book import Book, BookTemplate

ASSETS_DIR = './assets'
DB_FILE = 'my_library.db'

class Library:
    """
    A class representing personal library. SQLite is used to store and manage book data.

    Constructor automatically creates (if it doesn't already exist):
     - 'assets' directory.
     - 'my_library.db' file in the 'assets' directory.
     - 'books' table in the 'my_library.db' file.
    """
    def __init__(self):
        if not os.path.exists(ASSETS_DIR):
            os.mkdir(ASSETS_DIR)

        self.connection = sqlite3.connect(f'{ASSETS_DIR}/{DB_FILE}')
        self.cursor = self.connection.cursor()
        self.tables = self.cursor.execute('SELECT name FROM sqlite_master')

        self.template = BookTemplate().get_template_data()

        if self.tables.fetchone() is None:
            columns = ''
            for key, value in self.template.items():
                if key == 'title':
                    column = f'{key} {value["type"]} NOT NULL'
                elif key == 'isbn':
                    column = f'{key} {value["type"]} PRIMARY KEY'
                else:
                    column = f'{key} {value["type"]}'
                columns = columns + f'{column},'
            columns = columns[:-1]
            # TODO: use placeholder here?
            query = f'CREATE TABLE books({columns})'
            self.cursor.execute(query)

    def all_books(self, sort: str ='title') -> list:
        """
        Return a list of all book in the library.

        :param sort: String. Search is sorted by the 'sort' attribute. By default, set to 'title'.
        :return: a list of Book objects. If no match found, returns an empty list.
        """
        sort_by = 'title'
        for key, value in self.template.items():
            if value['name'] == sort:
                sort_by = key
        if sort_by == 'rating':
            query = f'SELECT * FROM books WHERE rating IS NOT "" ORDER BY {sort_by} DESC'
        else:
            query = f'SELECT * FROM books ORDER BY {sort_by}'
        query_result = self.cursor.execute(query).fetchall()
        return self.__make_book__(query_result)

    def add_book(self, new_book: Book) -> Book | str:
        """
        Add a book to the library.

        :param new_book: a Book object.
        :return: a book object and a human-readable representation of the Book object.
        """
        book = new_book.get_all_info()
        try:
            columns = ''
            for key in book:
                columns = columns + f':{key},'
            columns = columns[:-1]
            query = f'INSERT INTO books VALUES ({columns})'
            data_dict = {}
            for key, value in book.items():
                data_dict[key] = book[key][1]
            data = (data_dict,)
            self.cursor.executemany(query, data)
            self.connection.commit()
            return new_book
        except sqlite3.IntegrityError as error:
            if error.args == ('UNIQUE constraint failed: books.isbn',):
                pass

    def find_book(self, criteria: tuple) -> list:
        """
        Find a book in the database by criteria.

        :param criteria: Tuple - (attribute to search: str, value: str).
        :return: a list of Book objects. If no match found, returns an empty list.
        """
        if criteria == ('is_lent', 'is_lent_yes'):
            prompt = 'SELECT * FROM books WHERE is_lent IS NOT ""'
            query_result = self.cursor.execute(prompt).fetchall()
        elif criteria == ('is_lent', 'is_lent_no'):
            prompt = 'SELECT * FROM books WHERE is_lent = ""'
            query_result = self.cursor.execute(prompt).fetchall()
        elif criteria[0] == 'isbn_to_delete':
            query = f'SELECT * FROM books WHERE isbn = ?'
            params = (criteria[1],)
            query_result = self.cursor.execute(query, params).fetchall()
        else:
            query = f'SELECT * FROM books WHERE {criteria[0]} LIKE ?'
            params = (f'%{criteria[1]}%',)
            query_result = self.cursor.execute(query, params).fetchall()
        return self.__make_book__(query_result)

    def update_book(self, isbn: str, attribute: tuple) -> int:
        """
        Find a book in the database by ISBN and update an attribute.

        :param isbn: String - book ISBN.
        :param attribute: Tuple - (attribute to update: str, new value: str).
        :return: Integer - number of updated rows in the database.
        """
        data = {
            'isbn': isbn,
            'attribute': attribute[0],
            'content': attribute[1]
        }
        query = f'UPDATE books SET {attribute[0]}=:content WHERE isbn=:isbn'
        result = self.cursor.execute(query, data).rowcount
        self.connection.commit()
        return result

    def delete_book(self, isbn: str) -> int | None:
        """
        Find a book in the database by ISBN and delete it from the library.

        :param isbn: String - book ISBN.
        :return: Integer - number of deleted rows in the database. Return None if no ISBN was entered.
        """
        if isbn != '':
            query = 'DELETE FROM books WHERE isbn = ?'
            params = (f'{isbn}',)
            result = self.cursor.execute(query, params).rowcount
            self.connection.commit()
            return result
        else:
            return None

    def __make_book__(self, query_result: list) -> list:
        """
        Create a Book object.

        :param query_result: List - result of a query in the Library.
        :return: List - a list of Book objects.
        """
        result = []
        for item in query_result:
            kwargs = {}
            i = 0
            for key in self.template:
                kwargs[key] = item[i]
                i += 1
            book = Book(**kwargs)
            result.append(book)
        return result
