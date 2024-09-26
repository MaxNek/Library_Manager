from database_manager import Library
from gui_manager import GuiApp

library = Library()

app = GuiApp(library)
app.mainloop()
