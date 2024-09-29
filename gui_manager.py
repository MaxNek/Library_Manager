import tkinter
from database_manager import Library
from book import Book
from tkinter import *
from tkinter import messagebox
import tkinter.ttk as ttk


# GUI Settings
MAIN_BACKGROUND_COLOR = 'light steel blue'
MAIN_WINDOW_PADDING = 15

WIDGET_FRAME_COLOR = 'grey'
WIDGET_NAME_FONT = ('Helvetica', 10, 'bold')
WIDGET_FRAME_BORDER = 0
WIDGET_PADDING = 5
WIDGET_MARGIN = 10

BUTTON_PADDING = 5
BUTTON_WIDTH = 14

ENTRY_WIDTH = 23
ENTRY_PADDING = 1

OUTPUT_WIDTH = 80
OUTPUT_HEIGHT = 15

BOOK_WINDOW_FRAME_PADDING = 5
BOOK_WINDOW_TEXT_FONT = ('Arial', 10, 'normal')
BOOK_WINDOW_TEXT_BG_COLOR = 'SlateGray2'
BOOK_WINDOW_TEXT_BG_COLOR_EDIT = 'white'
BOOK_WINDOW_DESCRIPTION_HEIGHT = 15
BOOK_WINDOW_NOTES_HEIGHT = 2

BOOK_RATING_OPTIONS = ['', '1', '2', '3', '4', '5']

ABOUT_WINDOW_COLOR = 'light steel blue'

class GuiApp(Tk):
    def __init__(self, library: Library):
        super().__init__()
        # Connect to a library
        self.library = library

        # Location options
        self.book_location_options = []

        # Create main gui window
        self.title('My Personal Library')
        self.config(bg=MAIN_BACKGROUND_COLOR, padx=MAIN_WINDOW_PADDING, pady=MAIN_WINDOW_PADDING)

        # Add widgets
        self.__view_all_widget__()
        self.__output_widget__()
        self.__add_book_widget__()
        self.__find_book_widget__()
        self.__delete_book_widget__()
        self.__menu__()

        # Combobox styling
        style = ttk.Style()
        style.theme_settings("default",
                             {"TCombobox": {
                                 "map": {
                                     "fieldbackground":[
                                         ("readonly", BOOK_WINDOW_TEXT_BG_COLOR_EDIT),
                                         ("disabled", BOOK_WINDOW_TEXT_BG_COLOR)]}}})
        style.theme_use("default")

        self.list_of_books = []

#----------------------------- Widgets -----------------------------#
    def __view_all_widget__(self):
        # Create widget frame
        frame = self.__make_frame__(column=0, row=0, widget_name='Show all books')

        # Create 'Sort by' dropdown
        sort_options = ['Title', 'Author', 'Rating']
        sort_label = Label(frame, text='Sort by:', bg=MAIN_BACKGROUND_COLOR)
        sort_label.grid(column=0, row=1)
        self.sort_by = tkinter.ttk.Combobox(frame, state="readonly", values=sort_options)
        self.sort_by.set('Title')
        self.sort_by.grid(column=0, row=2)

        # Create 'Show' button
        button = Button(frame, text='Show', width=BUTTON_WIDTH, command=self.__display_all__)
        button.grid(column=0, row=3, pady=BUTTON_PADDING)

    def __add_book_widget__(self):
        # Create widget frame
        frame = self.__make_frame__(column=1, row=0, rowspan=2, widget_name='Add a book')

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
        self.is_read_entry = ttk.Combobox(frame, state="readonly", values=['Yes', 'Not yet'])
        self.is_read_entry.grid(column=0, row=8, padx=ENTRY_PADDING)
        self.add_book_entries.append(self.is_read_entry)

        current_page_label = Label(frame, text='Currently at page', bg=MAIN_BACKGROUND_COLOR)
        current_page_label.grid(column=0, row=9)
        self.current_page_entry = Entry(frame, width=ENTRY_WIDTH)
        self.current_page_entry.grid(column=0, row=10, padx=ENTRY_PADDING)
        self.add_book_entries.append(self.current_page_entry)

        rating_label = Label(frame, text='My rating', bg=MAIN_BACKGROUND_COLOR)
        rating_label.grid(column=1, row=1)
        self.rating_entry = ttk.Combobox(frame, state="readonly", values=BOOK_RATING_OPTIONS)
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
        self.location_entry = ttk.Combobox(frame, state="normal", values=self.book_location_options)
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

        # Create 'Search by' dropdown
        book_search_options = ['Title', 'Author', 'Has been read?', 'Rating', 'In notes', 'In description',
                               'Has been borrowed?', 'Has been lent to', 'Location', 'ISBN']
        search_by_label = Label(frame, text='Search:', bg=MAIN_BACKGROUND_COLOR)
        search_by_label.grid(column=0, row=1)
        self.search_by = tkinter.ttk.Combobox(frame,
                                              state="readonly",
                                              values=book_search_options)
        self.search_by.set('Title')
        self.search_by.grid(column=0, row=2)

        # Create entry field
        self.search_by_entry = Entry(frame, width=ENTRY_WIDTH)
        self.search_by_entry.grid(column=0, row=3, pady=ENTRY_PADDING)

        # Create 'Show' button
        button = Button(frame, text='Find', width=BUTTON_WIDTH, command=self.__find_book__)
        button.grid(column=0, row=4, pady=BUTTON_PADDING)

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
        self.scrollbar.grid(column=2, row=2)

        # Create an output screen
        self.output = Listbox(width=OUTPUT_WIDTH, height=OUTPUT_HEIGHT, yscrollcommand=self.scrollbar.set)
        self.output.grid(column=0, row=2, columnspan=2, padx=WIDGET_PADDING, pady=WIDGET_PADDING)
        self.output.bind('<Double-1>', self.__click__)

        # Attach the scrollbar to the output screen
        self.scrollbar.config(command=self.output.yview)

    # TODO: add 'Menu' option. Include 'About', option to add book location, consider option to modify gui colours

    def __menu__(self):
        top = self.winfo_toplevel()
        self.menuBar = Menu(top)
        top['menu'] = self.menuBar

        self.subMenu = Menu(self.menuBar)
        self.menuBar.add_cascade(label='Menu', menu=self.subMenu)
        self.subMenu.add_command(label='Settings', command=self.__open_settings__)
        self.subMenu.add_command(label='About', command=self.__open_about__)

    # ----------------------------- Widget button functionality -----------------------------#

    def __display_all__(self):
        self.list_of_books.clear()
        self.output.delete(first=0, last=END)
        sort = self.sort_by.get().lower()
        all_books = self.library.all_books(sort=sort)
        for book in all_books:
            sort_option_names = {'title': book.title, 'author': book.author, 'rating': book.rating}
            if sort == 'title':
                self.output.insert(END, f'"{book.title}" by {book.author}')
            elif sort == 'author':
                self.output.insert(END, f'{book.author}, "{book.title}"')
            else:
                self.output.insert(END, f'{sort_option_names[sort]} {book}')
            self.list_of_books.append(book)

    def __add_book__(self):
        self.output.delete(first=0, last=END)
        self.list_of_books.clear()
        if self.isbn_entry.get() != '' and self.title_entry.get().title() != '':
            is_read = True if self.is_read_entry.get() == 'Yes' else False
            is_lent = '' if self.is_lent_entry.get() == '' else self.is_lent_entry.get().title().strip()
            new_book = Book(
                title=self.title_entry.get().title().strip(),
                author=self.author_entry.get().title().strip(),
                description=self.descr_entry.get().replace('"', "'").strip(),
                is_read=is_read,
                current_page=self.current_page_entry.get().strip(),
                rating=self.rating_entry.get(),
                notes=self.notes_entry.get().strip(),
                is_lent=is_lent,
                location=self.location_entry.get(),
                isbn=self.isbn_entry.get().strip())
            result = self.library.add_book(new_book)
            if result:
                self.list_of_books.append(result)
                self.output.insert(END, result, 'has been added to the library')
            else:
                book = self.library.find_book(criteria=('isbn', new_book.isbn.strip()))[0]
                self.list_of_books.append(book)
                self.output.insert(END, book, 'was already in the library')
            for entry in self.add_book_entries:
                if type(entry) == tkinter.ttk.Combobox:
                    entry.set('')
                else:
                    entry.delete(first=0, last=END)
        else:
            self.output.insert(END, 'Book title and ISBN must be entered')

    def __find_book__(self):
        book_search_non_db_options = {'Has been read?': 'is_read',
                                      'In notes': 'notes',
                                      'In description': 'description',
                                      'Has been borrowed?': 'is_lent',
                                      'Has been lent to': 'is_lent'}
        self.list_of_books.clear()
        self.output.delete(first=0, last=END)
        if self.search_by.get() != '' and self.search_by_entry.get() != '':
            entry = self.search_by_entry.get().lower()
            if self.search_by.get() in book_search_non_db_options:
                attribute = book_search_non_db_options[f'{self.search_by.get()}']
                if attribute == 'is_read':
                    prompt = 'True' if entry == 'yes' else 'False'
                elif attribute == 'is_lent' and entry == 'no':
                    prompt = 'is_lent_no'
                elif attribute == 'is_lent' and entry == 'yes':
                    prompt = 'is_lent_yes'
                else:
                    prompt = entry
            else:
                attribute = self.search_by.get()
                prompt = entry
            criteria = (attribute, prompt)
            result = self.library.find_book(criteria=criteria)
            for book in result:
                self.output.insert(END, book)
                self.list_of_books.append(book)
            self.search_by.set('')
            self.search_by_entry.delete(first=0, last=END)

    def __delete_book__(self):
        self.output.delete(first=0, last=END)
        isbn = self.isbn_to_delete.get()
        if isbn != '':
            book_to_delete = self.library.find_book(('isbn', isbn))[0]
            confirm = messagebox.askquestion('Delete book',
                                             f'Are you sure you want to delete {book_to_delete}?',
                                             icon=messagebox.WARNING)
            if confirm == 'yes':
                self.library.delete_book(isbn=isbn)
                self.output.insert(END, f'Deleted {book_to_delete}')
                self.isbn_to_delete.delete(first=0, last=END)
        else:
            self.output.insert(END, 'Enter ISBN of the book to delete')

    def __open_settings__(self):
        settings_window = Toplevel(bg=ABOUT_WINDOW_COLOR)
        settings_window.title('Settings')
        frame = LabelFrame(master=settings_window,
                           text='Add location options',
                           highlightbackground=WIDGET_FRAME_COLOR,
                           highlightthickness=WIDGET_FRAME_BORDER,
                           bg=MAIN_BACKGROUND_COLOR)
        frame.grid(column=0, row=0, padx=20, pady=20)

        self.new_location_entry = Entry(frame)
        self.new_location_entry.grid(column=0, row=0, padx=20, pady=10)

        add_button = Button(frame, text='Add', command=self.__add_location__)
        add_button.grid(column=0, row=1, padx=20, pady=10)


    def __open_about__(self):
        about_window = Toplevel(bg=ABOUT_WINDOW_COLOR)
        about_window.title('About')
        about_window.geometry('250x100')
        label = Label(about_window, text='Personal Library Manager\nby Max Nekrasov\n\n2024', justify=LEFT, bg=ABOUT_WINDOW_COLOR)
        label.grid(column=0, row=0, padx=20, pady=20)

    def __add_location__(self):
        new_location = self.new_location_entry.get().strip()

# ----------------------------- Book pop-up window -----------------------------#

    def __click__(self, event):
        # Get book object from selection
        selection = self.output.curselection()
        book = self.list_of_books[selection[0]]

        # Create pop-up window
        self.window = Toplevel(bg=MAIN_BACKGROUND_COLOR,
                               padx=MAIN_WINDOW_PADDING,
                               pady=MAIN_WINDOW_PADDING)
        self.window.title('Book Details')

        # Fill pop-up window with widgets and book information
        self.text_containers = {}
        combobox_fields = {'is_read': ['Yes', 'Not yet'],
                           'rating': BOOK_RATING_OPTIONS,
                           'location': self.book_location_options}
        centered_row = 0
        right_row = left_row = 4
        for attribute, content in book.get_all_info().items():
            frame = LabelFrame(master=self.window,
                               text=f'{content[0]}',
                               highlightbackground=WIDGET_FRAME_COLOR,
                               highlightthickness=WIDGET_FRAME_BORDER,
                               bg=MAIN_BACKGROUND_COLOR,
                               bd=0)
            text_container_width = ENTRY_WIDTH
            if attribute in ['title', 'author', 'description', 'notes']:
                frame.grid(column=0, row=centered_row, columnspan=2)
                text_container_width = 70
            elif attribute in ['is_read', 'current_page', 'rating']:
                frame.grid(column=0, row=right_row)
                right_row += 1
            else:
                frame.grid(column=1, row=left_row)
                left_row += 1
            if attribute == 'description':
                container = Text(frame,
                                 bg=BOOK_WINDOW_TEXT_BG_COLOR,
                                 height=BOOK_WINDOW_DESCRIPTION_HEIGHT,
                                 wrap='word',
                                 font=BOOK_WINDOW_TEXT_FONT)
            elif attribute == 'notes':
                container = Text(frame,
                                 bg=BOOK_WINDOW_TEXT_BG_COLOR,
                                 height=BOOK_WINDOW_NOTES_HEIGHT,
                                 wrap='word',
                                 font=BOOK_WINDOW_TEXT_FONT)
            elif attribute in combobox_fields:
                container = ttk.Combobox(frame,
                                         font=BOOK_WINDOW_TEXT_FONT,
                                         values=combobox_fields[attribute],
                                         foreground='black')
                text_container_width = ENTRY_WIDTH - 2
            else:
                container = Text(frame,
                                 bg=BOOK_WINDOW_TEXT_BG_COLOR,
                                 height=1,
                                 wrap='word',
                                 font=BOOK_WINDOW_TEXT_FONT)
            container.insert(tkinter.END, f'{content[1]}')
            container.config(state='disabled', width=text_container_width)
            container.grid(column=0, row=0, pady=BOOK_WINDOW_FRAME_PADDING)
            self.text_containers[attribute] = container
            centered_row += 1

        # Create 'Edit' button
        edit_button = Button(self.window, text='Edit book', width=BUTTON_WIDTH, command=self.__edit_book__)
        edit_button.grid(column=0, row=7, pady=BUTTON_PADDING)

        # Create 'Save' button
        save_button = Button(self.window, text='Save changes', width=BUTTON_WIDTH, command=self.__save_changes__)
        save_button.grid(column=0, row=8, pady=BUTTON_PADDING)

        # Create 'Delete' button
        save_button = Button(self.window, text='Delete book', width=BUTTON_WIDTH, command=self.__delete_book_alt__)
        save_button.grid(column=1, row=8, columnspan=2, pady=BUTTON_PADDING)

        self.window.mainloop()

# ----------------------------- Pop-up window button functionality -----------------------------#

    # TODO: fix bug when 'description' is set to the content of 'column name

    def __edit_book__(self):
        self.isbn_to_update = self.text_containers['isbn'].get('1.0', tkinter.END).strip()
        for attr, container in self.text_containers.items():
            if container.winfo_class() == 'TCombobox':
                container.config(state='normal')
            else:
                container.config(state='normal', bg=BOOK_WINDOW_TEXT_BG_COLOR_EDIT)

    def __save_changes__(self):
        isbn = self.isbn_to_update
        book_attributes = ['title', 'author', 'description', 'notes', 'is_read', 'current_page', 'rating', 'is_lent',
                           'location', 'isbn']
        ind = 0
        for attr, container in self.text_containers.items():
            if container.winfo_class() == 'TCombobox':
                content = container.get().strip()
                container.config(state='disabled')
                if content == 'Yes':
                    content = 'True'
                elif content == 'Not yet':
                    content = 'False'
            else:
                content = container.get('1.0', tkinter.END).strip()
                container.config(state='disabled', bg=BOOK_WINDOW_TEXT_BG_COLOR)
            self.library.update_book(isbn=isbn, attribute=(book_attributes[ind], content))
            ind += 1
        self.__display_all__()

    def __delete_book_alt__(self):
        isbn = self.text_containers['isbn'].get('1.0', tkinter.END).strip()
        confirm = messagebox.askquestion('Delete book',
                                         'Are you sure you want to delete the book?',
                                         icon=messagebox.WARNING)
        if confirm == 'yes':
            self.library.delete_book(isbn=isbn)
            self.__display_all__()
            self.window.destroy()

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
