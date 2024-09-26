class Book:
    """
    A class to represent a book. If non-required attributes are not set, they default to an empty string.

    Attributes:
        title (str): Title of the book, required attribute
        isbn (str): Book's ISBN, required attribute
        author (str): Author of the book
        description (str): Description of the book
        is_read (str): If the book has been read 'is_read' is True
        current_page (str): Currently reading at this page
        rating (str): Personal rating of the book
        notes (str): Personal notes
        is_lent (str): The name of the person who borrowed the book
        location (str): Book's location at home
    """
    def __init__(self, title, isbn, author='', description='', is_read='', current_page='', rating='', notes='', is_lent='', location=''):
        self.title = title
        self.author = author
        self.description = description
        self.is_read = is_read
        self.current_page = current_page
        self.rating = rating
        self.notes = notes
        self.is_lent = is_lent
        self.location = location
        self.isbn = isbn

    def get_all_info(self) -> dict:
        return {'title': ('Book title', self.title),
                'author': ('Author\'s name', self.author),
                'description': ('Book description', self.description),
                'notes': ('My notes', self.notes),
                'is_read': ('Has the book been read?', "Yes" if self.is_read else "Not yet"),
                'current_page': ('Currently at page', self.current_page),
                'rating': ('My rating', self.rating),
                'is_lent': ('Book is lent to', self.is_lent),
                'location': ('Location at home', self.location),
                'isbn': ('ISBN', self.isbn)}

    def __str__(self):
        return f'"{self.title}" by {self.author}'

