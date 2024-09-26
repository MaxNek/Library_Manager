import tkinter
from database_manager import Library
from book import Book
from tkinter import *
import tkinter.ttk

# GUI Settings
MAIN_BACKGROUND_COLOR = 'light steel blue'
MAIN_WINDOW_PADDING = 15

WIDGET_FRAME_COLOR = 'grey'
WIDGET_NAME_FONT = ('Helvetica', 10, 'bold')
WIDGET_FRAME_BORDER = 0
WIDGET_PADDING = 5
WIDGET_MARGIN = 10

BUTTON_PADDING = 2
BUTTON_WIDTH = 14

ENTRY_WIDTH = 23
ENTRY_PADDING = 1

OUTPUT_WIDTH = 108
OUTPUT_HEIGHT = 15

BOOK_WINDOW_FRAME_PADDING = 5
BOOK_WINDOW_TEXT_FONT = ('Arial', 10, 'normal')
BOOK_WINDOW_TEXT_BG_COLOR = 'white'

class GuiApp(Tk):
    def __init__(self, library: Library):
        super().__init__()
        # Connect to a library
        self.library = library

        # Create main gui window
        self.title('My Personal Library')
        self.config(bg=MAIN_BACKGROUND_COLOR, padx=MAIN_WINDOW_PADDING, pady=MAIN_WINDOW_PADDING)

        # Add widgets
        self.__view_all_widget__()
        self.__output_widget__()
        self.__add_book_widget__()
        self.__find_book_widget__()
        self.__update_book_widget__()
        self.__delete_book_widget__()

        self.list_of_books = []

        # Add 'Quit' button
        self.quit_button = Button(text='Quit', width=BUTTON_WIDTH, command=self.destroy)
        self.quit_button.grid(column=0, row=3, pady=BUTTON_PADDING)

#----------------------------- Widgets -----------------------------#
    def __view_all_widget__(self):
        # Create widget frame
        frame = self.__make_frame__(column=0, row=0, widget_name='Show all books')

        #TODO: 'View All widget' - Add sorting by rating

        # Create 'Sort by' dropdown
        sort_label = Label(frame, text='Sort by:', bg=MAIN_BACKGROUND_COLOR)
        sort_label.grid(column=0, row=1)
        self.sort_by = tkinter.ttk.Combobox(frame, state="readonly", values=['title', 'author'])
        self.sort_by.set('title')
        self.sort_by.grid(column=0, row=2)

        # Create 'Show' button
        button = Button(frame, text='Show', width=BUTTON_WIDTH, command=self.__display_all__)
        button.grid(column=0, row=3, pady=BUTTON_PADDING)

    def __add_book_widget__(self):
        # Create widget frame
        frame = self.__make_frame__(column=2, row=0, rowspan=2, widget_name='Add a book')

        # Create entry forms
        self.add_book_entries = []
        title_label = Label(frame, text='Book title', bg=MAIN_BACKGROUND_COLOR)
        title_label.grid(column=0, row=1)
        self.title_entry = Entry(frame, width=ENTRY_WIDTH)
        self.title_entry.grid(column=0, row=2, padx=ENTRY_PADDING)
        self.add_book_entries.append(self.title_entry)

        author_label = Label(frame, text='Author\'s name', bg=MAIN_BACKGROUND_COLOR)
        author_label.grid(column=0, row=3)
        self.author_entry = Entry(frame, width=ENTRY_WIDTH)
        self.author_entry.grid(column=0, row=4, padx=ENTRY_PADDING)
        self.add_book_entries.append(self.author_entry)

        descr_label = Label(frame, text='Description', bg=MAIN_BACKGROUND_COLOR)
        descr_label.grid(column=0, row=5)
        self.descr_entry = Entry(frame, width=ENTRY_WIDTH)
        self.descr_entry.grid(column=0, row=6, padx=ENTRY_PADDING)
        self.add_book_entries.append(self.descr_entry)

        is_read_label = Label(frame, text='Has been read?', bg=MAIN_BACKGROUND_COLOR)
        is_read_label.grid(column=0, row=7)
        self.is_read_entry = tkinter.ttk.Combobox(frame, state="readonly", values=['Yes', 'Not yet'])
        self.is_read_entry.grid(column=0, row=8, padx=ENTRY_PADDING)
        self.add_book_entries.append(self.is_read_entry)

        current_page_label = Label(frame, text='Currently at page', bg=MAIN_BACKGROUND_COLOR)
        current_page_label.grid(column=0, row=9)
        self.current_page_entry = Entry(frame, width=ENTRY_WIDTH)
        self.current_page_entry.grid(column=0, row=10, padx=ENTRY_PADDING)
        self.add_book_entries.append(self.current_page_entry)

        rating_label = Label(frame, text='My rating', bg=MAIN_BACKGROUND_COLOR)
        rating_label.grid(column=1, row=1)
        self.rating_entry = tkinter.ttk.Combobox(frame, state="readonly", values=[str(score) for score in range(1, 11)])
        self.rating_entry.grid(column=1, row=2, padx=ENTRY_PADDING)
        self.add_book_entries.append(self.rating_entry)

        notes_label = Label(frame, text='My notes', bg=MAIN_BACKGROUND_COLOR)
        notes_label.grid(column=1, row=3)
        self.notes_entry = Entry(frame, width=ENTRY_WIDTH)
        self.notes_entry.grid(column=1, row=4, padx=ENTRY_PADDING)
        self.add_book_entries.append(self.notes_entry)

        is_lent_label = Label(frame, text='Book is lent to', bg=MAIN_BACKGROUND_COLOR)
        is_lent_label.grid(column=1, row=5)
        self.is_lent_entry = Entry(frame, width=ENTRY_WIDTH)
        self.is_lent_entry.grid(column=1, row=6, padx=ENTRY_PADDING)
        self.add_book_entries.append(self.is_lent_entry)

        location_label = Label(frame, text='Location at home', bg=MAIN_BACKGROUND_COLOR)
        location_label.grid(column=1, row=7)
        self.location_entry = tkinter.ttk.Combobox(frame, state="readonly", values=['living room', 'bedroom'])
        self.location_entry.grid(column=1, row=8, padx=ENTRY_PADDING)
        self.add_book_entries.append(self.location_entry)

        isbn_label = Label(frame, text='ISBN', bg=MAIN_BACKGROUND_COLOR)
        isbn_label.grid(column=1, row=9)
        self.isbn_entry = Entry(frame, width=ENTRY_WIDTH)
        self.isbn_entry.grid(column=1, row=10, padx=ENTRY_PADDING)
        self.add_book_entries.append(self.isbn_entry)

        # Create 'Add' button
        button = Button(frame, text='Add', width=BUTTON_WIDTH, command=self.__add_book__)
        button.grid(column=0, row=21, columnspan=2, pady=BUTTON_PADDING)


    def __find_book_widget__(self):
        # Create widget frame
        frame = self.__make_frame__(column=0, row=1, widget_name='Find books')

        # TODO: make 'Find book widget' dropdown human readable

        # Create 'Search by' dropdown
        search_by_label = Label(frame, text='Search by:', bg=MAIN_BACKGROUND_COLOR)
        search_by_label.grid(column=0, row=1)
        self.search_by = tkinter.ttk.Combobox(frame, state="readonly", values=['title', 'author', 'is_read', 'rating',
                                                                               'notes', 'is_lent', 'location', 'isbn'])
        self.search_by.set('title')
        self.search_by.grid(column=0, row=2)

        # Create entry field
        self.search_by_entry = Entry(frame, width=ENTRY_WIDTH)
        self.search_by_entry.grid(column=0, row=3, pady=ENTRY_PADDING)

        # Create 'Show' button
        button = Button(frame, text='Find', width=BUTTON_WIDTH, command=self.__find_book__)
        button.grid(column=0, row=4, pady=BUTTON_PADDING)

    def __update_book_widget__(self):
        # Create widget frame
        frame = self.__make_frame__(column=1, row=0, rowspan=2, widget_name='Update book')

        # TODO: make 'Update book widget' dropdown human readable

        # Create entry forms
        self.update_book_entries = []
        isbn_to_update = Label(frame, text='ISBN', bg=MAIN_BACKGROUND_COLOR)
        isbn_to_update.grid(column=0, row=1)
        self.isbn_to_update_entry = Entry(frame, width=ENTRY_WIDTH)
        self.isbn_to_update_entry.grid(column=0, row=2, padx=ENTRY_PADDING)
        self.update_book_entries.append(self.isbn_to_update_entry)

        update_field_label = Label(frame, text='Update', bg=MAIN_BACKGROUND_COLOR)
        update_field_label.grid(column=0, row=3)
        self.update_field_entry = tkinter.ttk.Combobox(frame, state="readonly", values=['title', 'author', 'is_read', 'rating',
                                                                               'notes', 'is_lent', 'location', 'isbn'])
        self.update_field_entry.grid(column=0, row=4, padx=ENTRY_PADDING)
        self.update_book_entries.append(self.update_field_entry)

        update_to_label = Label(frame, text='To', bg=MAIN_BACKGROUND_COLOR)
        update_to_label.grid(column=0, row=5)
        self.update_to_entry = Entry(frame, width=ENTRY_WIDTH)
        self.update_to_entry.grid(column=0, row=6, padx=ENTRY_PADDING)
        self.update_book_entries.append(self.update_to_entry)

        # Create 'Update' button
        button = Button(frame, text='Update', width=BUTTON_WIDTH, command=self.__update_book__)
        button.grid(column=0, row=7, pady=BUTTON_PADDING)

    def __delete_book_widget__(self):
        # Create widget frame
        frame = self.__make_frame__(column=1, row=3, columnspan=2, widget_name='Delete book by ISBN:')

        # Create search entry
        self.isbn_to_delete = Entry(frame, width=ENTRY_WIDTH)
        self.isbn_to_delete.grid(column=2, row=0, padx=ENTRY_PADDING)

        # Create 'Delete' button
        button = Button(frame, text='Delete', width=BUTTON_WIDTH, command=self.__delete_book__)
        button.grid(column=3, row=0, padx=BUTTON_PADDING)

    def __output_widget__(self):
        # Create a scrollbar
        self.scrollbar = Scrollbar(self)
        self.scrollbar.grid(column=3, row=2)

        # Create an output screen
        self.output = Listbox(width=OUTPUT_WIDTH, height=OUTPUT_HEIGHT, yscrollcommand=self.scrollbar.set)
        self.output.grid(column=0, row=2, columnspan=3, padx=WIDGET_PADDING, pady=WIDGET_PADDING)
        self.output.bind('<Double-1>', self.__click__)

        # Attach the scrollbar to the output screen
        self.scrollbar.config(command=self.output.yview)

# ----------------------------- Widget button functionality -----------------------------#

    def __click__(self, event):
        selection = self.output.curselection()
        book = self.list_of_books[selection[0]]
        window = Toplevel(bg=MAIN_BACKGROUND_COLOR, padx=MAIN_WINDOW_PADDING, pady=MAIN_WINDOW_PADDING)
        window.title('Book Details')
        row = 0
        right_row = 4
        left_row = 4
        for attribute, content in book.get_all_info().items():
            frame = LabelFrame(master=window,
                               text=f'{content[0]}',
                               highlightbackground=WIDGET_FRAME_COLOR,
                               highlightthickness=WIDGET_FRAME_BORDER,
                               bg=MAIN_BACKGROUND_COLOR,
                               bd=0)
            text_width = 20
            if attribute in ['title', 'author', 'description', 'notes']:
                frame.grid(column=0, row=row, columnspan=2)
                text_width = 70
            elif attribute in ['is_read', 'current_page', 'rating']:
                frame.grid(column=0, row=right_row)
                right_row += 1
            else:
                frame.grid(column=1, row=left_row)
                left_row += 1
            if attribute == 'description':
                cont_text = Text(frame, bg=BOOK_WINDOW_TEXT_BG_COLOR, height=15, wrap='word', font=BOOK_WINDOW_TEXT_FONT)
            elif attribute == 'notes':
                cont_text = Text(frame, bg=BOOK_WINDOW_TEXT_BG_COLOR, height=2, wrap='word', font=BOOK_WINDOW_TEXT_FONT)
            else:
                cont_text = Text(frame, bg=BOOK_WINDOW_TEXT_BG_COLOR, height=1,  wrap='word', font=BOOK_WINDOW_TEXT_FONT)
            cont_text.insert(tkinter.END, f'{content[1]}')
            cont_text.config(state='disabled', width=text_width)
            cont_text.grid(column=0, row=0, pady=BOOK_WINDOW_FRAME_PADDING )
            row += 1
        window.mainloop()

    def __display_all__(self):
        self.list_of_books.clear()
        self.output.delete(first=0, last=END)
        sort = self.sort_by.get()
        all_books = self.library.all_books(sort=sort)
        for book in all_books:
            self.output.insert(END, book)
            self.list_of_books.append(book)

    def __add_book__(self):
        self.output.delete(first=0, last=END)
        if self.is_read_entry.get() == 'Yes':
            is_read = True
        else:
            is_read = False
        new_book = Book(
            title=self.title_entry.get().title(),
            author=self.author_entry.get().title(),
            description=self.descr_entry.get(),
            is_read=is_read,
            current_page=self.current_page_entry.get(),
            rating=self.rating_entry.get(),
            notes=self.notes_entry.get(),
            is_lent=self.is_lent_entry.get().title(),
            location=self.location_entry.get(),
            isbn=self.isbn_entry.get())
        result = self.library.add_book(new_book)
        if result:
            self.output.insert(END, f'{new_book} {result}')
        for entry in self.add_book_entries:
            if type(entry) == tkinter.ttk.Combobox:
                entry.set('')
            else:
                entry.delete(first=0, last=END)

    def __find_book__(self):
        self.output.delete(first=0, last=END)
        if self.search_by.get() != '':
            attribute = self.search_by.get()
            prompt = self.search_by_entry.get()
            criteria = (attribute, prompt)
            result = self.library.find_book(criteria=criteria)
            for book in result:
                self.output.insert(END, book)
            self.search_by.set('')
            self.search_by_entry.delete(first=0, last=END)

    def __update_book__(self):
        self.output.delete(first=0, last=END)
        isbn = self.isbn_to_update_entry.get()
        field = self.update_field_entry.get()
        new_value = self.update_to_entry.get()
        if field != '':
            result = self.library.update_book(isbn=isbn, attribute=(field, new_value))
            self.output.insert(END, result)
        for entry in self.update_book_entries:
            if type(entry) == tkinter.ttk.Combobox:
                entry.set('')
            else:
                entry.delete(first=0, last=END)

    def __delete_book__(self):
        self.output.delete(first=0, last=END)
        isbn = self.isbn_to_delete.get()
        result = self.library.delete_book(isbn=isbn)
        self.output.insert(END, result)
        self.isbn_to_delete.delete(first=0, last=END)

# ----------------------------- Class utilities -----------------------------#

    def __make_frame__(self, column=0, row=0, columnspan=1, rowspan=1, widget_name='Widget name'):
        # Create widget frame
        frame = LabelFrame(self,
                           text=widget_name,
                           highlightbackground=WIDGET_FRAME_COLOR,
                           highlightthickness=WIDGET_FRAME_BORDER,
                           padx=WIDGET_PADDING,
                           pady=WIDGET_PADDING,
                           bg=MAIN_BACKGROUND_COLOR)
        frame.grid(column=column, row=row, columnspan=columnspan, rowspan=rowspan, padx=WIDGET_MARGIN)
        return frame
