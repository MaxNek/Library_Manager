import sqlite3
from book import Book

class Library:
    """
    A class representing personal library. SQLite is used to store and manage book data.
    """
    def __init__(self):
        self.connection = sqlite3.connect("my_library.db")
        self.cursor = self.connection.cursor()
        self.tables = self.cursor.execute('SELECT name FROM sqlite_master')
        if self.tables.fetchone() is None:
            self.cursor.execute('''
            CREATE TABLE books(
                title TEXT NOT NULL, 
                author TEXT,
                description TEXT,
                is_read TEXT,
                current_page INTEGER,
                rating REAL,
                notes TEXT,
                is_lent TEXT,
                location TEXT,
                isbn INTEGER PRIMARY KEY
            )''')

    def all_books(self, sort='title') -> list:
        """
        Return a list of all book in the library
        Args:
            sort (str): search is sorted by 'sort' attribute
        Returns:
            result (list): a list of Book objects. If no match found, returns an empty list
        """
        query_result = self.cursor.execute(f'SELECT * FROM books ORDER BY {sort}').fetchall()
        return self.__make_book__(query_result)

    def add_book(self, book: Book) -> str:
        """
        Add a book in the library
        Args:
            book (Book): a Book object
        Returns:
            (str): message that a book was added to the library or if the book was already in the library
        """
        try:
            self.cursor.execute(f'''INSERT INTO books VALUES (
                "{book.title}", 
                "{book.author}",
                "{book.description}",
                "{book.is_read}",
                "{book.current_page}",
                "{book.rating}",
                "{book.notes}",
                "{book.is_lent}",
                "{book.location}",
                "{book.isbn}"
            )''')
            self.connection.commit()
            return 'Book has been successfully added'
        except sqlite3.IntegrityError as error:
            if error.args == ('UNIQUE constraint failed: books.isbn',):
                return 'already in the library'

    # TODO: Consider making flexible search %%

    def find_book(self, criteria: tuple) -> list:
        """
        Locate a book by criteria
        Args:
            criteria (tuple): (attribute to search: str, value: str)
        Returns:
            result (list): a list of Book objects. If no match found, returns an empty list
        """
        query_result = self.cursor.execute(f'SELECT * FROM books WHERE {criteria[0]} = "{criteria[1]}"').fetchall()
        return self.__make_book__(query_result)

    def update_book(self, isbn, attribute: tuple) -> int:
        """
        Locate a book by ISBN and update an attribute
        Args:
            isbn (str): book ISBN
            attribute (tuple): (attribute to update: str, new value: str)
        Returns:
            (int): number of updated rows
        """
        result = self.cursor.execute(f'UPDATE books SET {attribute[0]}="{attribute[1]}" WHERE isbn={isbn}').rowcount
        self.connection.commit()
        return result

    def delete_book(self, isbn: str):
        """
        Locate a book by ISBN and delete it from the library
        Args:
            isbn (str): book ISBN
        Returns:
            (int, None): number of deleted rows or None
        """
        if isbn != '':
            result = self.cursor.execute(f'DELETE FROM books WHERE isbn={isbn}').rowcount
            self.connection.commit()
            return result
        else:
            return None

    def __make_book__(self, query_result: list) -> list:
        """
        Create a Book object
        Args:
            query_result (list): result of a query in the Library
        Returns:
            result (list): a list of Book objects
        """
        result = []
        for item in query_result:
            book = Book(
                title=item[0],
                author=item[1],
                description=item[2],
                is_read=item[3],
                current_page=item[4],
                rating=item[5],
                notes=item[6],
                is_lent=item[7],
                location=item[8],
                isbn=item[9])
            result.append(book)
        return result
