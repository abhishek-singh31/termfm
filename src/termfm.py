from prompt_toolkit import Application
from prompt_toolkit.layout import Dimension, WindowAlign
from prompt_toolkit.widgets import HorizontalLine, VerticalLine
from prompt_toolkit.layout.containers import Window, HSplit, VSplit
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.layout import Layout

from keybindings import kb


############## show home folder contents by default, have a window at left for favs and common folders

menu_content = Window(style="bg:#393E46", cursorline=True,
                      content=FormattedTextControl([
                          ("[SetCursorPosition]", ""),
                          ("fg:#ffaa33", "  hello"),
                          ("fg:ansiblue", "  world")
                      ]))

menu_container = VSplit([
    Window(width=Dimension(max=5)),  # makes a left side container (use it for favs later)
    VerticalLine(),
    menu_content,
    ])

root_container =  HSplit([
    Window(height=Dimension(max=1), align=WindowAlign.CENTER, style="fg:ansiwhite bg:ansiblack", content=FormattedTextControl(text="TERMFM", focusable=False)),
    HorizontalLine(),
    menu_container,
])

layout = Layout(root_container, focused_element=menu_content)


app = Application(key_bindings=kb, layout=layout, full_screen=True)
app.run()
