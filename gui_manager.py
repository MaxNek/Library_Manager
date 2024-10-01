import tkinter
from database_manager import Library
from config_manager import AppConfig
from book import Book
from tkinter import *
from tkinter import messagebox
import tkinter.ttk as ttk

#----------------------------- GUI layout settings -----------------------------#

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

# TODO: consider giving user the ability to set their own rating scale.
BOOK_RATING_OPTIONS = ['', '1', '2', '3', '4', '5']

TOP_MENU_WINDOW_COLOR = 'light steel blue'
TOP_MENU_WINDOW_MARGIN = 20

#----------------------------- GUI -----------------------------#

class GuiApp(Tk):
    """
    A class to create Graphical User Interface to interact with books database. Extends tkinter.Tk.

    :param library: Library object.
    """
    def __init__(self, library: Library):
        super().__init__()
        self.library = library

        # Enable configuration manager.
        self.app_config = AppConfig()

        # Get book location options if any were saved.
        self.book_location_options = self.app_config.get_book_locations()

        # Create main gui window.
        self.title('My Personal Library')
        self.config(bg=MAIN_BACKGROUND_COLOR, padx=MAIN_WINDOW_PADDING, pady=MAIN_WINDOW_PADDING)

        # Add widgets to the main window.
        self.__view_all_widget__()
        self.__output_widget__()
        self.__add_book_widget__()
        self.__find_book_widget__()
        self.__delete_book_widget__()
        self.__menu__()

        # Set dropdown entry fields styling for 'readonly' and 'disabled' states.
        style = ttk.Style()
        style.theme_settings("default",
                             {"TCombobox": {"map": {
                                 "fieldbackground":[
                                     ("readonly", BOOK_WINDOW_TEXT_BG_COLOR_EDIT),
                                     ("disabled", BOOK_WINDOW_TEXT_BG_COLOR)]}}})
        style.theme_use("default")

        # Create a list to store currently displayed books as Book objects.
        self.list_of_books = []

#----------------------------- Functions to create widgets -----------------------------#

    def __view_all_widget__(self):
        # Create widget frame and name
        frame = self.__make_frame__(column=0, row=0, widget_name='Show all books')

        # Create 'Sort by' dropdown field as read only. Set it to 'title' by default.
        sort_options = ['Title', 'Author', 'Rating']
        sort_label = Label(frame, text='Sort by:', bg=MAIN_BACKGROUND_COLOR)
        sort_label.grid(column=0, row=1)
        self.sort_by = tkinter.ttk.Combobox(frame, state="readonly", values=sort_options)
        self.sort_by.set('Title')
        self.sort_by.grid(column=0, row=2)

        # Create 'Show' button
        button = Button(frame, text='Show', width=BUTTON_WIDTH, command=self.__view_all__)
        button.grid(column=0, row=3, pady=BUTTON_PADDING)

    def __add_book_widget__(self):
        # Create widget frame and name
        frame = self.__make_frame__(column=1, row=0, rowspan=2, widget_name='Add a book')

        # A list to store all entry field objects
        self.add_book_entries = []

        # Indicates dropdown fields and their options (ttk.combobox).
        combobox_fields = {'is_read': ['Yes', 'Not yet'],
                           'rating': BOOK_RATING_OPTIONS,
                           'location': self.book_location_options}

        # A dictionary to store all entry fields as element 1 of the list in the value.
        self.add_book_dict = {'title': ['Book title'],
                      'author': ['Author\'s name'],
                      'description': ['Book description'],
                      'notes': ['My notes'],
                      'is_read': ['Has the book been read?'],
                      'current_page': ['Currently at page'],
                      'rating': ['My rating'],
                      'is_lent': ['Book is lent to'],
                      'location': ['Location at home'],
                      'isbn': ['ISBN']}

        # Create entry fields: name, field. Ad them to self.add_book_dict.
        col = 0
        row = 0
        for key, value in self.add_book_dict.items():
            label = Label(frame, text=value[0], bg=MAIN_BACKGROUND_COLOR)
            label.grid(column=col, row=row)
            if key in combobox_fields:
                state = "normal" if key == 'location' else "readonly"
                self.entry = ttk.Combobox(frame, state=state, values=combobox_fields[key])
            else:
                self.entry = Entry(frame, width=ENTRY_WIDTH)
            self.entry.grid(column=col, row=row+1, padx=ENTRY_PADDING)
            self.add_book_dict[key].append(self.entry)
            row += 2
            if row == 10:
                row = 0
                col = 1

        # Create 'Add' button.
        button = Button(frame, text='Add', width=BUTTON_WIDTH, command=self.__add_book__)
        button.grid(column=0, row=21, columnspan=2, pady=BUTTON_PADDING)

    def __find_book_widget__(self):
        # Create widget frame and name.
        frame = self.__make_frame__(column=0, row=1, widget_name='Find books')

        # Create 'Search by' dropdown. Set 'Search by' to 'title' by default.
        book_search_options = ['Title', 'Author', 'Has been read?', 'Rating', 'In notes', 'In description',
                               'Has been borrowed?', 'Has been lent to', 'Location', 'ISBN']
        search_by_label = Label(frame, text='Search:', bg=MAIN_BACKGROUND_COLOR)
        search_by_label.grid(column=0, row=1)
        self.search_by = tkinter.ttk.Combobox(frame, state="readonly", values=book_search_options)
        self.search_by.set('Title')
        self.search_by.grid(column=0, row=2)

        # Create entry field to enter search criteria.
        self.search_by_entry = Entry(frame, width=ENTRY_WIDTH)
        self.search_by_entry.grid(column=0, row=3, pady=ENTRY_PADDING)

        # Create 'Find' button.
        button = Button(frame, text='Find', width=BUTTON_WIDTH, command=self.__find_book__)
        button.grid(column=0, row=4, pady=BUTTON_PADDING)

    def __delete_book_widget__(self):
        # Create widget frame and name.
        frame = self.__make_frame__(column=1, row=3, columnspan=2, widget_name='Delete book by ISBN:')

        # Create entry field to enter ISBN of the book to delete.
        self.isbn_to_delete = Entry(frame, width=ENTRY_WIDTH)
        self.isbn_to_delete.grid(column=2, row=0, padx=ENTRY_PADDING)

        # Create 'Delete' button.
        button = Button(frame, text='Delete', width=BUTTON_WIDTH, command=self.__delete_book__)
        button.grid(column=3, row=0, padx=BUTTON_PADDING)

    def __output_widget__(self):
        # Create a scrollbar.
        # TODO: make scrollbar height same as the output screen.
        self.scrollbar = Scrollbar(self)
        self.scrollbar.grid(column=2, row=2)

        # Create an output screen.
        self.output = Listbox(width=OUTPUT_WIDTH, height=OUTPUT_HEIGHT, yscrollcommand=self.scrollbar.set)
        self.output.grid(column=0, row=2, columnspan=2, padx=WIDGET_PADDING, pady=WIDGET_PADDING)

        # Attach the scrollbar to the output screen.
        self.scrollbar.config(command=self.output.yview)

        # When a book is double-clicked open book's window (call self.__click__ function).
        self.output.bind('<Double-1>', self.__click__)


# ----------------------------- Create menu -----------------------------#

    def __menu__(self):
        # Create menu bar and add it to the main window.
        menubar = Menu(self)
        self.config(menu=menubar)

        # TODO: add 'Help' option to the Menu.
        # Create 'Menu' dropdown and add it to the menu bar.
        menu = Menu(menubar, tearoff=0)
        menu.add_command(label='Settings', command=self.__open_settings__)
        menu.add_command(label='About', command=self.__open_about__)
        menu.add_separator()
        menu.add_command(label='Exit', command=self.destroy)
        menubar.add_cascade(label='Menu', menu=menu)

# ----------------------------- Widget button functionality -----------------------------#

    def __view_all__(self):
        # CLear 'list_of_books' and the output screen.
        self.list_of_books.clear()
        self.output.delete(first=0, last=END)

        # Get sort criteria from the user and query in the database.
        sort = self.sort_by.get().lower()
        all_books = self.library.all_books(sort=sort)

        # Display books in the output screen:
        # Sort by title - {title} by {author}
        # Sort by author - {author}, {title}
        # Sort by other criteria - {criteria} {book}
        for book in all_books:
            sort_option_names = {'title': book.title, 'author': book.author, 'rating': book.rating}
            if sort == 'title':
                self.output.insert(END, f'"{book.title}" by {book.author}')
            elif sort == 'author':
                self.output.insert(END, f'{book.author}, "{book.title}"')
            else:
                self.output.insert(END, f'{sort_option_names[sort]} {book}')

            # Add a book to 'list_of_books'.
            self.list_of_books.append(book)

    def __add_book__(self):
        # CLear 'list_of_books' and the output screen.
        self.list_of_books.clear()
        self.output.delete(first=0, last=END)

        # Check if 'title' and 'isbn' were entered.
        # If yes, create a Book object from the entry fields and notify user.
        # If not, notify user to fill the required fields and notify user.
        if self.add_book_dict['isbn'][1].get() != '' and self.add_book_dict['title'][1].get() != '':
            is_read = True if self.add_book_dict['is_read'][1].get() == 'Yes' else False
            is_lent = '' if self.add_book_dict['is_lent'][1].get() == '' else self.add_book_dict['is_lent'][1].get().title().strip()
            new_book = Book(
                title=self.add_book_dict['title'][1].get().title().strip(),
                author=self.add_book_dict['author'][1].get().title().strip(),
                description=self.add_book_dict['description'][1].get().replace('"', "'").strip(),
                is_read=is_read,
                current_page=self.add_book_dict['current_page'][1].get().strip(),
                rating=self.add_book_dict['rating'][1].get(),
                notes=self.add_book_dict['notes'][1].get().strip(),
                is_lent=is_lent,
                location=self.add_book_dict['location'][1].get().lower().strip(),
                isbn=self.add_book_dict['isbn'][1].get().strip())

            # Attempt the add book to the database. Interpret the results and notify user.
            result = self.library.add_book(new_book)
            if result:
                self.list_of_books.append(result)
                self.output.insert(END, result, 'has been added to the library')
            else:
                book = self.library.find_book(criteria=('isbn', new_book.isbn.strip()))[0]
                self.list_of_books.append(book)
                self.output.insert(END, book, 'was already in the library')

            # Clear entry fields.
            for key, value in self.add_book_dict.items():
                if type(value[1]) == tkinter.ttk.Combobox:
                    value[1].set('')
                else:
                    value[1].delete(first=0, last=END)
        else:
            self.output.insert(END, 'Book title and ISBN must be entered')

    def __find_book__(self):
        # Create user-friendly search options and their representation in the database.
        book_search_user_options = {'Has been read?': 'is_read',
                                      'In notes': 'notes',
                                      'In description': 'description',
                                      'Has been borrowed?': 'is_lent',
                                      'Has been lent to': 'is_lent'}

        # CLear 'list_of_books' and the output screen.
        self.list_of_books.clear()
        self.output.delete(first=0, last=END)

        # Check if search option and prompt were entered and construct a search criteria ('search option', 'prompt').
        if self.search_by.get() != '' and self.search_by_entry.get() != '':
            entry = self.search_by_entry.get().lower()
            if self.search_by.get() in book_search_user_options:
                attribute = book_search_user_options[f'{self.search_by.get()}']
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

            # Search for books in the database by the criteria. Add results to 'list_of_books'.
            result = self.library.find_book(criteria=criteria)
            for book in result:
                self.output.insert(END, book)
                self.list_of_books.append(book)

            # Clear entry fields.
            self.search_by.set('')
            self.search_by_entry.delete(first=0, last=END)

    def __delete_book__(self):
        # CLear the output screen.
        self.output.delete(first=0, last=END)

        # Check is ISBN of the book to delete was entered. If not, notify user to enter it.
        # Display a pop-up message asking user to confirm book deletion.
        # If confirmed, delete the book from the database and notify the user.
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
                self.list_of_books.clear()
        else:
            self.output.insert(END, 'Enter ISBN of the book to delete')

# ----------------------------- Menu functionality -----------------------------#

    def __open_settings__(self):
        # Create 'Settings' window.
        settings_window = Toplevel(bg=TOP_MENU_WINDOW_COLOR)
        settings_window.title('Settings')

        # Create widget to add/remove book location.
        frame = LabelFrame(master=settings_window,
                           text='Configure location options',
                           highlightbackground=WIDGET_FRAME_COLOR,
                           highlightthickness=WIDGET_FRAME_BORDER,
                           bg=MAIN_BACKGROUND_COLOR)
        frame.grid(column=0, row=0, padx=TOP_MENU_WINDOW_MARGIN, pady=TOP_MENU_WINDOW_MARGIN)

        # Create widget's entry field
        self.new_location_entry = Entry(frame, width=ENTRY_WIDTH*2)
        self.new_location_entry.grid(column=0, row=0, columnspan=2, padx=TOP_MENU_WINDOW_MARGIN, pady=TOP_MENU_WINDOW_MARGIN-10)

        # Create 'Add'/'Remove' buttons.
        add_button = Button(frame, text='Add', width=BUTTON_WIDTH, command=self.__add_location__)
        add_button.grid(column=0, row=1, padx=TOP_MENU_WINDOW_MARGIN, pady=TOP_MENU_WINDOW_MARGIN-10)
        remove_button = Button(frame, text='Remove', width=BUTTON_WIDTH, command=self.__remove_location__)
        remove_button.grid(column=1, row=1, padx=TOP_MENU_WINDOW_MARGIN, pady=TOP_MENU_WINDOW_MARGIN-10)

    def __open_about__(self):
        # Create 'About' window with information.
        about_window = Toplevel(bg=TOP_MENU_WINDOW_COLOR)
        about_window.title('About')
        label = Label(about_window, text='Personal Library Manager\nby Max Nekrasov\n\n2024', justify=LEFT, bg=TOP_MENU_WINDOW_COLOR)
        label.grid(column=0, row=0, padx=TOP_MENU_WINDOW_MARGIN, pady=TOP_MENU_WINDOW_MARGIN)

# ----------------------------- Menu > Settings window functionality -----------------------------#

    def __add_location__(self):
        # Get new book location from the user and attempt to add it to app configuration.
        new_location = self.new_location_entry.get().strip()
        result = self.app_config.add_book_location(new_location)

        # Interpret the result of configuration_manager, construct message, and notify user in pop-up message window.
        if result == 1:
            message_text = (f'"{new_location}" has been added to the list of locations.'
                            f'\n\nRestart the application to implement the change')
        elif result == 0:
            message_text = 'This location already exists'
        else:
            message_text = 'Error adding a location. Try again'
        messagebox.showinfo(title='Book locations', message=message_text)
        self.new_location_entry.delete(first=0, last=END)

    def __remove_location__(self):
        # Get  book location from the user and attempt to remove it from app configuration.
        location = self.new_location_entry.get().strip()
        result = self.app_config.remove_book_location(location)

        # Interpret the result of configuration_manager, construct message, and notify user in pop-up message window.
        if result == 1:
            message_text = (f'"{location}" has been removed from the list of locations.'
                            f'\n\nRestart the application to implement the change')
        elif result == 0:
            message_text = 'This location was not saved'
        else:
            message_text = 'Error adding a location. Try again'
        messagebox.showinfo(title='Book locations', message=message_text)
        self.new_location_entry.delete(first=0, last=END)

# ----------------------------- Individual book pop-up window -----------------------------#

    def __click__(self, event):
        # This function is called when user double-clicks on a book in the output screen.
        # Get Book object from selection in the output screen.
        selection = self.output.curselection()
        try:
            self.open_book = self.list_of_books[selection[0]]

            # Create pop-up window for the selected book.
            self.window = Toplevel(bg=MAIN_BACKGROUND_COLOR,
                                   padx=MAIN_WINDOW_PADDING,
                                   pady=MAIN_WINDOW_PADDING)
            self.window.title('Book Details')

            # Dictionary to store text_fields.
            self.text_containers = {}

            # Dropdown fields options.
            combobox_fields = {'is_read': ['Yes', 'Not yet'],
                               'rating': BOOK_RATING_OPTIONS,
                               'location': self.book_location_options}

            # Create text fields and dropdowns. Lay out on the window. Add to 'text_containers' dictionary.
            centered_row = 0
            right_row = left_row = 4
            for attribute, content in self.open_book.get_all_info().items():
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

            # Create edit frame to hold edit buttons. Frame is not visible to user.
            edit_frame = Frame(self.window, bg=MAIN_BACKGROUND_COLOR)
            edit_frame.grid(column=0, row=7)

            # Create 'Edit' button (inside edit frame).
            edit_button = Button(edit_frame, text='Edit book', width=BUTTON_WIDTH*2, command=self.__edit_book__)
            edit_button.grid(column=0, row=0, columnspan=2, pady=BUTTON_PADDING)

            # Create 'Save' button (inside edit frame).
            save_button = Button(edit_frame, text='Save changes', width=BUTTON_WIDTH-1, command=self.__save_changes__)
            save_button.grid(column=0, row=1, pady=BUTTON_PADDING)

            # Create 'Discard changes' button (inside edit frame).
            save_button = Button(edit_frame, text='Discard changes', width=BUTTON_WIDTH-1, command=self.__discard_changes__)
            save_button.grid(column=1, row=1, pady=BUTTON_PADDING)

            # Create 'Delete' button.
            save_button = Button(self.window, text='Delete book', width=BUTTON_WIDTH, command=self.__delete_book_alt__)
            save_button.grid(column=1, row=7, columnspan=1, pady=BUTTON_PADDING)

            # Keep book pop-up window running until it is closed by the user.
            self.window.mainloop()
        except IndexError:
            pass

# ----------------------------- Pop-up window button functionality -----------------------------#

    def __edit_book__(self):
        # Get and hold on book's ISBN.
        self.isbn_to_update = self.text_containers['isbn'].get('1.0', tkinter.END).strip()

        # Enable text containers and dropdown fields for editing.
        for attr, container in self.text_containers.items():
            if container.winfo_class() == 'TCombobox':
                container.config(state='normal')
            else:
                container.config(state='normal', bg=BOOK_WINDOW_TEXT_BG_COLOR_EDIT)

    def __save_changes__(self):
        # Hold on book's original ISBN.
        isbn = self.isbn_to_update

        # Create a list of database column names.
        book_attributes = ['title', 'author', 'description', 'notes', 'is_read', 'current_page', 'rating', 'is_lent',
                           'location', 'isbn']

        # Get user edits and update the book in the database. Use original ISBN to find the book.
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
                content = container.get('1.0', tkinter.END).strip().replace('"', "'")
                container.config(state='disabled', bg=BOOK_WINDOW_TEXT_BG_COLOR)
            self.library.update_book(isbn=isbn, attribute=(book_attributes[ind], content))
            ind += 1

        # Refresh output screen with updated book.
        self.__view_all__()

    def __discard_changes__(self):
        # Delete all content from all entry fields.
        # Replace it with the content from the database for this book.
        # Disable entry fields for editing.
        book = self.open_book
        for key, value in book.get_all_info().items():
            if type(self.text_containers[key]) == tkinter.ttk.Combobox:
                self.text_containers[key].set('')
            else:
                self.text_containers[key].delete('1.0', 'end')
            self.text_containers[key].insert(tkinter.END, f'{value[1]}')
            if type(self.text_containers[key]) == tkinter.ttk.Combobox:
                self.text_containers[key].config(state='disabled')
            else:
                self.text_containers[key].config(state='disabled', bg=BOOK_WINDOW_TEXT_BG_COLOR)

    def __delete_book_alt__(self):
        # Get and hold on book's ISBN.
        isbn = self.text_containers['isbn'].get('1.0', tkinter.END).strip()

        # Confirm if user wants to delete the book.
        # If yes, delete the book from the database and close the book pop-up window.
        # Refresh the output screen without the deleted book.
        confirm = messagebox.askquestion('Delete book',
                                         'Are you sure you want to delete the book?',
                                         icon=messagebox.WARNING)
        if confirm == 'yes':
            self.library.delete_book(isbn=isbn)
            self.__view_all__()
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
