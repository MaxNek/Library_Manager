from source.database import Library
from source.gui import Gui

library = Library()

gui = Gui(library)
gui.mainloop()
