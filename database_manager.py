import sqlite3
import os
from book import Book

class Library:
    """
    A class representing personal library. SQLite is used to store and manage book data.

    Constructor automatically creates (if it doesn't already exist):
     - 'assets' directory.
     - 'my_library.db' file in the 'assets' directory.
     - 'books' table in the 'my_library.db' file.

    'books' table schema:
     - title TEXT NOT NULL
     - author TEXT
     - description TEXT
     - notes TEXT
     - is_read TEXT
     - current_page INTEGER
     - rating INTEGER
     - is_lent TEXT
     - location TEXT
     - isbn INTEGER PRIMARY KEY
    """
    def __init__(self):
        # check if 'assets' directory exists and create one if it doesn't.
        if not os.path.exists('assets'):
            os.mkdir('assets')

        # check if 'my_library.db' file exists and create one if it doesn't.
        self.connection = sqlite3.connect('assets/my_library.db')
        self.cursor = self.connection.cursor()
        self.tables = self.cursor.execute('SELECT name FROM sqlite_master')

        # check if 'books' table exist and create one if it doesn't.
        if self.tables.fetchone() is None:
            self.cursor.execute('''
            CREATE TABLE books(
                title TEXT NOT NULL, 
                author TEXT,
                description TEXT,
                notes TEXT,
                is_read TEXT,
                current_page INTEGER,
                rating INTEGER,
                is_lent TEXT,
                location TEXT,
                isbn INTEGER PRIMARY KEY
            )''')

    def all_books(self, sort: str ='title') -> list:
        """
        Return a list of all book in the library.

        :param sort: String. Search is sorted by the 'sort' attribute. By default, set to 'title'.
        :return: a list of Book objects. If no match found, returns an empty list.
        """
        # when sorting by rating, return result in descending order to have higher rated books on the top
        if sort == 'rating':
            query_result = self.cursor.execute(f'SELECT * FROM books WHERE rating IS NOT "" ORDER BY {sort} DESC').fetchall()
        else:
            query_result = self.cursor.execute(f'SELECT * FROM books ORDER BY {sort}').fetchall()
        return self.__make_book__(query_result)

    def add_book(self, book: Book) -> Book | str:
        """
        Add a book to the library.

        :param book: a Book object.
        :return: a book object and a human-readable representation of the Book object.
        """
        # Use Book object to fill the columns in the book's row.
        # The order of inserting the elements must exactly match the order in the 'books' table schema.
        # If database already has a book with this ISBN, do nothing.
        try:
            self.cursor.execute(f'''INSERT INTO books VALUES (
                "{book.title}", 
                "{book.author}",
                "{book.description}",
                "{book.notes}",
                "{book.is_read}",
                "{book.current_page}",
                "{book.rating}",
                "{book.is_lent}",
                "{book.location}",
                "{book.isbn}"
            )''')
            self.connection.commit()
            return book
        except sqlite3.IntegrityError as error:
            if error.args == ('UNIQUE constraint failed: books.isbn',):
                pass

    def find_book(self, criteria: tuple) -> list:
        """
        Find a book in the database by criteria.

        :param criteria: Tuple - (attribute to search: str, value: str).
        :return: a list of Book objects. If no match found, returns an empty list.
        """
        # Search books that are/aren't lent by checking if 'is_lent' column has a borrower's name.
        # When searching by other criteria, perform pattern matching in the respective column.
        if criteria == ('is_lent', 'is_lent_yes'):
            query_result = self.cursor.execute(f'SELECT * FROM books WHERE {criteria[0]} IS NOT ""').fetchall()
        elif criteria == ('is_lent', 'is_lent_no'):
            query_result = self.cursor.execute(f'SELECT * FROM books WHERE {criteria[0]} = ""').fetchall()
        else:
            query_result = self.cursor.execute(f'SELECT * FROM books WHERE {criteria[0]} LIKE "%{criteria[1]}%"').fetchall()
        return self.__make_book__(query_result)

    def update_book(self, isbn: str, attribute: tuple) -> int:
        """
        Find a book in the database by ISBN and update an attribute.

        :param isbn: String - book ISBN.
        :param attribute: Tuple - (attribute to update: str, new value: str).
        :return: Integer - number of updated rows in the database.
        """
        result = self.cursor.execute(f'UPDATE books SET {attribute[0]}="{attribute[1]}" WHERE isbn={isbn}').rowcount
        self.connection.commit()
        return result

    def delete_book(self, isbn: str) -> int | None:
        """
        Find a book in the database by ISBN and delete it from the library.

        :param isbn: String - book ISBN.
        :return: Integer - number of deleted rows in the database. Return None if no ISBN was entered.
        """
        # If no ISBN provided (isbn is an empty string) - do nothing, return nothing.
        if isbn != '':
            result = self.cursor.execute(f'DELETE FROM books WHERE isbn={isbn}').rowcount
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
        # Create books object from the query result and append them to a list.
        # The order of the book attributes below must exactly match 'books' table schema.
        result = []
        for item in query_result:
            book = Book(
                title=item[0],
                author=item[1],
                description=item[2],
                notes=item[3],
                is_read=item[4],
                current_page=item[5],
                rating=item[6],
                is_lent=item[7],
                location=item[8],
                isbn=item[9])
            result.append(book)
        return result
