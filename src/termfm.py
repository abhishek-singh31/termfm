from prompt_toolkit import Application
from prompt_toolkit.layout import Dimension, WindowAlign
from prompt_toolkit.widgets import HorizontalLine, VerticalLine, MenuContainer, MenuItem
from prompt_toolkit.layout.containers import Window, HSplit, VSplit
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.layout import Layout

from keybindings import kb
from main_menu import menu
from dir_data import data



############## show home folder contents by default, have a window at left for favs and common folders



menu_env = VSplit([
    Window(width=Dimension(max=5)),  # makes a left side container (use it for favs later)
    VerticalLine(),
    menu,
    ])

root_container =  HSplit([
    Window(height=Dimension(max=1), align=WindowAlign.CENTER, style="fg:ansiwhite bg:ansiblack", content=FormattedTextControl(text="TERMFM", focusable=False)),
    HorizontalLine(),
    menu_env,
])

layout = Layout(root_container, focused_element=menu)


app = Application(key_bindings=kb, layout=layout, full_screen=True)
app.run()



