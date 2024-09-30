class Book:
    """
    A class to represent a book. If non-required attributes are not set, they default to an empty string.
    All params must be of string type.

    :param title: Title of the book, required attribute.
    :param isbn: Book's ISBN, required attribute.
    :param author: Author of the book, optional.
    :param description: Description of the book, optional.
    :param is_read: True if the has been read, optional, by default sets to False.
    :param current_page: Currently reading at this page, optional.
    :param rating: Personal rating of the book, optional.
    :param notes: Personal notes, optional.
    :param is_lent: The name of the person who borrowed the book, optional.
    :param location: Book's location at home, optional.
    """
    def __init__(self, title: str, isbn: str, author='', description='', is_read='', current_page='', rating='', notes='', is_lent='', location=''):
        self.title = title
        self.author = author
        self.description = description
        self.notes = notes
        self.is_read = is_read
        self.current_page = current_page
        self.rating = rating
        self.is_lent = is_lent
        self.location = location
        self.isbn = isbn

    def get_all_info(self) -> dict:
        """
        Return all information about a book from the database.
        Includes column name (str), user-friendly name of the column (str), column content (str).

        :return: dictionary {'column name': ('user-friendly name', 'content')}
        """
        return {'title': ('Book title', self.title),
                'author': ('Author\'s name', self.author),
                'description': ('Book description', self.description),
                'notes': ('My notes', self.notes),
                'is_read': ('Has the book been read?', "Yes" if self.is_read == 'True' else "Not yet"),
                'current_page': ('Currently at page', self.current_page),
                'rating': ('My rating', self.rating),
                'is_lent': ('Book is lent to', self.is_lent),
                'location': ('Location at home', self.location),
                'isbn': ('ISBN', self.isbn)}

    def __str__(self):
        """
        Return human-readable representation of a Book object in string format.

        :return: string - {"Book title"} by {Author's name}
        """
        if self.author != '':
            return f'"{self.title}" by {self.author}'
        else:
            return self.title
