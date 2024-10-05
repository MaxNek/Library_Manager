from source.config import AppConfig

class BookTemplate:
    """
    A class to define what book information is stored in the database,
    Book object attributes and their user-friendly representations.
    """
    def __init__(self):
        self.config = AppConfig()
        book_locations = self.config.get_book_locations()
        book_rating = self.config.get_rating_scale()

        self.data = {
            'title': {
                'name': 'Book title',
                'type': 'TEXT',
                'sort_all_by': True,
                'search_by': True,
                'selectable': False,
                'width': 2},
            'author': {
                'name': 'Author\'s name',
                'type': 'TEXT',
                'sort_all_by': True,
                'search_by': True,
                'selectable': False,
                'width': 2},
            'description': {
                'name': 'Book description',
                'type': 'TEXT',
                'sort_all_by': False,
                'search_by': True,
                'selectable': False,
                'width': 2},
            'notes': {
                'name': 'My notes',
                'type': 'TEXT',
                'sort_all_by': False,
                'search_by': True,
                'selectable': False,
                'width': 2},
            'is_read': {
                'name': 'Has been read?',
                'type': 'TEXT',
                'sort_all_by': False,
                'search_by': True,
                'selectable': True,
                'options': ['Yes', 'Not yet'],
                'def_state': 'readonly',
                'width': 1},
            'current_page': {
                'name': 'Currently at page',
                'type': 'INTEGER',
                'sort_all_by': False,
                'search_by': False,
                'selectable': False,
                'width': 1},
            'rating': {
                'name': 'My rating',
                'type': 'REAL',
                'sort_all_by': True,
                'search_by': True,
                'selectable': True,
                'options': book_rating,
                'def_state': 'readonly',
                'width': 1},
            'is_lent': {
                'name': 'Book is lent to',
                'type': 'TEXT',
                'sort_all_by': False,
                'search_by': True,
                'selectable': False,
                'width': 1},
            'location': {
                'name': 'Location at home',
                'type': 'TEXT',
                'sort_all_by': False,
                'search_by': True,
                'selectable': True,
                'options': book_locations,
                'def_state': 'normal',
                'width': 1},
            'isbn': {
                'name': 'ISBN',
                'type': 'TEXT',
                'sort_all_by': False,
                'search_by': True,
                'selectable': False,
                'width': 1}
        }

    def get_template_data(self) -> dict:
        """
        Return the entire book template.

        :return: Dictionary
        """
        return self.data

class Book:
    """
    A class to represent a book. If attributes are not set, they default to an empty string.

    - title: Title of the book.
    - isbn: Book's ISBN.
    - author: Author of the book.
    - description: Description of the book.
    - is_read: True if the has been read.
    - current_page: Currently reading at this page.
    - rating: Personal rating of the book.
    - notes: Personal notes.
    - is_lent: The name of the person who borrowed the book.
    - location: Book's location at home.
    """
    def __init__(self, **kwargs):
        self.template = BookTemplate().get_template_data()
        self.book_info = {}
        for key in self.template:
            if key in kwargs:
                self.book_info[key] = kwargs[key]
            else:
                self.book_info[key] = ''

    def get_all_info(self) -> dict:
        """
        Return all information about a book from the database.
        Includes column name (str), user-friendly name of the column (str), column content (str).

        :return: dictionary {'column name': ('user-friendly name', 'content')}
        """
        all_info = {}
        for key, value in self.template.items():
            all_info[key] = (value, self.book_info[key])

        return all_info

    def get_this_info(self, attribute):
        """
        Return book's 'attribute' content.

        :param attribute: String - book's attribute
        :return:  String - value stored in the Book object ufor the 'attribute'
        """
        return self.book_info[attribute]

    def __str__(self):
        """
        Return human-readable representation of a Book object in string format.

        :return: string - {"Book title"} by {Author's name}
        """
        if self.book_info['author'] != '':
            return f'"{self.book_info['title']}" by {self.book_info['author']}'
        else:
            return f'"{self.book_info['title']}"'
