import tkinter
from tkinter.ttk import Combobox

from source.database import Library
from source.config import AppConfig
from source.book import Book, BookTemplate
from tkinter import *
from tkinter import messagebox
import tkinter.ttk as ttk

#----------------------------- GUI layout settings -----------------------------#

MAIN_WINDOW_TITLE = 'My Personal Library'
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

TOP_MENU_WINDOW_COLOR = 'light steel blue'
TOP_MENU_WINDOW_MARGIN = 20
TOP_MENU_WINDOW_PADDING = 15

ABOUT_TEXT = 'Personal Library Manager\nby Max Nekrasov\n\n2024'

#----------------------------- GUI -----------------------------#

class Gui(Tk):
    """
    A class to create Graphical User Interface to interact with books database. Extends tkinter.Tk.

    :param library: Library object.
    """
    def __init__(self, library: Library):
        super().__init__()
        self.library = library
        self.app_config = AppConfig()
        self.book_template = BookTemplate()
        self.template = self.book_template.get_template_data()

        self.title(MAIN_WINDOW_TITLE)
        self.config(bg=MAIN_BACKGROUND_COLOR, padx=MAIN_WINDOW_PADDING, pady=MAIN_WINDOW_PADDING)

        self.__view_all_widget__()
        self.__output_widget__()
        self.__add_book_widget__()
        self.__find_book_widget__()
        self.__delete_book_widget__()
        self.__menu__()

        # Set styling for ttk elements.
        style = ttk.Style()
        style.theme_settings('default',{
            'TCombobox': {
                'map': {
                    'fieldbackground':[
                        ('readonly', BOOK_WINDOW_TEXT_BG_COLOR_EDIT),
                        ('disabled', BOOK_WINDOW_TEXT_BG_COLOR)
                    ]}}})
        style.configure('TCombobox', fieldbackground='orange')
        style.theme_use('default')

        self.current_books = []

#----------------------------- Functions to create widgets -----------------------------#

    def __view_all_widget__(self):
        frame = __make_frame__(master=self, column=0, row=0, widget_name='Show all books')

        sort_options = [value['name'] for key, value in self.template.items() if value['sort_all_by']]
        sort_label = Label(frame, text='Sort by:', bg=MAIN_BACKGROUND_COLOR)
        sort_label.grid(column=0, row=1)
        self.sort_by = tkinter.ttk.Combobox(frame, state="readonly", values=sort_options)
        self.sort_by.set(self.template['title']['name'])
        self.sort_by.grid(column=0, row=2)

        button = Button(frame, text='Show', width=BUTTON_WIDTH, command=self.__view_all__)
        button.grid(column=0, row=3, pady=BUTTON_PADDING)

    def __add_book_widget__(self):
        frame = __make_frame__(master=self, column=1, row=0, rowspan=2, widget_name='Add a book')

        self.add_book_entries = {}
        count = row = 0
        for key, value in self.book_template.get_template_data().items():
            column = 0 if count % 2 == 0 else 1
            label = Label(frame, text=value['name'], bg=MAIN_BACKGROUND_COLOR)
            label.grid(column=column, row=row)
            if value['selectable']:
                self.entry = ttk.Combobox(frame, state=value['def_state'], values=value['options'])
            else:
                self.entry = Entry(frame, width=ENTRY_WIDTH)
            self.entry.grid(column=column, row=row + 1, padx=ENTRY_PADDING)
            self.add_book_entries[key] = self.entry
            count += 1
            if count != 0 and count % 2 == 0:
                row += 2

        button = Button(frame, text='Add', width=BUTTON_WIDTH, command=self.__add_book__)
        button.grid(column=0, row=row, columnspan=2, pady=BUTTON_PADDING)

    def __find_book_widget__(self):
        frame = __make_frame__(master=self, column=0, row=1, widget_name='Find books')

        search_options = [value['name'] for key, value in self.template.items() if value['search_by']]
        search_options.append('Has been borrowed?')
        search_by_label = Label(frame, text='Search:', bg=MAIN_BACKGROUND_COLOR)
        search_by_label.grid(column=0, row=1)
        self.search_by = tkinter.ttk.Combobox(frame, state="readonly", values=search_options)
        self.search_by.set(self.template['title']['name'])
        self.search_by.grid(column=0, row=2)

        self.search_by_entry = Entry(frame, width=ENTRY_WIDTH)
        self.search_by_entry.grid(column=0, row=3, pady=ENTRY_PADDING)

        button = Button(frame, text='Find', width=BUTTON_WIDTH, command=self.__find_book__)
        button.grid(column=0, row=4, pady=BUTTON_PADDING)

    def __delete_book_widget__(self):
        frame = __make_frame__(master=self, column=1, row=3, columnspan=2, widget_name='Delete book by ISBN:')

        self.isbn_to_delete = Entry(frame, width=ENTRY_WIDTH)
        self.isbn_to_delete.grid(column=2, row=0, padx=ENTRY_PADDING)

        button = Button(frame, text='Delete', width=BUTTON_WIDTH, command=self.__delete_book__)
        button.grid(column=3, row=0, padx=BUTTON_PADDING)

    def __output_widget__(self):
        # TODO: make scrollbar height same as the output screen.
        scrollbar = Scrollbar(self)
        scrollbar.grid(column=2, row=2)

        self.output = Listbox(width=OUTPUT_WIDTH, height=OUTPUT_HEIGHT, yscrollcommand=scrollbar.set)
        self.output.grid(column=0, row=2, columnspan=2, padx=WIDGET_PADDING, pady=WIDGET_PADDING)

        scrollbar.config(command=self.output.yview)

        self.output.bind('<Double-1>', self.__click__)

# ----------------------------- Create menu -----------------------------#

    def __menu__(self):
        menubar = Menu(self)
        self.config(menu=menubar)

        # TODO: add 'Help' option to the Menu.
        menu = Menu(menubar, tearoff=0)
        menu.add_command(label='Settings', command=self.__open_settings__)
        menu.add_command(label='About', command=self.__open_about__)
        menu.add_separator()
        menu.add_command(label='Exit', command=self.destroy)
        menubar.add_cascade(label='Menu', menu=menu)

# ----------------------------- Widget button functionality -----------------------------#

    def __view_all__(self):
        self.__clear_screen__()

        sort = self.sort_by.get()
        sort_by = 'title'
        for key, value in self.book_template.get_template_data().items():
            if value['name'] == sort:
                sort_by = key
        all_books = self.library.all_books(sort=sort)

        for book in all_books:
            if sort_by == 'title':
                self.output.insert(END, f'"{book.get_this_info('title')}" by {book.get_this_info('author')}')
            elif sort_by == 'author':
                self.output.insert(END, f'{book.get_this_info('author')}, "{book.get_this_info('title')}"')
            else:
                self.output.insert(END, f'{book.get_this_info(sort_by)} {book}')
            self.current_books.append(book)

    def __add_book__(self):
        self.__clear_screen__()

        # TODO: title() entries.
        entries = self.add_book_entries
        if entries['isbn'].get() != '' and entries['title'].get() != '':
            kwargs = {}
            for key, value in entries.items():
                if key == 'is_read':
                    kwargs[key] = 'True' if value.get() == 'Yes' else 'False'
                elif key == 'is_lent':
                    kwargs[key] = '' if value.get() == '' else value.get().title().strip()
                elif key == 'description' or key == 'notes':
                    kwargs[key] = value.get().strip()
                elif key == 'title' or key == 'author':
                    kwargs[key] = value.get().strip().title()
                else:
                    kwargs[key] = value.get().strip().capitalize()
            new_book = Book(**kwargs)

            result = self.library.add_book(new_book)
            if result:
                self.current_books.append(result)
                self.output.insert(END, result, 'has been added to the library')
            else:
                book = self.library.find_book(criteria=('isbn', new_book.get_this_info('isbn')))[0]
                self.current_books.append(book)
                self.output.insert(END, book, 'was already in the library')

            for key, value in entries.items():
                if value.winfo_class() == 'TCombobox':
                    value.set('')
                else:
                    value.delete(first=0, last=END)
        else:
            self.output.insert(END, 'Book title and ISBN must be entered')

    def __find_book__(self):
        self.__clear_screen__()

        search_by = self.search_by.get()
        entry = self.search_by_entry.get().lower()
        if search_by != '' and entry != '':
            if search_by == 'Has been borrowed?':
                attribute = 'is_lent'
                prompt = 'is_lent_yes' if entry == 'yes' else 'is_lent_no'
            else:
                for key, value in self.template.items():
                    if value['name'] == search_by:
                        attribute = key
                prompt = entry

            criteria = (attribute, prompt)
            result = self.library.find_book(criteria=criteria)
            for book in result:
                self.output.insert(END, book)
                self.current_books.append(book)

            self.search_by_entry.delete(first=0, last=END)

    def __delete_book__(self):
        self.__clear_screen__()

        delete_isbn = self.isbn_to_delete.get().strip()
        if delete_isbn != '':
            result = self.library.find_book(('isbn_to_delete', delete_isbn))
            if result:
                book_to_delete = result[0]
                confirm = messagebox.askquestion(title='Delete book',
                                                 message=f'Are you sure you want to delete {book_to_delete}?',
                                                 icon=messagebox.WARNING)
                if confirm == 'yes':
                    self.library.delete_book(isbn=delete_isbn)
                    self.output.insert(END, f'Deleted {book_to_delete}')
                    self.isbn_to_delete.delete(first=0, last=END)
            else:
                self.output.insert(END, f'There is no bok with ISBN {delete_isbn} in the library')
        else:
            self.output.insert(END, 'Enter ISBN of the book to delete')

# ----------------------------- Menu functionality -----------------------------#
    # TODO: Dropdown for locations
    def __open_settings__(self):
        settings_window = Toplevel(bg=TOP_MENU_WINDOW_COLOR, pady=TOP_MENU_WINDOW_PADDING)
        settings_window.title('Settings')

        locations_frame = __make_frame__(master=settings_window, column=0, row=0, widget_name='Location options')
        self.new_location_entry = Entry(locations_frame, width=ENTRY_WIDTH*2)
        self.new_location_entry.grid(column=0, row=0, columnspan=2, padx=TOP_MENU_WINDOW_MARGIN, pady=TOP_MENU_WINDOW_MARGIN-10)
        add_button = Button(locations_frame, text='Add', width=BUTTON_WIDTH, command=self.__add_location__)
        add_button.grid(column=0, row=1, padx=TOP_MENU_WINDOW_MARGIN, pady=TOP_MENU_WINDOW_MARGIN-10)
        remove_button = Button(locations_frame, text='Remove', width=BUTTON_WIDTH, command=self.__remove_location__)
        remove_button.grid(column=1, row=1, padx=TOP_MENU_WINDOW_MARGIN, pady=TOP_MENU_WINDOW_MARGIN-10)

        rating_frame = __make_frame__(master=settings_window, column=0, row=1, widget_name='Rating scale')
        self.rating_entries = {
            'From': {'values': [str(i) for i in range(0, 101)]},
            'To': {'values': [str(i) for i in range(0, 101)]},
            'Step': {'values': ['0.25', '0.5', '1']}
        }
        column = 0
        for key, value in self.rating_entries.items():
            self.rating_entries[key]['label'] = Label(rating_frame, text=key, bg=MAIN_BACKGROUND_COLOR)
            self.rating_entries[key]['entry'] = Combobox(rating_frame,
                                                         state='readonly',
                                                         width=ENTRY_WIDTH//2,
                                                         values=value['values'])
            self.rating_entries[key]['label'].grid(column=column, row=0)
            self.rating_entries[key]['entry'].grid(column=column, row=1, pady=TOP_MENU_WINDOW_MARGIN - 10, padx=12)
            column += 1
        set_button = Button(rating_frame, text='Set rating', width=BUTTON_WIDTH, command=self.__set_rating__)
        set_button.grid(column=0, row=3, columnspan=3, padx=TOP_MENU_WINDOW_MARGIN, pady=TOP_MENU_WINDOW_MARGIN-10)

    def __open_about__(self):
        about_window = Toplevel(bg=TOP_MENU_WINDOW_COLOR)
        about_window.title('About')
        label = Label(about_window, text=ABOUT_TEXT, justify=LEFT, bg=TOP_MENU_WINDOW_COLOR)
        label.grid(column=0, row=0, padx=TOP_MENU_WINDOW_MARGIN, pady=TOP_MENU_WINDOW_MARGIN)

# ----------------------------- Menu > Settings window functionality -----------------------------#

    def __add_location__(self):
        new_location = self.new_location_entry.get().strip().title()
        if new_location != '':
            result = self.app_config.add_book_location(new_location)
            self.__show_messge__(result=result, location=new_location, act='add')


    def __remove_location__(self):
        location = self.new_location_entry.get().strip().title()
        if location != '':
            result = self.app_config.remove_book_location(location)
            self.__show_messge__(result=result, location=location, act='remove')

    def __set_rating__(self):
        start = int(self.rating_entries['From']['entry'].get())
        end = int(self.rating_entries['To']['entry'].get())
        step = float(self.rating_entries['Step']['entry'].get())
        self.app_config.set_rating_scale(start=start, end=end, step=step)
        messagebox.showinfo(title='Book rating', message='New rating scale has been saved')
        self.new_location_entry.delete(first=0, last=END)
        for value in self.rating_entries.values():
            value['entry'].set('')

# ----------------------------- Individual book pop-up window -----------------------------#

    def __click__(self, event):
        """
        This function is called when user double-clicks on a book in the output screen.
        """

        selection = self.output.curselection()
        try:
            self.open_book = self.current_books[selection[0]]
            self.window = Toplevel(bg=MAIN_BACKGROUND_COLOR,
                                   padx=MAIN_WINDOW_PADDING,
                                   pady=MAIN_WINDOW_PADDING)
            self.window.title('Book Details')
            self.text_containers = {}

            book_data = self.open_book.get_all_info()
            centered_row = column = count = 0
            row = len(book_data) - len([key for key,value in book_data.items() if value[0]['width'] == 1])
            for key, value in book_data.items():
                column = 1 if count % 2 == 0 else 0

                frame = LabelFrame(master=self.window,
                                   text=f'{value[0]['name']}',
                                   highlightbackground=WIDGET_FRAME_COLOR,
                                   highlightthickness=WIDGET_FRAME_BORDER,
                                   bg=MAIN_BACKGROUND_COLOR,
                                   bd=0)
                text_container_width = ENTRY_WIDTH

                if value[0]['width'] == 2:
                    frame.grid(column=0, row=centered_row, columnspan=2)
                    text_container_width = 70
                elif value[0]['width'] == 1:
                    frame.grid(column=column, row=row)
                if key == 'description':
                    container = Text(frame,
                                     bg=BOOK_WINDOW_TEXT_BG_COLOR,
                                     height=BOOK_WINDOW_DESCRIPTION_HEIGHT,
                                     wrap='word',
                                     font=BOOK_WINDOW_TEXT_FONT)
                elif key == 'notes':
                    container = Text(frame,
                                     bg=BOOK_WINDOW_TEXT_BG_COLOR,
                                     height=BOOK_WINDOW_NOTES_HEIGHT,
                                     wrap='word',
                                     font=BOOK_WINDOW_TEXT_FONT)
                elif value[0]['selectable']:
                    container = ttk.Combobox(frame,
                                             font=BOOK_WINDOW_TEXT_FONT,
                                             values=value[0]['options'],
                                             foreground='black')
                    text_container_width = ENTRY_WIDTH - 2
                else:
                    container = Text(frame,
                                     bg=BOOK_WINDOW_TEXT_BG_COLOR,
                                     height=1,
                                     wrap='word',
                                     font=BOOK_WINDOW_TEXT_FONT)
                if key == 'is_read':
                    container.insert(tkinter.END, f'{'Yes' if value[1] == 'True' else 'Not yet'}')
                else:
                    container.insert(tkinter.END, f'{value[1]}')
                container.config(state='disabled', width=text_container_width)
                container.grid(column=0, row=0, pady=BOOK_WINDOW_FRAME_PADDING)
                self.text_containers[key] = container
                centered_row += 1
                count += 1
                if count !=0 and count % 2 == 0:
                    row += 1

            edit_frame = Frame(self.window, bg=MAIN_BACKGROUND_COLOR)
            edit_frame.grid(column=0, row=row)

            edit_button = Button(edit_frame, text='Edit book', width=BUTTON_WIDTH*2, command=self.__edit_book__)
            edit_button.grid(column=0, row=0, columnspan=2, pady=BUTTON_PADDING)

            save_button = Button(edit_frame, text='Save changes', width=BUTTON_WIDTH-1, command=self.__save_changes__)
            save_button.grid(column=0, row=1, pady=BUTTON_PADDING)

            save_button = Button(edit_frame, text='Discard changes', width=BUTTON_WIDTH-1, command=self.__discard_changes__)
            save_button.grid(column=1, row=1, pady=BUTTON_PADDING)

            save_button = Button(self.window, text='Delete book', width=BUTTON_WIDTH, command=self.__delete_book_alt__)
            save_button.grid(column=1, row=row, columnspan=1, pady=BUTTON_PADDING)

            self.window.mainloop()
        except IndexError:
            pass

# ----------------------------- Pop-up window button functionality -----------------------------#

    def __edit_book__(self):
        self.isbn_to_update = self.text_containers['isbn'].get('1.0', tkinter.END).strip()

        for attr, container in self.text_containers.items():
            if container.winfo_class() == 'TCombobox':
                container.config(state='normal')
            else:
                container.config(state='normal', bg=BOOK_WINDOW_TEXT_BG_COLOR_EDIT)

    def __save_changes__(self):
        isbn = self.isbn_to_update

        book_attributes = [key for key in self.template]

        ind = 0
        for key, value in self.text_containers.items():
            if value.winfo_class() == 'TCombobox':
                content = value.get().strip()
                value.config(state='disabled')
                if content == 'Yes':
                    content = 'True'
                elif content == 'Not yet':
                    content = 'False'
            else:
                content = value.get('1.0', tkinter.END).strip()
                value.config(state='disabled', bg=BOOK_WINDOW_TEXT_BG_COLOR)
            self.library.update_book(isbn=isbn, attribute=(book_attributes[ind], content))
            ind += 1

        self.__view_all__()

    def __discard_changes__(self):
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
        isbn = self.text_containers['isbn'].get('1.0', tkinter.END).strip()

        confirm = messagebox.askquestion('Delete book',
                                         'Are you sure you want to delete the book?',
                                         icon=messagebox.WARNING)
        if confirm == 'yes':
            self.library.delete_book(isbn=isbn)
            self.__view_all__()
            self.window.destroy()

# ----------------------------- Class utilities -----------------------------#

    def __clear_screen__(self):
        self.current_books.clear()
        self.output.delete(first=0, last=END)

    def __show_messge__(self, result, location, act):
        if result == 1:
            message_text = (f'"{location}" has been {'added to' if act == 'add' else 'removed from'} the list of locations.'
                            f'\n\nRestart the application to implement the change')
        elif result == 0:
            message_text = f'This location {'already exists' if act == 'add' else 'was not saved'}'
        else:
            message_text = 'Error adding a location. Try again'
        messagebox.showinfo(title='Book locations', message=message_text)
        self.new_location_entry.delete(first=0, last=END)

# ----------------------------- Static functions -----------------------------#

def __make_frame__(master, column=0, row=0, columnspan=1, rowspan=1, widget_name='Widget name'):
    frame = LabelFrame(master=master,
                       text=widget_name,
                       highlightbackground=WIDGET_FRAME_COLOR,
                       highlightthickness=WIDGET_FRAME_BORDER,
                       padx=WIDGET_PADDING,
                       pady=WIDGET_PADDING,
                       bg=MAIN_BACKGROUND_COLOR)
    frame.grid(column=column, row=row, columnspan=columnspan, rowspan=rowspan, padx=WIDGET_MARGIN, pady=WIDGET_MARGIN)
    return frame

