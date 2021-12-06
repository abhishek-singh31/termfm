from prompt_toolkit import Application
from prompt_toolkit.layout import WindowAlign
from prompt_toolkit.widgets import MenuContainer, TextArea
from prompt_toolkit.layout.containers import Window, HSplit, VSplit
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.widgets import MenuContainer
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.application import get_app

import subprocess, sys
from art import text2art

from utils import get_input, get_menu_selection
from dir_data import data, menu_data


kb = KeyBindings()
menu_kb = KeyBindings()

heading = text2art("TERMFM", font="cyberlarge")

menu_container = Window(style="fg:ansiwhite bg:ansiblack")
menu = MenuContainer(body=menu_container, menu_items=menu_data, key_bindings=menu_kb)
menu_env = VSplit([menu])

prompt_field = Window(dont_extend_height=True, content=FormattedTextControl(focusable=False), style="bg:ansigray fg:ansiblack")
user_input_field = TextArea(multiline=False, focusable=True, dont_extend_height=True, style="bg:ansigray fg:ansiblack",
accept_handler=get_input)

root_container =  HSplit([
    Window(dont_extend_height=True, align=WindowAlign.CENTER, style="fg:ansiwhite bg:ansiblack", content=FormattedTextControl(text=heading, focusable=False)),
    menu_env,
    prompt_field,
    user_input_field,
])

layout = Layout(root_container, focused_element=menu)


# -------------------------------  KEYBINDINGS  --------------------------


# Exit
@kb.add('c-q')
def exit_(event):
    event.app.exit()


# KEYBINDINGS FOR MENU

@menu_kb.add('o')
# open a file with its associated program
def start_file(event):
    selection = get_menu_selection(data, menu.selected_menu)
    if selection['type'] == "file":
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, selection['path']])
    else:
        pass


@menu_kb.add('d')
# delete a file
def delete_file(event):
    get_app().layout.focus(user_input_field)



@menu_kb.add('r')
def rename(event):
    get_menu_selection(data, menu.selected_menu)


app = Application(key_bindings=kb, layout=layout, full_screen=True)
app.run()
