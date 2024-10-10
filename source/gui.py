from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox, Style
from source.database import Library
from source.config import AppConfig
from source.book import Book, BookTemplate


#----------------------------- GUI layout settings -----------------------------#

MAIN_WINDOW_TITLE = 'My Personal Library'
MAIN_BACKGROUND_COLOR = 'light steel blue'
MAIN_WINDOW_PADDING = 15

WIDGET_FRAME_COLOR = 'grey'
WIDGET_NAME_FONT = ('Helvetica', 10, 'bold')
WIDGET_FRAME_BORDER = 0
WIDGET_PADDING = 5
WIDGET_MARGIN = 10

BUTTON_MARGIN = 5
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
        # Set styling for ttk elements.
        style = Style()
        style.theme_settings('default',{
            'TCombobox': {
                'map': {
                    'fieldbackground':[
                        ('readonly', BOOK_WINDOW_TEXT_BG_COLOR_EDIT),
                        ('disabled', BOOK_WINDOW_TEXT_BG_COLOR)
                    ]}}})
        style.theme_use('default')

        self.library = library
        self.app_config = AppConfig()
        self.template = BookTemplate().get_template_data()

        self.title(MAIN_WINDOW_TITLE)
        self.config(bg=MAIN_BACKGROUND_COLOR, padx=MAIN_WINDOW_PADDING, pady=MAIN_WINDOW_PADDING)

        self.view_all = ViewAllBooks(parent=self, w_column=0, w_row=0)
        self.find_book = FindBook(parent=self, w_column=0, w_row=1)
        self.add_book = AddBook(parent=self, w_column=1, w_row=0, w_rowspan=2)
        self.output = OutputScreen(parent=self, w_column=0, w_row=2, w_columnspan=2)
        self.delete_book = DeleteBook(parent=self, w_column=1, w_row=3, w_rowspan=2)
        self.menu = MainMenu(parent=self)
        # self.__menu__()

        self.mainloop()

# ----------------------------- Widgets -----------------------------#

class ViewAllBooks:
    def __init__(self, parent, w_column, w_row, w_columnspan=1, w_rowspan=1):
        self.parent = parent
        sort_options = [value['name'] for key, value in self.parent.template.items() if value['sort_all_by']]
        w_structure = {'frame':
                           {'name': 'Show all books'},
                       'sections':
                           {'view_all':
                                {'label':
                                     {'text': 'Sort by:'},
                                 'dropdown':
                                     {'values': sort_options,
                                      'set': self.parent.template['title']['name'],
                                      'state': 'readonly'}}},
                        'button':
                           {'text': 'Show',
                            'command': self.__view_all__}
                       }
        self.widget = __make_widget__(parent=self.parent,
                                        w_column=w_column,
                                        w_row=w_row,
                                        w_columnspan=w_columnspan,
                                        w_rowspan=w_rowspan,
                                        w_structure=w_structure)

    def __view_all__(self):
        self.parent.output.clear_screen()
        sort = self.widget['sections']['view_all']['dropdown'].get()
        sort_by = 'title'
        for key, value in self.parent.template.items():
            if value['name'] == sort:
                sort_by = key
        all_books = self.parent.library.all_books(sort=sort)
        for book in all_books:
            if sort_by == 'title':
                line = f'"{book.get_this_info('title')}" by {book.get_this_info('author')}'
            elif sort_by == 'author':
                line = f'{book.get_this_info('author')}, "{book.get_this_info('title')}"'
            else:
                line = f'{book.get_this_info(sort_by)} {book}'
            self.parent.output.insert(index=END, book=book, args=[line])

class FindBook:
    def __init__(self, parent, w_column, w_row, w_columnspan=1, w_rowspan=1):
        self.parent = parent
        search_options = [value['name'] for key, value in self.parent.template.items() if value['search_by']]
        search_options.append('Has been borrowed?')
        w_structure = {'frame':
                           {'name': 'Find books'},
                       'sections':
                           {'find_book':
                                {'label':
                                     {'text': 'Search'},
                                 'dropdown':
                                     {'values': search_options,
                                      'set': self.parent.template['title']['name'],
                                      'state': 'readonly'},
                                 'entry': {}}},
                        'button':
                           {'text': 'Find',
                            'command': self.__find_book__}}
        self.widget = __make_widget__(parent=self.parent,
                                        w_column=w_column,
                                        w_row=w_row,
                                        w_columnspan=w_columnspan,
                                        w_rowspan=w_rowspan,
                                        w_structure=w_structure)

    def __find_book__(self):
        self.parent.output.clear_screen()
        widget = self.widget['sections']['find_book']
        search_by = widget['dropdown'].get()
        entry = widget['entry'].get().lower()
        if search_by != '' and entry != '':
            if search_by == 'Has been borrowed?':
                attribute = 'is_lent'
                prompt = 'is_lent_yes' if entry == 'yes' else 'is_lent_no'
            elif search_by == self.parent.template['is_read']['name']:
                attribute = 'is_read'
                if entry == 'yes':
                    prompt = 'True'
                elif entry == 'no':
                    prompt = 'False'
            else:
                for key, value in self.parent.template.items():
                    if value['name'] == search_by:
                        attribute = key
                prompt = entry
            criteria = (attribute, prompt)
            result = self.parent.library.find_book(criteria=criteria)
            for book in result:
                self.parent.output.insert(index=END, book=book, args=[book])
            widget['entry'].delete(first=0, last=END)

class AddBook:
    def __init__(self, parent, w_column, w_row, w_columnspan=1, w_rowspan=1):
        self.parent = parent

        w_structure = {'frame':
                           {'name': 'Add book'},
                       'sections':{},
                       'button':
                           {'text': 'Add',
                            'command': self.__add_book__}
                       }
        for section, attribute in self.parent.template.items():
            w_structure['sections'][section] = {'label':
                                                    {'text': attribute['name']},
                                                'entry': attribute['selectable']}
        self.widget = __make_widget__(parent=self.parent,
                                        w_column=w_column,
                                        w_row=w_row,
                                        w_columnspan=w_columnspan,
                                        w_rowspan=w_rowspan,
                                        w_structure=w_structure)

    def __add_book__(self):
        self.parent.output.clear_screen()
        entries = {}
        for section, attribute in self.widget['sections'].items():
            if section != 'frame' and section != 'button':
                entries[section] = attribute['entry']
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
            result = self.parent.library.add_book(new_book)
            if result:
                self.parent.output.insert(index=END, book=result, args=[result, 'has been added to the library'])
            else:
                book = self.parent.library.find_book(criteria=('isbn', new_book.get_this_info('isbn')))[0]
                self.parent.output.insert(index=END, book=book, args=[book, 'was already in the library'])
            for key, value in entries.items():
                if value.winfo_class() == 'TCombobox':
                    value.set('')
                else:
                    value.delete(first=0, last=END)
        else:
            self.parent.output.insert(index=END, args=['Book title and ISBN must be entered'])

class DeleteBook:
    def __init__(self, parent, w_column, w_row, w_columnspan=1, w_rowspan=1):
        self.parent = parent
        w_structure = {'frame':
                           {'name': 'Delete book by ISBN:'},
                       'sections':
                           {'delete_book':
                                {'entry': {}}},
                       'button':
                           {'text': 'Delete',
                            'command': self.__delete_book__}}
        self.widget = __make_widget__(parent=self.parent,
                                        w_column=w_column,
                                        w_row=w_row,
                                        w_columnspan=w_columnspan,
                                        w_rowspan=w_rowspan,
                                        w_structure=w_structure)
        self.widget['sections']['delete_book']['entry'].grid(column=0, row=0, padx=ENTRY_PADDING)
        self.widget['button'].grid(column=1, row=0, padx=ENTRY_PADDING)

    def __delete_book__(self):
        self.parent.output.clear_screen()

        delete_isbn = self.widget['sections']['delete_book']['entry'].get().strip()
        if delete_isbn != '':
            result = self.parent.library.find_book(('isbn_to_delete', delete_isbn))
            if result:
                book_to_delete = result[0]
                confirm = messagebox.askquestion(title='Delete book',
                                                 message=f'Are you sure you want to delete {book_to_delete}?',
                                                 icon=messagebox.WARNING)
                if confirm == 'yes':
                    self.parent.library.delete_book(isbn=delete_isbn)
                    self.parent.output.insert(END, f'Deleted {book_to_delete}')
                    self.widget['sections']['delete_book']['entry'].delete(first=0, last=END)
            else:
                self.parent.output.insert(index=END, args=[f'There is no bok with ISBN {delete_isbn} in the library'])
        else:
            self.parent.output.insert(index=END, args=['Enter ISBN of the book to delete'])

class OutputScreen:
    def __init__(self, parent, w_column, w_row, w_columnspan=1, w_rowspan=1):
        # TODO: make scrollbar height same as the output screen.
        self.parent = parent
        scrollbar = Scrollbar(self.parent)
        scrollbar.grid(column=2, row=2)
        self.output = Listbox(width=OUTPUT_WIDTH, height=OUTPUT_HEIGHT, yscrollcommand=scrollbar.set)
        self.output.grid(column=w_column, row=w_row, columnspan=w_columnspan, padx=WIDGET_PADDING, pady=WIDGET_PADDING)
        scrollbar.config(command=self.output.yview)
        self.output.bind('<Double-1>', self.__click__)
        self.current_books = []

    def clear_screen(self):
        self.current_books.clear()
        self.output.delete(first=0, last=END)

    def insert(self, index, args, book=None):
        self.output.insert(index, *args)
        self.current_books.append(book)

    def get_current_books(self):
        return self.current_books

    def refresh(self):
        pass

    def __click__(self, event):
        line = self.output.curselection()
        if line:
            window = BookWindow(parent=self.parent, line=line)

class BookWindow:
    def __init__(self, parent, line):
        self.parent = parent
        try:
            self.is_edit_mode = False
            current_books = self.parent.output.get_current_books()
            self.open_book = current_books[line[0]]
            self.window = Toplevel(master=parent,
                                   bg=MAIN_BACKGROUND_COLOR,
                                   padx=MAIN_WINDOW_PADDING,
                                   pady=MAIN_WINDOW_PADDING)
            self.window.title('Book Details')
            self.fields = {}
            book_data = self.open_book.get_all_info()
            centered_row = count = 0
            row = len(book_data) - len([key for key, value in book_data.items() if value[0]['width'] == 1])
            for key, value in book_data.items():
                column = 1 if count % 2 == 0 else 0
                frame = LabelFrame(master=self.window,
                                   text=f'{value[0]['name']}',
                                   highlightbackground=WIDGET_FRAME_COLOR,
                                   highlightthickness=WIDGET_FRAME_BORDER,
                                   bg=MAIN_BACKGROUND_COLOR,
                                   bd=0)
                field_width = ENTRY_WIDTH
                if value[0]['width'] == 2:
                    frame.grid(column=0, row=centered_row, columnspan=2)
                    field_width = 70
                elif value[0]['width'] == 1:
                    frame.grid(column=column, row=row)
                if key == 'description':
                    field = Text(frame,
                                     bg=BOOK_WINDOW_TEXT_BG_COLOR,
                                     height=BOOK_WINDOW_DESCRIPTION_HEIGHT,
                                     wrap='word',
                                     font=BOOK_WINDOW_TEXT_FONT)
                elif key == 'notes':
                    field = Text(frame,
                                     bg=BOOK_WINDOW_TEXT_BG_COLOR,
                                     height=BOOK_WINDOW_NOTES_HEIGHT,
                                     wrap='word',
                                     font=BOOK_WINDOW_TEXT_FONT)
                elif value[0]['selectable']:
                    field = Combobox(frame,
                                         font=BOOK_WINDOW_TEXT_FONT,
                                         values=value[0]['selectable']['options'],
                                         foreground='black')
                    field_width = ENTRY_WIDTH - 2
                else:
                    field = Text(frame,
                                     bg=BOOK_WINDOW_TEXT_BG_COLOR,
                                     height=1,
                                     wrap='word',
                                     font=BOOK_WINDOW_TEXT_FONT)
                if key == 'is_read':
                    field.insert(END, f'{'Yes' if value[1] == 'True' else 'Not yet'}')
                else:
                    field.insert(END, f'{value[1]}')
                field.config(state='disabled', width=field_width)
                field.grid(column=0, row=0, pady=BOOK_WINDOW_FRAME_PADDING)
                self.fields[key] = field
                centered_row += 1
                count += 1
                if count != 0 and count % 2 == 0:
                    row += 1

            edit_frame = Frame(self.window, bg=MAIN_BACKGROUND_COLOR)
            edit_frame.grid(column=0, row=row)

            edit_button = Button(edit_frame, text='Edit book', width=BUTTON_WIDTH * 2, command=self.__edit_book__)
            edit_button.grid(column=0, row=0, columnspan=2, pady=BUTTON_MARGIN)

            save_button = Button(edit_frame, text='Save changes', width=BUTTON_WIDTH - 1, command=self.__save_changes__)
            save_button.grid(column=0, row=1, pady=BUTTON_MARGIN)

            save_button = Button(edit_frame, text='Discard changes', width=BUTTON_WIDTH - 1,
                                 command=self.__discard_changes__)
            save_button.grid(column=1, row=1, pady=BUTTON_MARGIN)

            save_button = Button(self.window, text='Delete book', width=BUTTON_WIDTH, command=self.__delete_book_alt__)
            save_button.grid(column=1, row=row, columnspan=1, pady=BUTTON_MARGIN)
        except IndexError:
            pass

    def __edit_book__(self):
        self.is_edit_mode = True
        self.isbn_to_update = self.fields['isbn'].get('1.0', END).strip()

        for attr, container in self.fields.items():
            if container.winfo_class() == 'TCombobox':
                container.config(state='normal')
            else:
                container.config(state='normal', bg=BOOK_WINDOW_TEXT_BG_COLOR_EDIT)

    def __save_changes__(self):
        if self.is_edit_mode:
            isbn = self.isbn_to_update
            book_attributes = [key for key in self.parent.template]
            ind = 0
            for key, value in self.fields.items():
                if value.winfo_class() == 'TCombobox':
                    content = value.get().strip()
                    value.config(state='disabled')
                    if content == 'Yes':
                        content = 'True'
                    elif content == 'Not yet':
                        content = 'False'
                else:
                    content = value.get('1.0', END).strip()
                    value.config(state='disabled', bg=BOOK_WINDOW_TEXT_BG_COLOR)
                self.parent.library.update_book(isbn=isbn, attribute=(book_attributes[ind], content))
                ind += 1
            self.is_edit_mode = False
            self.parent.view_all.__view_all__()

    def __discard_changes__(self):
        if self.is_edit_mode:
            book = self.open_book
            for key, value in book.get_all_info().items():
                if type(self.fields[key]) == Combobox:
                    self.fields[key].set('')
                else:
                    self.fields[key].delete('1.0', 'end')
                if key == 'is_read':
                    self.fields[key].insert(END, f'{'Yes' if value[1] == 'True' else 'Not yet'}')
                else:
                    self.fields[key].insert(END, f'{value[1]}')
                if type(self.fields[key]) == Combobox:
                    self.fields[key].config(state='disabled')
                else:
                    self.fields[key].config(state='disabled', bg=BOOK_WINDOW_TEXT_BG_COLOR)
            self.is_edit_mode = False

    def __delete_book_alt__(self):
        isbn = self.fields['isbn'].get('1.0', END).strip()

        confirm = messagebox.askquestion('Delete book',
                                         'Are you sure you want to delete the book?',
                                         icon=messagebox.WARNING)
        if confirm == 'yes':
            self.parent.library.delete_book(isbn=isbn)
            self.parent.view_all.__view_all__()
            self.window.destroy()

class MainMenu:
    def __init__(self, parent):
        self.parent = parent
        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)

        # TODO: add 'Help' option to the Menu.
        menu = Menu(menubar, tearoff=0)
        menu.add_command(label='Settings', command=self.__open_settings__)
        menu.add_command(label='About', command=self.__open_about__)
        menu.add_separator()
        menu.add_command(label='Exit', command=self.parent.destroy)
        menubar.add_cascade(label='Menu', menu=menu)

    # TODO: Dropdown for locations
    def __open_settings__(self):
        settings = SettingsMenu()

    def __open_about__(self):
        about_window = Toplevel(bg=TOP_MENU_WINDOW_COLOR)
        about_window.title('About')
        label = Label(about_window, text=ABOUT_TEXT, justify=LEFT, bg=TOP_MENU_WINDOW_COLOR)
        label.grid(column=0, row=0, padx=TOP_MENU_WINDOW_MARGIN, pady=TOP_MENU_WINDOW_MARGIN)

class SettingsMenu:
    def __init__(self):
        self.settings = Toplevel(bg=TOP_MENU_WINDOW_COLOR, pady=TOP_MENU_WINDOW_PADDING)
        self.settings.title('Settings')

        locations_frame = LabelFrame(master=self.settings,
                                     text='Location options',
                                     highlightbackground=WIDGET_FRAME_COLOR,
                                     highlightthickness=WIDGET_FRAME_BORDER,
                                     padx=WIDGET_PADDING,
                                     pady=WIDGET_PADDING,
                                     bg=MAIN_BACKGROUND_COLOR)
        locations_frame.grid(column=0, row=0)
        self.new_location_entry = Entry(locations_frame, width=ENTRY_WIDTH*2)
        self.new_location_entry.grid(column=0, row=0, columnspan=2, padx=TOP_MENU_WINDOW_MARGIN, pady=TOP_MENU_WINDOW_MARGIN-10)
        add_button = Button(locations_frame, text='Add', width=BUTTON_WIDTH, command=self.__add_location__)
        add_button.grid(column=0, row=1, padx=TOP_MENU_WINDOW_MARGIN, pady=TOP_MENU_WINDOW_MARGIN-10)
        remove_button = Button(locations_frame, text='Remove', width=BUTTON_WIDTH, command=self.__remove_location__)
        remove_button.grid(column=1, row=1, padx=TOP_MENU_WINDOW_MARGIN, pady=TOP_MENU_WINDOW_MARGIN-10)

        rating_frame = LabelFrame(master=self.settings, text='Rating scale',
                                     highlightbackground=WIDGET_FRAME_COLOR,
                                     highlightthickness=WIDGET_FRAME_BORDER,
                                     padx=WIDGET_PADDING,
                                     pady=WIDGET_PADDING,
                                     bg=MAIN_BACKGROUND_COLOR)
        rating_frame.grid(column=0, row=1)
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

    def __add_location__(self):
        app_config = AppConfig()
        new_location = self.new_location_entry.get().strip().title()
        if new_location != '':
            result = app_config.add_book_location(new_location=new_location)
            self.__show_message__(result=result, location=new_location, act='add')

    def __remove_location__(self):
        app_config = AppConfig()
        location = self.new_location_entry.get().strip().title()
        if location != '':
            result = app_config.remove_book_location(location)
            self.__show_message__(result=result, location=location, act='remove')

    def __set_rating__(self):
        app_config = AppConfig()
        start = int(self.rating_entries['From']['entry'].get())
        end = int(self.rating_entries['To']['entry'].get())
        step = float(self.rating_entries['Step']['entry'].get())
        if start < end:
            app_config.set_rating_scale(start=start, end=end, step=step)
            messagebox.showinfo(title='Book rating', message='New rating scale has been saved')
            for value in self.rating_entries.values():
                value['entry'].set('')
        else:
            messagebox.showinfo(title='Book rating', message='"From" must be less than "To"')
            for value in self.rating_entries.values():
                value['entry'].set('')

    def __show_message__(self, result, location, act):
        if result == 1:
            message_text = (
                f'"{location}" has been {'added to' if act == 'add' else 'removed from'} the list of locations.'
                f'\n\nRestart the application to implement the change')
        elif result == 0:
            message_text = f'This location {'already exists' if act == 'add' else 'was not saved'}'
        else:
            message_text = 'Error adding a location. Try again'
        messagebox.showinfo(title='Book locations', message=message_text)
        self.new_location_entry.delete(first=0, last=END)

# ----------------------------- Static functions -----------------------------#

def __make_widget__(parent, w_structure,  w_column, w_row, w_columnspan, w_rowspan):
    widget = {'frame': LabelFrame(master=parent,
                                  text=w_structure['frame']['name'],
                                  highlightbackground=WIDGET_FRAME_COLOR,
                                  highlightthickness=WIDGET_FRAME_BORDER,
                                  padx=WIDGET_PADDING,
                                  pady=WIDGET_PADDING,
                                  bg=MAIN_BACKGROUND_COLOR)}
    widget['frame'].grid(column=w_column,
                         row=w_row,
                         columnspan=w_columnspan,
                         rowspan=w_rowspan,
                         padx=WIDGET_MARGIN,
                         pady=WIDGET_MARGIN)
    count = row = 0
    widget['sections'] = {}
    for section, elements in w_structure['sections'].items():
        widget['sections'][section] = {}
        column = 0 if count % 2 == 0 else 1
        for element, attribute in elements.items():
            if element == 'label':
                widget['sections'][section]['label'] = Label(widget['frame'], text=attribute['text'], bg=MAIN_BACKGROUND_COLOR)
                widget['sections'][section]['label'].grid(column=column, row=row)
            elif element == 'dropdown':
                widget['sections'][section]['dropdown'] = Combobox(widget['frame'], values=attribute['values'], state=attribute['state'])
                widget['sections'][section]['dropdown'].set(attribute['set'])
                widget['sections'][section]['dropdown'].grid(column=column, row=row + 1)
            elif element == 'entry':
                # Check if the entry is a dropdown (attribute = 'selectable')
                if not attribute:
                    widget['sections'][section]['entry'] = Entry(widget['frame'], width=ENTRY_WIDTH)
                else:
                    widget['sections'][section]['entry'] = Combobox(widget['frame'], state=attribute['def_state'], values=attribute['options'])
                widget['sections'][section]['entry'].grid(column=column, row=row + 2, pady=ENTRY_PADDING, padx=ENTRY_PADDING)
        count += 1
        if count != 0 and count % 2 == 0:
            row += 4
    widget['button'] = Button(widget['frame'],
                              text=w_structure['button']['text'],
                              command=w_structure['button']['command'],
                              width=BUTTON_WIDTH)
    widget['button'].grid(column=0, row=row + 3, columnspan=2, pady=BUTTON_MARGIN)
    return widget


